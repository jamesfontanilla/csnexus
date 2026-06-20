package com.csnexus.app.feature.mockexam.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.mockexam.data.MockExamAttemptDto
import com.csnexus.app.feature.mockexam.data.MockExamRepository
import com.csnexus.app.feature.mockexam.data.MockExamReview
import com.csnexus.app.feature.mockexam.data.MockExamSubmittedDto
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import com.csnexus.app.feature.quizzes.ui.effectiveSelectedAnswer
import java.time.Instant
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

enum class MockExamPhase {
    Setup,
    Loading,
    Active,
    Submitted,
}

data class MockExamUiState(
    val phase: MockExamPhase = MockExamPhase.Setup,
    val attempt: MockExamAttemptDto? = null,
    val result: MockExamSubmittedDto? = null,
    val review: MockExamReview? = null,
    val currentIndex: Int = 0,
    val remainingSeconds: Int = 0,
    val errorMessage: String? = null,
    val statusMessage: String? = null,
    val savingQuestionIds: Set<Int> = emptySet(),
    val isSubmitting: Boolean = false,
    val isLoadingReview: Boolean = false,
) {
    val currentQuestion: QuizQuestionDto?
        get() = attempt?.questions?.getOrNull(currentIndex)

    val answeredCount: Int
        get() = attempt?.questions.orEmpty().count { it.effectiveSelectedAnswer != null }

    val isLinearNoRevisit: Boolean
        get() = attempt?.navPolicy.equals("LINEAR_NO_REVISIT", ignoreCase = true)
}

