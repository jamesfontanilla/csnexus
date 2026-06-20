package com.csnexus.app.feature.mockexam.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall

class MockExamRepository(
    private val mockExamApi: MockExamApi,
    private val reviewCache: MockExamReviewCache? = null,
) {
    suspend fun start(): ApiResult<MockExamAttemptDto> = safeApiCall { mockExamApi.start() }

    suspend fun attempt(attemptId: Int): ApiResult<MockExamAttemptDto> =
        safeApiCall { mockExamApi.attempt(attemptId) }

    suspend fun answer(attemptId: Int, questionId: Int, selectedAnswer: String): ApiResult<Unit> =
        safeApiCall {
            mockExamApi.answer(attemptId, questionId, MockExamAnswerRequestDto(selectedAnswer))
            Unit
        }

    suspend fun reportFocusLoss(attemptId: Int, kind: String, at: String): ApiResult<Unit> =
        safeApiCall {
            mockExamApi.reportFocusLoss(attemptId, MockExamFocusLossRequestDto(kind = kind, at = at))
            Unit
        }

    suspend fun submit(attemptId: Int): ApiResult<MockExamSubmittedDto> {
        return when (val result = safeApiCall { mockExamApi.submit(attemptId) }) {
            is ApiResult.Success -> {
                reviewCache?.put(
                    MockExamReview(
                        attemptId = result.value.attemptId.takeIf { it > 0 } ?: attemptId,
                        submitted = result.value,
                    ),
                )
                result
            }
            is ApiResult.Failure -> result
        }
    }

    suspend fun review(attemptId: Int, submitted: MockExamSubmittedDto? = null): ApiResult<MockExamReview> {
        val cached = reviewCache?.get(attemptId)
        val diagnostic = safeApiCall { mockExamApi.diagnostic(attemptId) }
        val recommendations = safeApiCall { mockExamApi.recommendations(attemptId) }
        val prediction = safeApiCall { mockExamApi.prediction() }

        val hasNetworkPayload = diagnostic is ApiResult.Success ||
            recommendations is ApiResult.Success ||
            prediction is ApiResult.Success

        if (!hasNetworkPayload && cached != null) {
            return ApiResult.Success(cached)
        }

        val review = MockExamReview(
            attemptId = attemptId,
            submitted = submitted ?: cached?.submitted,
            diagnostic = (diagnostic as? ApiResult.Success)?.value ?: cached?.diagnostic,
            recommendations = (recommendations as? ApiResult.Success)?.value ?: cached?.recommendations,
            prediction = (prediction as? ApiResult.Success)?.value ?: cached?.prediction,
            fromCache = false,
        )
        reviewCache?.put(review)
        return ApiResult.Success(review)
    }

    suspend fun acceptRecommendation(attemptId: Int): ApiResult<MockRecommendationDto> =
        safeApiCall { mockExamApi.acceptRecommendation(attemptId) }
}
