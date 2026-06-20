package com.csnexus.app.feature.mockexam.ui

import com.csnexus.app.feature.mockexam.data.MockExamAnswerRequestDto
import com.csnexus.app.feature.mockexam.data.MockExamApi
import com.csnexus.app.feature.mockexam.data.MockExamAttemptDto
import com.csnexus.app.feature.mockexam.data.MockExamFocusLossRequestDto
import com.csnexus.app.feature.mockexam.data.MockExamRepository
import com.csnexus.app.feature.mockexam.data.MockExamSubmitRequestDto
import com.csnexus.app.feature.mockexam.data.MockExamSubmittedDto
import com.csnexus.app.feature.mockexam.data.MockDiagnosticDto
import com.csnexus.app.feature.mockexam.data.MockPredictionDto
import com.csnexus.app.feature.mockexam.data.MockRecommendationDto
import com.csnexus.app.feature.mockexam.data.MockRecommendationsDto
import com.csnexus.app.feature.mockexam.data.MockSubtopicBreakdownDto
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceTimeBy
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runCurrent
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class MockExamViewModelTest {
    private val dispatcher = StandardTestDispatcher()

    @Before
    fun setUp() {
        Dispatchers.setMain(dispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun startExamActivatesAttemptWithServerRemainingTime() = runTest {
        val viewModel = MockExamViewModel(MockExamRepository(FakeMockExamApi()))

        viewModel.startExam()
        runCurrent()

        assertEquals(MockExamPhase.Active, viewModel.uiState.value.phase)
        assertEquals(30, viewModel.uiState.value.remainingSeconds)
        assertEquals("LINEAR_NO_REVISIT", viewModel.uiState.value.attempt?.navPolicy)
    }

    @Test
    fun answerPersistsAndAdvancesWhenLinearNoRevisit() = runTest {
        val api = FakeMockExamApi()
        val viewModel = MockExamViewModel(MockExamRepository(api))

        viewModel.startExam()
        runCurrent()
        viewModel.answer(questionId = 1, selectedAnswer = "A")
        runCurrent()

        assertEquals("A", api.savedAnswer)
        assertEquals(1, viewModel.uiState.value.currentIndex)
        assertEquals("Answer saved.", viewModel.uiState.value.statusMessage)
    }

    @Test
    fun submitMovesToSubmittedPhase() = runTest {
        val viewModel = MockExamViewModel(MockExamRepository(FakeMockExamApi()))

        viewModel.startExam()
        runCurrent()
        viewModel.submitExam()
        runCurrent()

        assertEquals(MockExamPhase.Submitted, viewModel.uiState.value.phase)
        assertEquals(42, viewModel.uiState.value.result?.score)
        assertEquals(84.0, viewModel.uiState.value.review?.diagnostic?.totalScore)
    }

    @Test
    fun timerTicksDownWhileExamIsActive() = runTest {
        val viewModel = MockExamViewModel(MockExamRepository(FakeMockExamApi()))

        viewModel.startExam()
        runCurrent()
        advanceTimeBy(2_000)
        runCurrent()

        assertEquals(28, viewModel.uiState.value.remainingSeconds)
    }
}

private class FakeMockExamApi : MockExamApi {
    var savedAnswer: String? = null

    override suspend fun start(): MockExamAttemptDto = attempt(10)

    override suspend fun attempt(attemptId: Int): MockExamAttemptDto = MockExamAttemptDto(
        attemptId = attemptId,
        status = "IN_PROGRESS",
        remainingSeconds = 30,
        navPolicy = "LINEAR_NO_REVISIT",
        questions = listOf(
            QuizQuestionDto(
                id = 1,
                ordinal = 1,
                stem = "First question",
                options = listOf("A", "B"),
            ),
            QuizQuestionDto(
                id = 2,
                ordinal = 2,
                stem = "Second question",
                options = listOf("C", "D"),
            ),
        ),
    )

    override suspend fun answer(
        attemptId: Int,
        questionId: Int,
        request: MockExamAnswerRequestDto,
    ) {
        savedAnswer = request.selected
    }

    override suspend fun reportFocusLoss(
        attemptId: Int,
        request: MockExamFocusLossRequestDto,
    ) = Unit

    override suspend fun submit(
        attemptId: Int,
        request: MockExamSubmitRequestDto,
    ): MockExamSubmittedDto = MockExamSubmittedDto(
        attemptId = attemptId,
        score = 42,
        maxScore = 50,
        percentage = 0.84,
        passed = true,
    )

    override suspend fun diagnostic(attemptId: Int): MockDiagnosticDto = MockDiagnosticDto(
        totalScore = 84.0,
        highestImpactAreas = listOf(
            MockSubtopicBreakdownDto(
                subtopicId = 3,
                subtopicName = "Verbal",
                questionsAttempted = 10,
                questionsCorrect = 7,
                accuracyPercentage = 70.0,
                pointsLost = 3,
            ),
        ),
    )

    override suspend fun recommendations(attemptId: Int): MockRecommendationsDto = MockRecommendationsDto(
        recommendations = listOf(
            MockRecommendationDto(
                id = 7,
                subtopicName = "Verbal",
                formattedString = "Review Verbal to gain +3 points",
                estimatedPointGain = 3.0,
            ),
        ),
    )

    override suspend fun acceptRecommendation(attemptId: Int): MockRecommendationDto = MockRecommendationDto(id = 7)

    override suspend fun prediction(): MockPredictionDto = MockPredictionDto(
        lowerBound = 80.0,
        midpoint = 84.0,
        upperBound = 88.0,
        confidenceLevel = "high",
    )
}