class MockExamViewModel(
    private val repository: MockExamRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(MockExamUiState())
    val uiState: StateFlow<MockExamUiState> = _uiState.asStateFlow()
    private var timerJob: Job? = null

    override fun onCleared() {
        timerJob?.cancel()
        super.onCleared()
    }

    fun startExam() {
        viewModelScope.launch {
            timerJob?.cancel()
            _uiState.value = MockExamUiState(
                phase = MockExamPhase.Loading,
                statusMessage = "Starting mock exam...",
            )
            when (val result = repository.start()) {
                is ApiResult.Success -> activateAttempt(result.value, "Mock exam #${result.value.effectiveAttemptId} started.")
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        phase = MockExamPhase.Setup,
                        errorMessage = result.error.userMessage(),
                        statusMessage = null,
                    )
                }
            }
        }
    }

    fun answer(questionId: Int, selectedAnswer: String) {
        val state = _uiState.value
        val attempt = state.attempt ?: return
        val question = state.attempt.questions.firstOrNull { it.id == questionId } ?: return
        if (selectedAnswer.isBlank() || state.isSubmitting) return
        if (state.isLinearNoRevisit && question.finalizedAt != null) return

        viewModelScope.launch {
            val finalizedAt = Instant.now().toString()
            _uiState.update {
                it.copy(
                    attempt = attempt.copy(
                        questions = attempt.questions.map { item ->
                            if (item.id == questionId) {
                                item.copy(selected = selectedAnswer, selectedAnswer = selectedAnswer, finalizedAt = finalizedAt)
                            } else {
                                item
                            }
                        },
                    ),
                    savingQuestionIds = it.savingQuestionIds + questionId,
                    errorMessage = null,
                    statusMessage = "Saving answer...",
                )
            }

            when (val result = repository.answer(attempt.effectiveAttemptId, questionId, selectedAnswer)) {
                is ApiResult.Success -> _uiState.update {
                    val nextIndex = if (it.isLinearNoRevisit) {
                        (it.currentIndex + 1).coerceAtMost(it.attempt?.questions.orEmpty().lastIndex.coerceAtLeast(0))
                    } else {
                        it.currentIndex
                    }
                    it.copy(
                        currentIndex = nextIndex,
                        savingQuestionIds = it.savingQuestionIds - questionId,
                        statusMessage = "Answer saved.",
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        savingQuestionIds = it.savingQuestionIds - questionId,
                        errorMessage = result.error.userMessage(),
                        statusMessage = null,
                    )
                }
            }
        }
    }

    fun goToQuestion(index: Int) {
        val questions = _uiState.value.attempt?.questions.orEmpty()
        if (index !in questions.indices) return
        _uiState.update { it.copy(currentIndex = index, errorMessage = null, statusMessage = null) }
    }

    fun previousQuestion() {
        if (_uiState.value.isLinearNoRevisit) return
        goToQuestion(_uiState.value.currentIndex - 1)
    }

    fun nextQuestion() {
        goToQuestion(_uiState.value.currentIndex + 1)
    }

    fun submitExam() {
        val attemptId = _uiState.value.attempt?.effectiveAttemptId ?: return
        if (_uiState.value.isSubmitting) return
        viewModelScope.launch {
            _uiState.update { it.copy(isSubmitting = true, errorMessage = null, statusMessage = "Submitting exam...") }
            when (val result = repository.submit(attemptId)) {
                is ApiResult.Success -> {
                    timerJob?.cancel()
                    _uiState.update {
                        it.copy(
                            phase = MockExamPhase.Submitted,
                            result = result.value,
                            isSubmitting = false,
                            isLoadingReview = true,
                            statusMessage = "Mock exam submitted.",
                        )
                    }
                    loadReview(result.value.attemptId.takeIf { it > 0 } ?: attemptId, result.value)
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        isSubmitting = false,
                        errorMessage = result.error.userMessage(),
                        statusMessage = null,
                    )
                }
            }
        }
    }

    fun reportFocusLoss(kind: String = "app_backgrounded") {
        val attemptId = _uiState.value.attempt?.effectiveAttemptId ?: return
        if (_uiState.value.phase != MockExamPhase.Active) return
        viewModelScope.launch {
            repository.reportFocusLoss(attemptId, kind = kind, at = Instant.now().toString())
        }
    }

    fun loadReview(attemptId: Int, submitted: MockExamSubmittedDto? = _uiState.value.result) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoadingReview = true, errorMessage = null) }
            when (val result = repository.review(attemptId, submitted)) {
                is ApiResult.Success -> _uiState.update {
                    it.copy(
                        review = result.value,
                        result = result.value.submitted ?: it.result,
                        isLoadingReview = false,
                        statusMessage = if (result.value.fromCache) {
                            "Offline. Showing cached finalized review."
                        } else {
                            "Mock exam review loaded."
                        },
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        isLoadingReview = false,
                        errorMessage = result.error.userMessage(),
                    )
                }
            }
        }
    }

    fun acceptRecommendation() {
        val attemptId = _uiState.value.review?.attemptId ?: _uiState.value.result?.attemptId ?: return
        viewModelScope.launch {
            when (val result = repository.acceptRecommendation(attemptId)) {
                is ApiResult.Success -> loadReview(attemptId)
                is ApiResult.Failure -> _uiState.update { it.copy(errorMessage = result.error.userMessage()) }
            }
        }
    }

    fun abandonLocalAttempt() {
        timerJob?.cancel()
        _uiState.value = MockExamUiState()
    }

    private fun activateAttempt(attempt: MockExamAttemptDto, message: String) {
        val remaining = attempt.remainingSeconds ?: attempt.timeLimitMinutes * 60
        _uiState.value = MockExamUiState(
            phase = MockExamPhase.Active,
            attempt = attempt,
            remainingSeconds = remaining,
            statusMessage = message,
        )
        startTimer()
    }

    private fun startTimer() {
        timerJob?.cancel()
        timerJob = viewModelScope.launch {
            while (_uiState.value.phase == MockExamPhase.Active && _uiState.value.remainingSeconds > 0) {
                delay(1_000)
                _uiState.update { it.copy(remainingSeconds = (it.remainingSeconds - 1).coerceAtLeast(0)) }
            }
        }
    }
}

val MockExamAttemptDto.effectiveAttemptId: Int
    get() = attemptId.takeIf { it > 0 } ?: id

class MockExamViewModelFactory(
    private val repository: MockExamRepository,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return MockExamViewModel(repository) as T
    }
}
