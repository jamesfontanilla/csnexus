package com.csnexus.app.feature.quizzes.ui

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.csnexus.app.core.design.CSNexusTheme
import com.csnexus.app.feature.quizzes.data.QuizApi
import com.csnexus.app.feature.quizzes.data.QuizAnswerRequestDto
import com.csnexus.app.feature.quizzes.data.QuizAttemptDto
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import com.csnexus.app.feature.quizzes.data.QuizRepository
import com.csnexus.app.feature.quizzes.data.QuizStartRequestDto
import com.csnexus.app.feature.quizzes.data.QuizSubmitRequestDto
import com.csnexus.app.feature.quizzes.data.QuizSubmittedDto
import org.junit.Rule
import org.junit.Test

class QuizScreenTest {
    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun quizScreenShowsModeSelectionAndStartsAttempt() {
        composeRule.setContent {
            CSNexusTheme {
                QuizScreen(
                    repository = QuizRepository(NoopQuizApi()),
                    contentPadding = PaddingValues(),
                )
            }
        }

        composeRule.onNodeWithText("Choose Your Mode").assertIsDisplayed()
        composeRule.onNodeWithText("Practice Mode").assertIsDisplayed()
        composeRule.onNodeWithText("Practice Mode").performClick()
        composeRule.waitUntil(5_000) {
            composeRule.onAllNodesWithText("Question 1 of 1").fetchSemanticsNodes().isNotEmpty()
        }
        composeRule.onNodeWithText("Native question?").assertIsDisplayed()
        composeRule.onNodeWithText("Yes").performClick()
        composeRule.onNodeWithText("Selected: Yes").assertIsDisplayed()
    }

    @Test
    fun quizScreenSubmitsAndShowsReview() {
        composeRule.setContent {
            CSNexusTheme {
                QuizScreen(
                    repository = QuizRepository(NoopQuizApi()),
                    contentPadding = PaddingValues(),
                )
            }
        }

        composeRule.onNodeWithText("Practice Mode").performClick()
        composeRule.waitUntil(5_000) {
            composeRule.onAllNodesWithText("Question 1 of 1").fetchSemanticsNodes().isNotEmpty()
        }
        composeRule.onNodeWithText("Yes").performClick()
        composeRule.onNodeWithText("Submit Quiz").performClick()
        composeRule.waitUntil(5_000) {
            composeRule.onAllNodesWithText("Quiz Results").fetchSemanticsNodes().isNotEmpty()
        }
        composeRule.onNodeWithText("Quiz Results").assertIsDisplayed()
        composeRule.onNodeWithText("Correct").assertIsDisplayed()
    }
}

private class NoopQuizApi : QuizApi {
    override suspend fun startModuleQuiz(
        moduleId: Int,
        request: QuizStartRequestDto,
    ): QuizAttemptDto = attempt(1)

    override suspend fun startTopicQuiz(
        topicId: Int,
        request: QuizStartRequestDto,
    ): QuizAttemptDto = attempt(1)

    override suspend fun startSubtopicQuiz(
        subtopicId: Int,
        request: QuizStartRequestDto,
    ): QuizAttemptDto = attempt(1)

    override suspend fun attempt(attemptId: Int): QuizAttemptDto = QuizAttemptDto(
        attemptId = attemptId,
        status = "IN_PROGRESS",
        timeLimitSeconds = 1200,
        questions = listOf(
            QuizQuestionDto(
                id = 10,
                ordinal = 1,
                stem = "Native question?",
                options = listOf("Yes", "No"),
            ),
        ),
    )

    override suspend fun answer(
        attemptId: Int,
        questionId: Int,
        request: QuizAnswerRequestDto,
    ) = Unit

    override suspend fun submit(
        attemptId: Int,
        request: QuizSubmitRequestDto,
    ): QuizSubmittedDto = QuizSubmittedDto(
        attemptId = attemptId,
        score = 1,
        maxScore = 1,
        percentage = 1.0,
        questions = listOf(
            QuizQuestionDto(
                id = 10,
                ordinal = 1,
                stem = "Native question?",
                options = listOf("Yes", "No"),
                selectedAnswer = "Yes",
                isCorrect = true,
                correctAnswer = "Yes",
            ),
        ),
    )
}
