package com.csnexus.app.feature.quizzes.ui

import com.csnexus.app.feature.quizzes.data.QuizApi
import com.csnexus.app.feature.quizzes.data.QuizAnswerRequestDto
import com.csnexus.app.feature.quizzes.data.QuizAttemptDto
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import com.csnexus.app.feature.quizzes.data.QuizRepository
import com.csnexus.app.feature.quizzes.data.QuizMode
import com.csnexus.app.feature.quizzes.data.QuizScope
import com.csnexus.app.feature.quizzes.data.QuizStartRequestDto
import com.csnexus.app.feature.quizzes.data.QuizSubmitRequestDto
import com.csnexus.app.feature.quizzes.data.QuizSubmittedDto
import com.csnexus.app.feature.quizzes.data.ActiveQuizStore
import retrofit2.HttpException
import retrofit2.Response
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.ResponseBody.Companion.toResponseBody
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.advanceTimeBy
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class QuizViewModelTest {
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
    fun startQuizStoresAttempt() = runTest {
        val viewModel = QuizViewModel(QuizRepository(FakeQuizApi()), QuizScope.Subtopic, 1)

        viewModel.startQuiz(QuizMode.Practice)
        advanceUntilIdle()

        assertEquals(42, viewModel.uiState.value.attempt?.attemptId)
        assertEquals(QuizPhase.InProgress, viewModel.uiState.value.phase)
        assertEquals("Quiz attempt #42 started.", viewModel.uiState.value.saveMessage)
    }

    @Test
    fun submitStoresResult() = runTest {
        val viewModel = QuizViewModel(QuizRepository(FakeQuizApi()), QuizScope.Subtopic, 1)

        viewModel.startQuiz(QuizMode.Practice)
        advanceUntilIdle()
        viewModel.submit()
        advanceUntilIdle()

        assertEquals(18, viewModel.uiState.value.result?.score)
        assertEquals(QuizPhase.Submitted, viewModel.uiState.value.phase)
        assertEquals("Quiz submitted.", viewModel.uiState.value.saveMessage)
    }

    @Test
    fun restoresActiveAttemptOnInit() = runTest {
        val store = MemoryQuizStore(activeAttemptId = 42)
        val viewModel = QuizViewModel(QuizRepository(FakeQuizApi(), store), QuizScope.Subtopic, 1)

        advanceUntilIdle()

        assertEquals(QuizPhase.InProgress, viewModel.uiState.value.phase)
        assertEquals(42, viewModel.uiState.value.restoredAttemptId)
        assertEquals("Restored quiz attempt #42.", viewModel.uiState.value.saveMessage)
    }

    @Test
    fun lessonBlockedResponseSwitchesPhase() = runTest {
        val viewModel = QuizViewModel(QuizRepository(LessonBlockedQuizApi()), QuizScope.Subtopic, 1)

        viewModel.startQuiz(QuizMode.Practice)
        advanceUntilIdle()

        assertEquals(QuizPhase.LessonBlocked, viewModel.uiState.value.phase)
    }
}

private class FakeQuizApi : QuizApi {
    override suspend fun startModuleQuiz(
        moduleId: Int,
        request: QuizStartRequestDto,
    ): QuizAttemptDto = startSubtopicQuiz(moduleId, request)

    override suspend fun startTopicQuiz(
        topicId: Int,
        request: QuizStartRequestDto,
    ): QuizAttemptDto = startSubtopicQuiz(topicId, request)

    override suspend fun startSubtopicQuiz(
        subtopicId: Int,
        request: QuizStartRequestDto,
    ): QuizAttemptDto = QuizAttemptDto(
        attemptId = 42,
        status = "IN_PROGRESS",
        questions = listOf(
            QuizQuestionDto(
                id = 7,
                ordinal = 1,
                stem = "What is the best answer?",
                options = listOf("A", "B"),
            ),
        ),
    )

    override suspend fun attempt(attemptId: Int): QuizAttemptDto = startSubtopicQuiz(1)

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
        score = 18,
        maxScore = 20,
        percentage = 0.9,
        awardedXp = 50,
    )
}

private class LessonBlockedQuizApi : QuizApi {
    override suspend fun startModuleQuiz(moduleId: Int, request: QuizStartRequestDto): QuizAttemptDto = fail()

    override suspend fun startTopicQuiz(topicId: Int, request: QuizStartRequestDto): QuizAttemptDto = fail()

    override suspend fun startSubtopicQuiz(subtopicId: Int, request: QuizStartRequestDto): QuizAttemptDto = fail()

    override suspend fun attempt(attemptId: Int): QuizAttemptDto = fail()

    override suspend fun answer(attemptId: Int, questionId: Int, request: QuizAnswerRequestDto) = Unit

    override suspend fun submit(
        attemptId: Int,
        request: QuizSubmitRequestDto,
    ): QuizSubmittedDto = QuizSubmittedDto(attemptId = attemptId)

    private fun fail(): Nothing {
        throw HttpException(
            Response.error<Any>(
                409,
                """{"error":{"code":"LESSON_NOT_COMPLETED","message":"lesson_not_completed"}}"""
                    .toResponseBody("application/json".toMediaType()),
            ),
        )
    }
}

private class MemoryQuizStore(
    private var activeAttemptId: Int? = null,
) : ActiveQuizStore {
    override fun activeAttemptId(): Int? = activeAttemptId

    override fun saveActiveAttemptId(attemptId: Int) {
        activeAttemptId = attemptId
    }

    override fun clearActiveAttempt() {
        activeAttemptId = null
    }
}
