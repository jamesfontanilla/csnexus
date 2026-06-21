package com.csnexus.app.feature.tutor.data

import kotlinx.coroutines.test.runTest
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import retrofit2.HttpException
import retrofit2.Response
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.ResponseBody.Companion.toResponseBody
import java.io.IOException

class TutorRepositoryTest {

    // ── tutorAction ───────────────────────────────────────────────────────────

    @Test
    fun tutorActionExplainReturnsResolvedText() = runTest {
        val api = FakeTutorApi(
            actionResponse = TutorResponseDto(
                interactionId = 5,
                responseText = "Here is a detailed explanation.",
            ),
        )
        val repo = TutorRepository(api)

        val result = repo.tutorAction(TutorAction.Explain, questionId = 10, selectedAnswer = "A")

        assertTrue(result is com.csnexus.app.core.network.ApiResult.Success)
        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertEquals(5, dto.interactionId)
        assertEquals("Here is a detailed explanation.", dto.resolvedText())
    }

    @Test
    fun tutorActionFallsBackToLegacyResponseField() = runTest {
        val api = FakeTutorApi(
            actionResponse = TutorResponseDto(response = "Legacy text."),
        )
        val repo = TutorRepository(api)

        val result = repo.tutorAction(TutorAction.Simplify, questionId = 1, selectedAnswer = null)

        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertEquals("Legacy text.", dto.resolvedText())
    }

    @Test
    fun tutorActionMapsHttpFailureToApiResultFailure() = runTest {
        val api = FailingTutorApi(statusCode = 503)
        val repo = TutorRepository(api)

        val result = repo.tutorAction(TutorAction.Hint, questionId = 1, selectedAnswer = null)

        assertTrue(result is com.csnexus.app.core.network.ApiResult.Failure)
        val err = (result as com.csnexus.app.core.network.ApiResult.Failure).error
        assertTrue(err is com.csnexus.app.core.error.AppError.Http)
        assertEquals(503, (err as com.csnexus.app.core.error.AppError.Http).statusCode)
    }

    @Test
    fun tutorActionMapsNetworkErrorToApiResultFailure() = runTest {
        val api = NetworkErrorTutorApi()
        val repo = TutorRepository(api)

        val result = repo.tutorAction(TutorAction.Explain, questionId = 1, selectedAnswer = null)

        assertTrue(result is com.csnexus.app.core.network.ApiResult.Failure)
        val err = (result as com.csnexus.app.core.network.ApiResult.Failure).error
        assertTrue(err is com.csnexus.app.core.error.AppError.Network)
    }

    // ── stepByStep ────────────────────────────────────────────────────────────

    @Test
    fun stepByStepReturnsOrderedSteps() = runTest {
        val api = FakeTutorApi(
            stepByStepResponse = StepByStepDto(
                interactionId = 7,
                steps = listOf("Step 1: identify givens", "Step 2: apply formula", "Step 3: verify"),
            ),
        )
        val repo = TutorRepository(api)

        val result = repo.stepByStep(questionId = 3, selectedAnswer = null)

        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertEquals(3, dto.steps.size)
        assertEquals("Step 1: identify givens", dto.steps.first())
        assertEquals(7, dto.interactionId)
    }

    @Test
    fun stepByStepEmptyStepsListIsSuccess() = runTest {
        val api = FakeTutorApi(stepByStepResponse = StepByStepDto(interactionId = 0, steps = emptyList()))
        val repo = TutorRepository(api)

        val result = repo.stepByStep(questionId = 1, selectedAnswer = null)

        assertTrue(result is com.csnexus.app.core.network.ApiResult.Success)
        assertTrue((result as com.csnexus.app.core.network.ApiResult.Success).value.steps.isEmpty())
    }

    // ── similar ───────────────────────────────────────────────────────────────

    @Test
    fun similarReturnsSimilarQuestion() = runTest {
        val api = FakeTutorApi(
            similarResponse = SimilarQuestionDto(
                interactionId = 9,
                stem = "What is 5 × 8?",
                options = listOf("35", "40", "45", "50"),
                correctAnswer = "40",
                explanation = "5 multiplied by 8 equals 40.",
            ),
        )
        val repo = TutorRepository(api)

        val result = repo.similar(questionId = 5, selectedAnswer = "A")

        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertEquals("What is 5 × 8?", dto.stem)
        assertEquals("40", dto.correctAnswer)
        assertEquals(4, dto.options?.size)
        assertEquals(9, dto.interactionId)
    }

    @Test
    fun similarWithNullOptionsIsSuccess() = runTest {
        val api = FakeTutorApi(
            similarResponse = SimilarQuestionDto(
                interactionId = 2,
                stem = "Open ended question?",
                options = null,
                correctAnswer = "Yes",
            ),
        )
        val repo = TutorRepository(api)

        val result = repo.similar(questionId = 2, selectedAnswer = null)

        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertTrue(dto.options == null)
        assertEquals("Yes", dto.correctAnswer)
    }

    // ── rateInteraction ───────────────────────────────────────────────────────

    @Test
    fun rateInteractionSuccessReturnsSuccess() = runTest {
        val api = FakeTutorApi()
        val repo = TutorRepository(api)

        val result = repo.rateInteraction(interactionId = 5, helpful = true)

        assertTrue(result is com.csnexus.app.core.network.ApiResult.Success)
        assertTrue(api.ratingCallHelpful)
        assertEquals(5, api.ratingCallInteractionId)
    }

    @Test
    fun rateInteractionFailureDoesNotThrow() = runTest {
        val api = FailingTutorApi(statusCode = 500)
        val repo = TutorRepository(api)

        // Rating errors are expected to be handled gracefully; result is Failure, not an exception.
        val result = repo.rateInteraction(interactionId = 99, helpful = false)

        assertTrue(result is com.csnexus.app.core.network.ApiResult.Failure)
    }

