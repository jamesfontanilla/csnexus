package com.csnexus.app.feature.mockexam.ui

import androidx.activity.ComponentActivity
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.csnexus.app.core.design.CSNexusTheme
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
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import org.junit.Rule
import org.junit.Test

class MockExamScreenTest {
    @get:Rule
    val composeRule = createAndroidComposeRule<ComponentActivity>()

    @Test
    fun activeMockExamShowsExitConfirmationAndResults() {
        composeRule.setContent {
            CSNexusTheme {
                MockExamScreen(
                    repository = MockExamRepository(TestMockExamApi()),
                    contentPadding = PaddingValues(),
                )
            }
        }

        composeRule.onNodeWithText("Start Mock Exam").performClick()
        composeRule.onNodeWithText("Question 1 of 1").assertIsDisplayed()
        composeRule.activity.onBackPressedDispatcher.onBackPressed()
        composeRule.onNodeWithText("Leave mock exam?").assertIsDisplayed()
        composeRule.onNodeWithText("Stay").performClick()
        composeRule.onNodeWithText("A").performClick()
        composeRule.onNodeWithText("Submit Exam").performClick()
        composeRule.onNodeWithText("Submit").performClick()
        composeRule.onNodeWithText("Mock Exam Results").assertIsDisplayed()
    }
}

private class TestMockExamApi : MockExamApi {
    override suspend fun start(): MockExamAttemptDto = attempt(1)

    override suspend fun attempt(attemptId: Int): MockExamAttemptDto = MockExamAttemptDto(
        attemptId = attemptId,
        remainingSeconds = 120,
        navPolicy = "FREE_NAVIGATION",
        questions = listOf(
            QuizQuestionDto(
                id = 1,
                ordinal = 1,
                stem = "Mock question",
                options = listOf("A", "B"),
            ),
        ),
    )

    override suspend fun answer(attemptId: Int, questionId: Int, request: MockExamAnswerRequestDto) = Unit

    override suspend fun reportFocusLoss(attemptId: Int, request: MockExamFocusLossRequestDto) = Unit

    override suspend fun submit(attemptId: Int, request: MockExamSubmitRequestDto): MockExamSubmittedDto =
        MockExamSubmittedDto(
            attemptId = attemptId,
            score = 1,
            maxScore = 1,
            percentage = 1.0,
            passed = true,
        )

    override suspend fun diagnostic(attemptId: Int): MockDiagnosticDto = MockDiagnosticDto(totalScore = 100.0)

    override suspend fun recommendations(attemptId: Int): MockRecommendationsDto = MockRecommendationsDto(
        recommendations = listOf(MockRecommendationDto(id = 1, formattedString = "Keep going")),
    )

    override suspend fun acceptRecommendation(attemptId: Int): MockRecommendationDto = MockRecommendationDto(id = 1)

    override suspend fun prediction(): MockPredictionDto = MockPredictionDto(midpoint = 90.0)
}
