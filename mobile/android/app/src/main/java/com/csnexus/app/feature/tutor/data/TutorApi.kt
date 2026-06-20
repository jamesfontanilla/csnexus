package com.csnexus.app.feature.tutor.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.Path

interface TutorApi {
    /** explain / simplify / hint → TutorResponseDto */
    @POST("v1/tutor/{action}")
    suspend fun tutorAction(
        @Path("action") action: String,
        @Body request: TutorActionRequestDto,
    ): TutorResponseDto

    /** step-by-step → StepByStepDto */
    @POST("v1/tutor/step-by-step")
    suspend fun stepByStep(@Body request: TutorActionRequestDto): StepByStepDto

    /** similar question */
    @POST("v1/tutor/similar")
    suspend fun similar(@Body request: TutorActionRequestDto): SimilarQuestionDto

    /** rate an interaction */
    @POST("v1/tutor/interactions/{interactionId}:rate")
    suspend fun rateInteraction(
        @Path("interactionId") interactionId: Int,
        @Body request: RateInteractionRequestDto,
    )

    /** lesson-aware chat (used from lesson companion) */
    @POST("v1/tutor/lesson-chat")
    suspend fun lessonChat(@Body request: LessonChatRequestDto): LessonChatResponseDto
}

// ── Request DTOs ──────────────────────────────────────────────────────────────

@Serializable
data class TutorActionRequestDto(
    @SerialName("question_id") val questionId: Int,
    @SerialName("selected_answer") val selectedAnswer: String? = null,
)

@Serializable
data class RateInteractionRequestDto(
    val helpful: Boolean,
)

@Serializable
data class LessonChatRequestDto(
    val message: String,
    val context: String? = null,
    @SerialName("subtopic_id") val subtopicId: Int? = null,
    @SerialName("active_section_index") val activeSectionIndex: Int? = null,
    val history: List<LessonChatHistoryItemDto> = emptyList(),
)

@Serializable
data class LessonChatHistoryItemDto(
    val role: String,
    val content: String,
)

// ── Response DTOs ─────────────────────────────────────────────────────────────

@Serializable
data class TutorResponseDto(
    @SerialName("interaction_id") val interactionId: Int = 0,
    @SerialName("response_text") val responseText: String = "",
    @SerialName("interaction_type") val interactionType: String = "",
    /** Fallback for legacy shape where the field is named differently */
    val response: String = "",
    val answer: String = "",
) {
    fun resolvedText(): String = responseText.ifBlank { response.ifBlank { answer } }
}

@Serializable
data class StepByStepDto(
    @SerialName("interaction_id") val interactionId: Int = 0,
    val steps: List<String> = emptyList(),
)

@Serializable
data class SimilarQuestionDto(
    @SerialName("interaction_id") val interactionId: Int = 0,
    val stem: String = "",
    val options: List<String>? = null,
    @SerialName("correct_answer") val correctAnswer: String = "",
    val explanation: String = "",
)

@Serializable
data class LessonChatResponseDto(
    @SerialName("interaction_id") val interactionId: Int = 0,
    @SerialName("response_text") val responseText: String = "",
    @SerialName("detected_intent") val detectedIntent: String = "",
    val response: String = "",
    val answer: String = "",
) {
    fun resolvedText(): String = responseText.ifBlank { response.ifBlank { answer } }
}