    // ── lessonChat ────────────────────────────────────────────────────────────

    @Test
    fun lessonChatPassesContextAndReturnsResponse() = runTest {
        val api = FakeTutorApi(
            lessonChatResponse = LessonChatResponseDto(
                interactionId = 12,
                responseText = "The answer is 42.",
            ),
        )
        val repo = TutorRepository(api)

        val result = repo.lessonChat(
            message = "What does this formula mean?",
            contextJson = buildJsonObject {
                put("lesson", "Algebra")
                put("subtopicId", 7)
            },
            subtopicId = 7,
            activeSectionIndex = 2,
            history = listOf(
                LessonChatHistoryItemDto(role = "user", content = "Summarize this section"),
                LessonChatHistoryItemDto(role = "assistant", content = "Here is a summary."),
            ),
        )

        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertEquals("The answer is 42.", dto.resolvedText())
        assertEquals(12, dto.interactionId)
        assertEquals("What does this formula mean?", api.lastLessonChatMessage)
        assertTrue(api.lastLessonChatContext is JsonElement)
        assertEquals("Algebra", api.lastLessonChatContext!!.jsonObject["lesson"]!!.jsonPrimitive.content)
        assertEquals(7, api.lastLessonChatSubtopicId)
        assertEquals(2, api.lastLessonChatActiveSectionIndex)
        assertEquals(2, api.lastLessonChatHistory.size)
    }

    @Test
    fun lessonChatFallsBackToAnswerField() = runTest {
        val api = FakeTutorApi(
            lessonChatResponse = LessonChatResponseDto(answer = "Legacy answer field."),
        )
        val repo = TutorRepository(api)

        val result = repo.lessonChat(message = "Test", contextJson = null)

        val dto = (result as com.csnexus.app.core.network.ApiResult.Success).value
        assertEquals("Legacy answer field.", dto.resolvedText())
    }

    @Test
    fun lessonChatWithNullContextSendsNullContext() = runTest {
        val api = FakeTutorApi(
            lessonChatResponse = LessonChatResponseDto(response = "OK"),
        )
        val repo = TutorRepository(api)

        repo.lessonChat(message = "Hello", contextJson = null)

        assertEquals(null, api.lastLessonChatContext)
    }
}

// ── Fakes ─────────────────────────────────────────────────────────────────────

private class FakeTutorApi(
    private val actionResponse: TutorResponseDto = TutorResponseDto(responseText = "default"),
    private val stepByStepResponse: StepByStepDto = StepByStepDto(steps = listOf("Step A")),
    private val similarResponse: SimilarQuestionDto = SimilarQuestionDto(stem = "Q?", correctAnswer = "A"),
    private val lessonChatResponse: LessonChatResponseDto = LessonChatResponseDto(response = "ok"),
) : TutorApi {
    var ratingCallInteractionId: Int = -1
        private set
    var ratingCallHelpful: Boolean = false
        private set
    var lastLessonChatMessage: String? = null
        private set
    var lastLessonChatContext: JsonElement? = null
        private set
    var lastLessonChatSubtopicId: Int? = null
        private set
    var lastLessonChatActiveSectionIndex: Int? = null
        private set
    var lastLessonChatHistory: List<LessonChatHistoryItemDto> = emptyList()
        private set

    override suspend fun tutorAction(action: String, request: TutorActionRequestDto): TutorResponseDto =
        actionResponse

    override suspend fun stepByStep(request: TutorActionRequestDto): StepByStepDto =
        stepByStepResponse

    override suspend fun similar(request: TutorActionRequestDto): SimilarQuestionDto =
        similarResponse

    override suspend fun rateInteraction(interactionId: Int, request: RateInteractionRequestDto) {
        ratingCallInteractionId = interactionId
        ratingCallHelpful = request.helpful
    }

    override suspend fun lessonChat(request: LessonChatRequestDto): LessonChatResponseDto {
        lastLessonChatMessage = request.message
        lastLessonChatContext = request.contextJson
        lastLessonChatSubtopicId = request.subtopicId
        lastLessonChatActiveSectionIndex = request.activeSectionIndex
        lastLessonChatHistory = request.history
        return lessonChatResponse
    }
}

private class FailingTutorApi(private val statusCode: Int) : TutorApi {
    private fun fail(): Nothing = throw HttpException(
        Response.error<Any>(
            statusCode,
            """{"error":{"code":"ERROR","message":"Something failed."}}"""
                .toResponseBody("application/json".toMediaType()),
        ),
    )

    override suspend fun tutorAction(action: String, request: TutorActionRequestDto): TutorResponseDto = fail()
    override suspend fun stepByStep(request: TutorActionRequestDto): StepByStepDto = fail()
    override suspend fun similar(request: TutorActionRequestDto): SimilarQuestionDto = fail()
    override suspend fun rateInteraction(interactionId: Int, request: RateInteractionRequestDto) = fail()
    override suspend fun lessonChat(request: LessonChatRequestDto): LessonChatResponseDto = fail()
}

private class NetworkErrorTutorApi : TutorApi {
    private fun fail(): Nothing = throw IOException("Network unavailable")

    override suspend fun tutorAction(action: String, request: TutorActionRequestDto): TutorResponseDto = fail()
    override suspend fun stepByStep(request: TutorActionRequestDto): StepByStepDto = fail()
    override suspend fun similar(request: TutorActionRequestDto): SimilarQuestionDto = fail()
    override suspend fun rateInteraction(interactionId: Int, request: RateInteractionRequestDto) = fail()
    override suspend fun lessonChat(request: LessonChatRequestDto): LessonChatResponseDto = fail()
}
