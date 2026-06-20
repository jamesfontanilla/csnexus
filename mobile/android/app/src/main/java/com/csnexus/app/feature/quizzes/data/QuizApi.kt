package com.csnexus.app.feature.quizzes.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path

interface QuizApi {
    @POST("v1/modules/{moduleId}/quiz-attempts")
    suspend fun startModuleQuiz(
        @Path("moduleId") moduleId: Int,
        @Body request: QuizStartRequestDto = QuizStartRequestDto(),
    ): QuizAttemptDto

    @POST("v1/topics/{topicId}/quiz-attempts")
    suspend fun startTopicQuiz(
        @Path("topicId") topicId: Int,
        @Body request: QuizStartRequestDto = QuizStartRequestDto(),
    ): QuizAttemptDto

    @POST("v1/subtopics/{subtopicId}/quiz-attempts")
    suspend fun startSubtopicQuiz(
        @Path("subtopicId") subtopicId: Int,
        @Body request: QuizStartRequestDto = QuizStartRequestDto(),
    ): QuizAttemptDto

    @GET("v1/quiz-attempts/{attemptId}")
    suspend fun attempt(@Path("attemptId") attemptId: Int): QuizAttemptDto

    @PATCH("v1/quiz-attempts/{attemptId}/answers/{questionId}")
    suspend fun answer(
        @Path("attemptId") attemptId: Int,
        @Path("questionId") questionId: Int,
        @Body request: QuizAnswerRequestDto,
    )

    @POST("v1/quiz-attempts/{attemptId}:submit")
    suspend fun submit(
        @Path("attemptId") attemptId: Int,
        @Body request: QuizSubmitRequestDto = QuizSubmitRequestDto(),
    ): QuizSubmittedDto
}

@Serializable
data class QuizStartRequestDto(
    @SerialName("time_limit_seconds")
    val timeLimitSeconds: Int? = null,
)

@Serializable
data class QuizAnswerRequestDto(
    @SerialName("selected_answer")
    val selectedAnswer: String,
)

@Serializable
data class QuizSubmitRequestDto(
    val client: String = "android",
)

@Serializable
data class QuizAttemptDto(
    @SerialName("attempt_id")
    val attemptId: Int,
    val status: String = "IN_PROGRESS",
    @SerialName("scope_level")
    val scopeLevel: String? = null,
    @SerialName("scope_id")
    val scopeId: Int? = null,
    @SerialName("started_at")
    val startedAt: String = "",
    @SerialName("time_limit_seconds")
    val timeLimitSeconds: Int? = null,
    val score: Int? = null,
    @SerialName("max_score")
    val maxScore: Int? = null,
    val percentage: Double? = null,
    val passed: Boolean? = null,
    @SerialName("is_passing")
    val isPassing: Boolean? = null,
    @SerialName("is_perfect")
    val isPerfect: Boolean? = null,
    @SerialName("awarded_xp")
    val awardedXp: Int = 0,
    val questions: List<QuizQuestionDto> = emptyList(),
    @SerialName("total_questions")
    val totalQuestions: Int = questions.size,
)

@Serializable
data class QuizQuestionDto(
    val id: Int,
    val ordinal: Int = 0,
    val stem: String = "",
    val qtype: String = "MULTIPLE_CHOICE",
    val difficulty: String = "",
    val options: List<String>? = null,
    @SerialName("selected_answer")
    val selectedAnswer: String? = null,
    val selected: String? = null,
    @SerialName("finalized_at")
    val finalizedAt: String? = null,
    @SerialName("is_correct")
    val isCorrect: Boolean? = null,
    @SerialName("correct_answer")
    val correctAnswer: String? = null,
    val correct: String? = null,
    val explanation: String? = null,
)

@Serializable
data class QuizSubmittedDto(
    @SerialName("attempt_id")
    val attemptId: Int,
    val status: String = "SUBMITTED",
    val score: Int = 0,
    @SerialName("max_score")
    val maxScore: Int = 0,
    val percentage: Double = 0.0,
    val passed: Boolean? = null,
    @SerialName("is_passing")
    val isPassing: Boolean? = null,
    @SerialName("is_perfect")
    val isPerfect: Boolean? = null,
    @SerialName("awarded_xp")
    val awardedXp: Int = 0,
    val questions: List<QuizQuestionDto> = emptyList(),
)
