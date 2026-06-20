package com.csnexus.app.feature.quizzes.data

import android.content.Context
import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall

enum class QuizScope(val apiValue: String) {
    Module("module"),
    Topic("topic"),
    Subtopic("subtopic");

    companion object {
        fun from(raw: String): QuizScope = entries.firstOrNull {
            it.apiValue.equals(raw, ignoreCase = true)
        } ?: Subtopic
    }
}

enum class QuizMode(val label: String, val description: String, val timeLimitSeconds: Int) {
    Practice(
        label = "Practice Mode",
        description = "20 minutes, relaxed pace and review after submission",
        timeLimitSeconds = 20 * 60,
    ),
    Exam(
        label = "Exam Mode",
        description = "15 minutes, closer to real CSE pacing",
        timeLimitSeconds = 15 * 60,
    ),
    Power(
        label = "Power Mode",
        description = "10 minutes, fastest challenge",
        timeLimitSeconds = 10 * 60,
    );
}

interface ActiveQuizStore {
    fun activeAttemptId(): Int?
    fun saveActiveAttemptId(attemptId: Int)
    fun clearActiveAttempt()
}

class SharedPreferencesActiveQuizStore(context: Context) : ActiveQuizStore {
    private val prefs = context.getSharedPreferences("active_quiz", Context.MODE_PRIVATE)

    override fun activeAttemptId(): Int? {
        val value = prefs.getInt(KEY_ATTEMPT_ID, 0)
        return value.takeIf { it > 0 }
    }

    override fun saveActiveAttemptId(attemptId: Int) {
        prefs.edit().putInt(KEY_ATTEMPT_ID, attemptId).apply()
    }

    override fun clearActiveAttempt() {
        prefs.edit().remove(KEY_ATTEMPT_ID).apply()
    }

    private companion object {
        const val KEY_ATTEMPT_ID = "attempt_id"
    }
}

class QuizRepository(
    private val quizApi: QuizApi,
    private val activeQuizStore: ActiveQuizStore? = null,
) {
    fun activeAttemptId(): Int? = activeQuizStore?.activeAttemptId()

    suspend fun startQuiz(scope: QuizScope, scopeId: Int, mode: QuizMode): ApiResult<QuizAttemptDto> {
        return when (
            val result = safeApiCall {
                val request = QuizStartRequestDto(timeLimitSeconds = mode.timeLimitSeconds)
                when (scope) {
                    QuizScope.Module -> quizApi.startModuleQuiz(scopeId, request)
                    QuizScope.Topic -> quizApi.startTopicQuiz(scopeId, request)
                    QuizScope.Subtopic -> quizApi.startSubtopicQuiz(scopeId, request)
                }
            }
        ) {
            is ApiResult.Success -> {
                activeQuizStore?.saveActiveAttemptId(result.value.attemptId)
                result
            }
            is ApiResult.Failure -> result
        }
    }

    suspend fun startSubtopicQuiz(subtopicId: Int): ApiResult<QuizAttemptDto> =
        startQuiz(QuizScope.Subtopic, subtopicId, QuizMode.Practice)

    suspend fun attempt(attemptId: Int): ApiResult<QuizAttemptDto> =
        safeApiCall { quizApi.attempt(attemptId) }

    suspend fun answer(attemptId: Int, questionId: Int, selectedAnswer: String): ApiResult<Unit> =
        safeApiCall {
            quizApi.answer(attemptId, questionId, QuizAnswerRequestDto(selectedAnswer))
            Unit
        }

    suspend fun submit(attemptId: Int): ApiResult<QuizSubmittedDto> {
        return when (val result = safeApiCall { quizApi.submit(attemptId) }) {
            is ApiResult.Success -> {
                activeQuizStore?.clearActiveAttempt()
                result
            }
            is ApiResult.Failure -> {
                if (result.error is AppError.Network) {
                    when (val restored = safeApiCall { quizApi.attempt(attemptId) }) {
                        is ApiResult.Success -> {
                            val submitted = restored.value.toSubmittedDtoOrNull()
                            if (submitted != null) {
                                activeQuizStore?.clearActiveAttempt()
                                ApiResult.Success(submitted)
                            } else {
                                result
                            }
                        }
                        is ApiResult.Failure -> result
                    }
                } else {
                    result
                }
            }
        }
    }
}

private fun QuizAttemptDto.toSubmittedDtoOrNull(): QuizSubmittedDto? {
    if (!status.equals("SUBMITTED", ignoreCase = true)) return null
    return QuizSubmittedDto(
        attemptId = attemptId,
        status = status,
        score = score ?: 0,
        maxScore = maxScore ?: questions.size,
        percentage = percentage ?: 0.0,
        passed = passed,
        isPassing = isPassing,
        isPerfect = isPerfect,
        awardedXp = awardedXp,
        questions = questions,
    )
}
