package com.csnexus.app.feature.quizzes.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.quizzes.data.QuizAttemptDto
import com.csnexus.app.feature.quizzes.data.QuizMode
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import com.csnexus.app.feature.quizzes.data.QuizRepository
import com.csnexus.app.feature.quizzes.data.QuizScope
import com.csnexus.app.feature.quizzes.data.QuizSubmittedDto
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

enum class QuizPhase {
    SelectMode,
    Loading,
    InProgress,
    Submitted,
    LessonBlocked,
}

data class QuizUiState(
    val phase: QuizPhase = QuizPhase.SelectMode,
    val selectedMode: QuizMode? = null,
    val attempt: QuizAttemptDto? = null,
    val result: QuizSubmittedDto? = null,
    val currentIndex: Int = 0,
    val errorMessage: String? = null,
    val saveMessage: String? = null,
    val isSubmitting: Boolean = false,
    val savingQuestionIds: Set<Int> = emptySet(),
    val restoredAttemptId: Int? = null,
    val remainingSeconds: Int? = null,
) {
    val currentQuestion: QuizQuestionDto?
        get() = attempt?.questions?.getOrNull(currentIndex)

    val answeredCount: Int
        get() = attempt?.questions.orEmpty().count { it.effectiveSelectedAnswer != null }
}

val QuizQuestionDto.effectiveSelectedAnswer: String?
    get() = selectedAnswer ?: selected

val QuizQuestionDto.effectiveCorrectAnswer: String?
    get() = correctAnswer ?: correct

