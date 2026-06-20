package com.csnexus.app.feature.quizzes.data

import com.csnexus.app.core.network.ApiResult
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.IOException

class QuizRepositoryTest {
    @Test
    fun startQuizUsesScopedEndpointAndPersistsActiveAttempt() = runTest {
        val api = RecordingQuizApi()
        val store = MemoryActiveQuizStore()
        val repository = QuizRepository(api, store)

        val result = repository.startQuiz(QuizScope.Topic, scopeId = 42, mode = QuizMode.Power)

        assertTrue(result is ApiResult.Success)
        assertEquals("topic:42", api.startedScope)
        assertEquals(QuizMode.Power.timeLimitSeconds, api.startedRequest?.timeLimitSeconds)
        assertEquals(99, store.activeAttemptId())
    }

    @Test
    fun submitClearsActiveAttempt() = runTest {
        val store = MemoryActiveQuizStore().apply { saveActiveAttemptId(99) }
        val repository = QuizRepository(RecordingQuizApi(), store)

        val result = repository.submit(99)

        assertTrue(result is ApiResult.Success)
        assertEquals(null, store.activeAttemptId())
    }

    @Test
    fun submitRecoversSubmittedAttemptWhenSubmitResponseFails() = runTest {
        val store = MemoryActiveQuizStore().apply { saveActiveAttemptId(99) }
        val repository = QuizRepository(SubmitResponseLostQuizApi(), store)

        val result = repository.submit(99)

        assertTrue(result is ApiResult.Success)
        result as ApiResult.Success
        assertEquals(2, result.value.score)
        assertEquals(3, result.value.maxScore)
        assertEquals(null, store.activeAttemptId())
    }
}

private open class RecordingQuizApi : QuizApi {
    var startedScope: String? = null
    var startedRequest: QuizStartRequestDto? = null

    override suspend fun startModuleQuiz(moduleId: Int, request: QuizStartRequestDto): QuizAttemptDto {
        startedScope = "module:$moduleId"
        startedRequest = request
        return attempt(99)
    }

    override suspend fun startTopicQuiz(topicId: Int, request: QuizStartRequestDto): QuizAttemptDto {
        startedScope = "topic:$topicId"
        startedRequest = request
        return attempt(99)
    }

    override suspend fun startSubtopicQuiz(subtopicId: Int, request: QuizStartRequestDto): QuizAttemptDto {
        startedScope = "subtopic:$subtopicId"
        startedRequest = request
        return attempt(99)
    }

    override open suspend fun attempt(attemptId: Int): QuizAttemptDto = QuizAttemptDto(
        attemptId = attemptId,
        status = "IN_PROGRESS",
        questions = listOf(
            QuizQuestionDto(
                id = 1,
                ordinal = 1,
                stem = "Question",
                options = listOf("A", "B"),
            ),
        ),
    )

    override suspend fun answer(
        attemptId: Int,
        questionId: Int,
        request: QuizAnswerRequestDto,
    ) = Unit

    override open suspend fun submit(
        attemptId: Int,
        request: QuizSubmitRequestDto,
    ): QuizSubmittedDto = QuizSubmittedDto(
        attemptId = attemptId,
        score = 1,
        maxScore = 1,
        percentage = 1.0,
    )
}

private class SubmitResponseLostQuizApi : RecordingQuizApi() {
    override suspend fun attempt(attemptId: Int): QuizAttemptDto = QuizAttemptDto(
        attemptId = attemptId,
        status = "SUBMITTED",
        score = 2,
        maxScore = 3,
        percentage = 0.66,
        isPassing = false,
        isPerfect = false,
        awardedXp = 0,
        questions = listOf(
            QuizQuestionDto(
                id = 1,
                ordinal = 1,
                stem = "Question",
                options = listOf("A", "B"),
                selectedAnswer = "A",
                correctAnswer = "B",
                isCorrect = false,
            ),
        ),
    )

    override suspend fun submit(
        attemptId: Int,
        request: QuizSubmitRequestDto,
    ): QuizSubmittedDto {
        throw IOException("closed")
    }
}

private class MemoryActiveQuizStore : ActiveQuizStore {
    private var attemptId: Int? = null

    override fun activeAttemptId(): Int? = attemptId

    override fun saveActiveAttemptId(attemptId: Int) {
        this.attemptId = attemptId
    }

    override fun clearActiveAttempt() {
        attemptId = null
    }
}
