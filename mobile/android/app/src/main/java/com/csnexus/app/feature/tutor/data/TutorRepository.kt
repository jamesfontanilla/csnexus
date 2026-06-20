package com.csnexus.app.feature.tutor.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall

/** Typed enumeration of the actions the web Tutor supports. */
enum class TutorAction(val endpoint: String, val label: String) {
    Explain("explain", "Explain"),
    Simplify("simplify", "Simplify"),
    Hint("hint", "Hint"),
    ;

    companion object {
        val actionValues: List<TutorAction> = entries
    }
}

/**
 * Contract for tutor interactions. Extracting an interface makes the ViewModel
 * testable without subclassing the concrete implementation.
 */
interface TutorRepositoryContract {
    suspend fun tutorAction(
        action: TutorAction,
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<TutorResponseDto>

    suspend fun stepByStep(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<StepByStepDto>

    suspend fun similar(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<SimilarQuestionDto>

    suspend fun rateInteraction(interactionId: Int, helpful: Boolean): ApiResult<Unit>

    suspend fun lessonChat(
        message: String,
        context: String? = null,
        subtopicId: Int? = null,
        activeSectionIndex: Int? = null,
        history: List<LessonChatHistoryItemDto> = emptyList(),
    ): ApiResult<LessonChatResponseDto>
}

open class TutorRepository(
    private val tutorApi: TutorApi,
) : TutorRepositoryContract {

    /**
     * Fire a named tutor action (explain / simplify / hint) against a question ID.
     * [selectedAnswer] is optional context for explain/hint actions.
     */
    override suspend fun tutorAction(
        action: TutorAction,
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<TutorResponseDto> = safeApiCall {
        tutorApi.tutorAction(
            action = action.endpoint,
            request = TutorActionRequestDto(questionId = questionId, selectedAnswer = selectedAnswer),
        )
    }

    /** Step-by-step solution for [questionId]. */
    override suspend fun stepByStep(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<StepByStepDto> = safeApiCall {
        tutorApi.stepByStep(TutorActionRequestDto(questionId = questionId, selectedAnswer = selectedAnswer))
    }

    /** Generate a similar practice question for [questionId]. */
    override suspend fun similar(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<SimilarQuestionDto> = safeApiCall {
        tutorApi.similar(TutorActionRequestDto(questionId = questionId, selectedAnswer = selectedAnswer))
    }

    /** Rate a previous tutor interaction. Fails silently by design (mirrors web behavior). */
    override suspend fun rateInteraction(interactionId: Int, helpful: Boolean): ApiResult<Unit> = safeApiCall {
        tutorApi.rateInteraction(interactionId, RateInteractionRequestDto(helpful = helpful))
    }

    /**
     * Lesson-aware chat used from within the lesson companion panel.
     * [context] is the lesson slug or subject so the tutor can ground its answer.
     */
    override suspend fun lessonChat(
        message: String,
        context: String?,
        subtopicId: Int?,
        activeSectionIndex: Int?,
        history: List<LessonChatHistoryItemDto>,
    ): ApiResult<LessonChatResponseDto> =
        safeApiCall {
            tutorApi.lessonChat(
                LessonChatRequestDto(
                    message = message,
                    context = context,
                    subtopicId = subtopicId,
                    activeSectionIndex = activeSectionIndex,
                    history = history,
                ),
            )
        }
}
