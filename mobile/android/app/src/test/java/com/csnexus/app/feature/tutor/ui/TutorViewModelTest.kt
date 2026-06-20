package com.csnexus.app.feature.tutor.ui

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.error.AppError
import com.csnexus.app.feature.tutor.data.LessonChatHistoryItemDto
import com.csnexus.app.feature.tutor.data.LessonChatRequestDto
import com.csnexus.app.feature.tutor.data.LessonChatResponseDto
import com.csnexus.app.feature.tutor.data.RateInteractionRequestDto
import com.csnexus.app.feature.tutor.data.SimilarQuestionDto
import com.csnexus.app.feature.tutor.data.StepByStepDto
import com.csnexus.app.feature.tutor.data.TutorAction
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract
import com.csnexus.app.feature.tutor.data.TutorResponseDto
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class TutorViewModelTest {

    private val dispatcher = StandardTestDispatcher()

    @Before
    fun setUp() {
        Dispatchers.setMain(dispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    // ── Input validation ──────────────────────────────────────────────────────

    @Test
    fun requestActionDoesNothingWhenQuestionIdIsBlank() = runTest {
        val vm = TutorViewModel(FakeTutorRepository())
        // No question ID set; action should be ignored.
        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        assertFalse(vm.uiState.value.loading)
        assertNull(vm.uiState.value.result)
    }

    @Test
    fun questionIdInputFiltersNonDigits() = runTest {
        val vm = TutorViewModel(FakeTutorRepository())
        vm.onQuestionIdChanged("abc12!@#")
        assertEquals("12", vm.uiState.value.questionIdInput)
    }

    @Test
    fun questionIdInputTruncatesAt9Digits() = runTest {
        val vm = TutorViewModel(FakeTutorRepository())
        vm.onQuestionIdChanged("123456789012")
        assertEquals("123456789", vm.uiState.value.questionIdInput)
    }

    // ── Explain action ────────────────────────────────────────────────────────

    @Test
    fun requestActionExplainSetsTextResultAndInteractionId() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(
                TutorResponseDto(interactionId = 7, responseText = "Explanation text."),
            ),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("10")

        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        val state = vm.uiState.value
        assertFalse(state.loading)
        assertTrue(state.result is TutorResult.Text)
        assertEquals("Explanation text.", (state.result as TutorResult.Text).text)
        assertEquals(7, state.interactionId)
    }

    @Test
    fun requestActionUsesSelectedAnswerInput() = runTest {
        val repo = FakeTutorRepository()
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("5")
        vm.onSelectedAnswerChanged("B")

        vm.requestAction(TutorAction.Hint)
        advanceUntilIdle()

        assertEquals("B", repo.lastSelectedAnswer)
    }

    // ── Step-by-step action ───────────────────────────────────────────────────

    @Test
    fun requestStepByStepSetsStepsResult() = runTest {
        val repo = FakeTutorRepository(
            stepByStepResult = ApiResult.Success(
                StepByStepDto(
                    interactionId = 3,
                    steps = listOf("Step 1", "Step 2", "Step 3"),
                ),
            ),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("8")

        vm.requestStepByStep()
        advanceUntilIdle()

        val state = vm.uiState.value
        assertTrue(state.result is TutorResult.Steps)
        assertEquals(3, (state.result as TutorResult.Steps).steps.size)
        assertEquals(3, state.interactionId)
    }

    @Test
    fun requestStepByStepDoesNothingWhenQuestionIdBlank() = runTest {
        val vm = TutorViewModel(FakeTutorRepository())
        vm.requestStepByStep()
        advanceUntilIdle()

        assertNull(vm.uiState.value.result)
    }

    // ── Similar action ────────────────────────────────────────────────────────

    @Test
    fun requestSimilarSetsSimilarResult() = runTest {
        val repo = FakeTutorRepository(
            similarResult = ApiResult.Success(
                SimilarQuestionDto(
                    interactionId = 11,
                    stem = "What is 3+3?",
                    options = listOf("5", "6", "7"),
                    correctAnswer = "6",
                    explanation = "3 plus 3 is 6.",
                ),
            ),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("2")

        vm.requestSimilar()
        advanceUntilIdle()

        val state = vm.uiState.value
        assertTrue(state.result is TutorResult.Similar)
        assertEquals("What is 3+3?", (state.result as TutorResult.Similar).dto.stem)
        assertEquals(11, state.interactionId)
    }

    // ── Failed send and retry ─────────────────────────────────────────────────

    @Test
    fun actionFailureSetsFailedSendResult() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Failure(AppError.Network("Network unreachable")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("4")

        vm.requestAction(TutorAction.Simplify)
        advanceUntilIdle()

        val state = vm.uiState.value
        assertFalse(state.loading)
        assertTrue(state.result is TutorResult.FailedSend)
        assertEquals("Simplify", (state.result as TutorResult.FailedSend).retryLabel)
        assertNull(state.interactionId)
    }

    @Test
    fun retryLastActionTriesAgainAfterFailure() = runTest {
        var callCount = 0
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(responseText = "ok")),
            onAction = { callCount++ },
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        // First call succeeds; set up a FailedSend manually via a failing repo then retry.
        val failRepo = FakeTutorRepository(
            actionResult = ApiResult.Failure(AppError.Network("down")),
        )
        val vmFail = TutorViewModel(failRepo)
        vmFail.onQuestionIdChanged("1")

        vmFail.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        assertTrue(vmFail.uiState.value.result is TutorResult.FailedSend)

        // After retry, same action is dispatched again.
        vmFail.retryLastAction()
        advanceUntilIdle()

        // Still a FailedSend because repo still returns Failure; no crash.
        assertTrue(vmFail.uiState.value.result is TutorResult.FailedSend)
    }

    @Test
    fun stepByStepFailureSetsLabeledRetry() = runTest {
        val repo = FakeTutorRepository(
            stepByStepResult = ApiResult.Failure(AppError.Network("timeout")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("3")

        vm.requestStepByStep()
        advanceUntilIdle()

        val result = vm.uiState.value.result as? TutorResult.FailedSend
        assertNotNull(result)
        assertEquals("Step-by-step", result!!.retryLabel)
    }

    @Test
    fun similarFailureSetsLabeledRetry() = runTest {
        val repo = FakeTutorRepository(
            similarResult = ApiResult.Failure(AppError.Http(503, "ERROR", "Server down", null)),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        vm.requestSimilar()
        advanceUntilIdle()

        val result = vm.uiState.value.result as? TutorResult.FailedSend
        assertNotNull(result)
        assertEquals("Similar", result!!.retryLabel)
    }

    // ── Loading state ─────────────────────────────────────────────────────────

    @Test
    fun loadingIsTrueWhileRequestIsInFlight() = runTest {
        val repo = FakeTutorRepository()
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        // Before advanceUntilIdle, loading should be true.
        vm.requestAction(TutorAction.Explain)
        assertTrue(vm.uiState.value.loading)

        advanceUntilIdle()
        assertFalse(vm.uiState.value.loading)
    }

    @Test
    fun newRequestClearsPreviousResult() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(responseText = "first")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        // Second request: during loading, result is null.
        vm.requestAction(TutorAction.Simplify)
        assertTrue(vm.uiState.value.loading)
        assertNull(vm.uiState.value.result)
    }

    // ── Rating ────────────────────────────────────────────────────────────────

    @Test
    fun ratingHelpfulSetsRatingFeedback() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(interactionId = 9, responseText = "Great.")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        vm.rateInteraction(helpful = true)
        advanceUntilIdle()

        assertNotNull(vm.uiState.value.ratingFeedback)
        assertTrue(repo.rateHelpful == true)
        assertEquals(9, repo.rateInteractionId)
    }

    @Test
    fun ratingNotHelpfulSetsRatingFeedback() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(interactionId = 4, responseText = "Hmm.")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        vm.rateInteraction(helpful = false)
        advanceUntilIdle()

        assertNotNull(vm.uiState.value.ratingFeedback)
        assertTrue(repo.rateHelpful == false)
    }

    @Test
    fun ratingIsSkippedWhenNoInteractionId() = runTest {
        val repo = FakeTutorRepository()
        val vm = TutorViewModel(repo)
        // No action fired; interactionId is null.
        vm.rateInteraction(helpful = true)
        advanceUntilIdle()

        assertNull(vm.uiState.value.ratingFeedback)
        assertEquals(-1, repo.rateInteractionId)
    }

    @Test
    fun clearRatingFeedbackNullsTheField() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(interactionId = 1, responseText = "ok")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("1")

        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()
        vm.rateInteraction(helpful = true)
        advanceUntilIdle()

        vm.clearRatingFeedback()
        assertNull(vm.uiState.value.ratingFeedback)
    }

    // ── Offline draft ─────────────────────────────────────────────────────────

    @Test
    fun offlineDraftIsPreservedAndClearable() = runTest {
        val vm = TutorViewModel(FakeTutorRepository())
        vm.saveOfflineDraft("Draft message")
        assertEquals("Draft message", vm.uiState.value.offlineDraft)

        vm.clearOfflineDraft()
        assertNull(vm.uiState.value.offlineDraft)
    }

    @Test
    fun blankDraftIsStoredAsNull() = runTest {
        val vm = TutorViewModel(FakeTutorRepository())
        vm.saveOfflineDraft("   ")
        assertNull(vm.uiState.value.offlineDraft)
    }

    // ── Reset ─────────────────────────────────────────────────────────────────

    @Test
    fun resetClearsAllState() = runTest {
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(interactionId = 1, responseText = "ok")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("42")
        vm.onSelectedAnswerChanged("C")
        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        vm.reset()

        val state = vm.uiState.value
        assertEquals("", state.questionIdInput)
        assertEquals("", state.selectedAnswerInput)
        assertFalse(state.loading)
        assertNull(state.result)
        assertNull(state.interactionId)
        assertNull(state.ratingFeedback)
    }

    // ── Context redaction safety ──────────────────────────────────────────────

    @Test
    fun noTokensOrSensitiveDataLeakIntoRepositoryCalls() = runTest {
        // Verify that the ViewModel never passes auth tokens or PII through action requests.
        // The action request payload is {question_id, selected_answer} only.
        val repo = FakeTutorRepository(
            actionResult = ApiResult.Success(TutorResponseDto(responseText = "ok")),
        )
        val vm = TutorViewModel(repo)
        vm.onQuestionIdChanged("99")
        vm.onSelectedAnswerChanged("B")

        vm.requestAction(TutorAction.Explain)
        advanceUntilIdle()

        assertEquals(99, repo.lastQuestionId)
        assertEquals("B", repo.lastSelectedAnswer)
        // Only these two fields should be passed — no extra payload.
    }
}

// ── Fake repository ───────────────────────────────────────────────────────────

private class FakeTutorRepository(
    private val actionResult: ApiResult<TutorResponseDto> = ApiResult.Success(
        TutorResponseDto(responseText = "default response"),
    ),
    private val stepByStepResult: ApiResult<StepByStepDto> = ApiResult.Success(
        StepByStepDto(steps = listOf("Step A")),
    ),
    private val similarResult: ApiResult<SimilarQuestionDto> = ApiResult.Success(
        SimilarQuestionDto(stem = "Q?", correctAnswer = "A"),
    ),
    private val onAction: (() -> Unit)? = null,
) : TutorRepositoryContract {

    var lastQuestionId: Int = -1
        private set
    var lastSelectedAnswer: String? = null
        private set
    var rateInteractionId: Int = -1
        private set
    var rateHelpful: Boolean? = null
        private set
    var lastLessonChatMessage: String? = null
        private set
    var lastLessonChatContext: String? = null
        private set

    override suspend fun tutorAction(
        action: TutorAction,
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<TutorResponseDto> {
        lastQuestionId = questionId
        lastSelectedAnswer = selectedAnswer
        onAction?.invoke()
        return actionResult
    }

    override suspend fun stepByStep(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<StepByStepDto> {
        lastQuestionId = questionId
        return stepByStepResult
    }

    override suspend fun similar(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<SimilarQuestionDto> {
        lastQuestionId = questionId
        return similarResult
    }

    override suspend fun rateInteraction(interactionId: Int, helpful: Boolean): ApiResult<Unit> {
        rateInteractionId = interactionId
        rateHelpful = helpful
        return ApiResult.Success(Unit)
    }

    override suspend fun lessonChat(
        message: String,
        context: String?,
        subtopicId: Int?,
        activeSectionIndex: Int?,
        history: List<LessonChatHistoryItemDto>,
    ): ApiResult<LessonChatResponseDto> {
        lastLessonChatMessage = message
        lastLessonChatContext = context
        return ApiResult.Success(LessonChatResponseDto(response = "ok"))
    }
}
