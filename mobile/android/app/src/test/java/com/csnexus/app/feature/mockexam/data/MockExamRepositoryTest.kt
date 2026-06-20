package com.csnexus.app.feature.mockexam.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class MockExamRepositoryTest {
    @Test
    fun answerAndFocusLossUseMockExamContracts() = runTest {
        val api = RecordingMockExamApi()
        val repository = MockExamRepository(api)

        val answerResult = repository.answer(attemptId = 9, questionId = 4, selectedAnswer = "B")
        val focusResult = repository.reportFocusLoss(attemptId = 9, kind = "app_backgrounded", at = "2026-06-08T00:00:00Z")

        assertTrue(answerResult is ApiResult.Success)
        assertTrue(focusResult is ApiResult.Success)
        assertEquals("9:4:B", api.savedAnswer)
        assertEquals("9:app_backgrounded:2026-06-08T00:00:00Z", api.focusLoss)
    }

    @Test
    fun startAndSubmitMapResponses() = runTest {
        val repository = MockExamRepository(RecordingMockExamApi())

        val started = repository.start()
        val submitted = repository.submit(9)

        assertTrue(started is ApiResult.Success)
        assertEquals(9, (started as ApiResult.Success).value.attemptId)
        assertTrue(submitted is ApiResult.Success)
        assertEquals(40, (submitted as ApiResult.Success).value.score)
    }
}

private class RecordingMockExamApi : MockExamApi {
    var savedAnswer: String? = null
    var focusLoss: String? = null

    override suspend fun start(): MockExamAttemptDto = attempt(9)

    override suspend fun attempt(attemptId: Int): MockExamAttemptDto = MockExamAttemptDto(
        attemptId = attemptId,
        status = "IN_PROGRESS",
        remainingSeconds = 10_800,
        navPolicy = "LINEAR_NO_REVISIT",
        questions = listOf(
            QuizQuestionDto(
                id = 4,
                ordinal = 1,
                stem = "Mock question",
                options = listOf("A", "B"),
            ),
        ),
    )

    override suspend fun answer(
        attemptId: Int,
        questionId: Int,
        request: MockExamAnswerRequestDto,
    ) {
        savedAnswer = "$attemptId:$questionId:${request.selected}"
    }

    override suspend fun reportFocusLoss(
        attemptId: Int,
        request: MockExamFocusLossRequestDto,
    ) {
        focusLoss = "$attemptId:${request.kind}:${request.at}"
    }

    override suspend fun submit(
        attemptId: Int,
        request: MockExamSubmitRequestDto,
    ): MockExamSubmittedDto = MockExamSubmittedDto(
        attemptId = attemptId,
        score = 40,
        maxScore = 50,
        percentage = 0.8,
        passed = true,
    )

    override suspend fun diagnostic(attemptId: Int): MockDiagnosticDto = MockDiagnosticDto(
        totalScore = 80.0,
        subtopicBreakdowns = listOf(
            MockSubtopicBreakdownDto(
                subtopicId = 5,
                subtopicName = "Ratio",
                questionsAttempted = 10,
                questionsCorrect = 8,
                accuracyPercentage = 80.0,
            ),
        ),
    )

    override suspend fun recommendations(attemptId: Int): MockRecommendationsDto = MockRecommendationsDto(
        recommendations = listOf(
            MockRecommendationDto(
                id = 1,
                subtopicName = "Ratio",
                estimatedPointGain = 4.0,
                formattedString = "Fix Ratio to gain +4 points",
            ),
        ),
    )

    override suspend fun acceptRecommendation(attemptId: Int): MockRecommendationDto = MockRecommendationDto(id = 1)

    override suspend fun prediction(): MockPredictionDto = MockPredictionDto(
        lowerBound = 78.0,
        midpoint = 82.0,
        upperBound = 86.0,
        confidenceLevel = "medium",
    )
}