class QuizViewModel(
    private val repository: QuizRepository,
    private val scope: QuizScope,
    private val scopeId: Int,
) : ViewModel() {
    private val _uiState = MutableStateFlow(QuizUiState())
    val uiState: StateFlow<QuizUiState> = _uiState.asStateFlow()
    private var timerJob: Job? = null

    init {
        restoreActiveAttempt()
    }

    fun startQuiz(mode: QuizMode) {
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    phase = QuizPhase.Loading,
                    selectedMode = mode,
                    attempt = null,
                    result = null,
                    currentIndex = 0,
                    errorMessage = null,
                    saveMessage = null,
                )
            }
            when (val started = repository.startQuiz(scope, scopeId, mode)) {
                is ApiResult.Success -> _uiState.update {
                    val remainingSeconds = started.value.timeLimitSeconds
                    startCountdown(remainingSeconds)
                    it.copy(
                        phase = QuizPhase.InProgress,
                        attempt = started.value,
                        result = null,
                        currentIndex = 0,
                        errorMessage = null,
                        saveMessage = "Quiz attempt #${started.value.attemptId} started.",
                        remainingSeconds = remainingSeconds,
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    if (started.error.isLessonBlocked()) {
                        it.copy(
                            phase = QuizPhase.LessonBlocked,
                            errorMessage = null,
                            saveMessage = null,
                        )
                    } else {
                        it.copy(
                            phase = QuizPhase.SelectMode,
                            errorMessage = started.error.userMessage(),
                            saveMessage = null,
                        )
                    }
                }
            }
        }
    }

    fun answer(questionId: Int, selectedAnswer: String) {
        val attempt = _uiState.value.attempt ?: return
        if (_uiState.value.isSubmitting || selectedAnswer.isBlank()) return
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    attempt = attempt.copy(
                        questions = attempt.questions.map { question ->
                            if (question.id == questionId) {
                                question.copy(selectedAnswer = selectedAnswer)
                            } else {
                                question
                            }
                        },
                    ),
                    errorMessage = null,
                    saveMessage = "Saving answer...",
                    savingQuestionIds = it.savingQuestionIds + questionId,
                )
            }
            when (val result = repository.answer(attempt.attemptId, questionId, selectedAnswer)) {
                is ApiResult.Success -> _uiState.update {
                    it.copy(
                        saveMessage = "Answer saved.",
                        savingQuestionIds = it.savingQuestionIds - questionId,
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        errorMessage = result.error.userMessage(),
                        saveMessage = null,
                        savingQuestionIds = it.savingQuestionIds - questionId,
                    )
                }
            }
        }
    }

    fun goToQuestion(index: Int) {
        val questions = _uiState.value.attempt?.questions.orEmpty()
        if (index !in questions.indices) return
        _uiState.update { it.copy(currentIndex = index, errorMessage = null, saveMessage = null) }
    }

    fun nextQuestion() {
        goToQuestion(_uiState.value.currentIndex + 1)
    }

    fun previousQuestion() {
        goToQuestion(_uiState.value.currentIndex - 1)
    }

    fun submit() {
        submitInternal(fromTimer = false)
    }

    private fun submitInternal(fromTimer: Boolean) {
        val attemptId = _uiState.value.attempt?.attemptId ?: return
        if (_uiState.value.isSubmitting) return
        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, errorMessage = null, saveMessage = null) }
            when (val submitted = repository.submit(attemptId)) {
                is ApiResult.Success -> {
                    if (!fromTimer) timerJob?.cancel()
                    _uiState.update {
                        it.copy(
                            phase = QuizPhase.Submitted,
                            result = submitted.value,
                            isSubmitting = false,
                            currentIndex = 0,
                            saveMessage = if (fromTimer) "Time expired. Quiz submitted." else "Quiz submitted.",
                            remainingSeconds = 0,
                        )
                    }
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        isSubmitting = false,
                        errorMessage = submitted.error.userMessage(),
                    )
                }
            }
        }
    }

    fun backToModes() {
        timerJob?.cancel()
        _uiState.value = QuizUiState()
    }

    private fun restoreActiveAttempt() {
        val attemptId = repository.activeAttemptId() ?: return
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    phase = QuizPhase.Loading,
                    restoredAttemptId = attemptId,
                    saveMessage = "Restoring active quiz...",
                )
            }
            when (val result = repository.attempt(attemptId)) {
                is ApiResult.Success -> {
                    val submitted = result.value.status.equals("SUBMITTED", ignoreCase = true)
                    if (!submitted) startCountdown(result.value.timeLimitSeconds)
                    _uiState.update {
                        it.copy(
                            phase = if (submitted) QuizPhase.SelectMode else QuizPhase.InProgress,
                            attempt = result.value.takeUnless { submitted },
                            restoredAttemptId = attemptId,
                            saveMessage = if (submitted) null else "Restored quiz attempt #$attemptId.",
                            remainingSeconds = result.value.timeLimitSeconds.takeUnless { submitted },
                        )
                    }
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        phase = QuizPhase.SelectMode,
                        restoredAttemptId = attemptId,
                        errorMessage = "Could not restore active quiz: ${result.error.userMessage()}",
                        saveMessage = null,
                    )
                }
            }
        }
    }

    private fun AppError.isLessonBlocked(): Boolean {
        return this is AppError.Http &&
            statusCode == 409 &&
            (
                code.equals("LESSON_NOT_COMPLETED", ignoreCase = true) ||
                    code.equals("lesson_not_completed", ignoreCase = true) ||
                    message.equals("lesson_not_completed", ignoreCase = true) ||
                    message.contains("lesson", ignoreCase = true)
                )
    }

    private fun startCountdown(totalSeconds: Int?) {
        timerJob?.cancel()
        if (totalSeconds == null || totalSeconds <= 0) return
        timerJob = viewModelScope.launch {
            var remaining = totalSeconds
            while (remaining > 0) {
                delay(1_000)
                remaining -= 1
                _uiState.update { state ->
                    if (state.phase == QuizPhase.InProgress) {
                        state.copy(remainingSeconds = remaining)
                    } else {
                        state
                    }
                }
            }
            submitInternal(fromTimer = true)
        }
    }
}

class QuizViewModelFactory(
    private val repository: QuizRepository,
    private val scope: QuizScope,
    private val scopeId: Int,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return QuizViewModel(repository, scope, scopeId) as T
    }
}
