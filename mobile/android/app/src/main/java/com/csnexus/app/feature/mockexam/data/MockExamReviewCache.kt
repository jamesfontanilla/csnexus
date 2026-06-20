package com.csnexus.app.feature.mockexam.data

import android.content.Context
import com.csnexus.app.core.database.FinalizedReviewDao
import com.csnexus.app.core.database.FinalizedReviewEntity
import kotlinx.serialization.Serializable
import kotlinx.serialization.Transient
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

interface MockExamReviewCache {
    suspend fun get(attemptId: Int): MockExamReview?
    suspend fun put(review: MockExamReview)
}

class SharedPreferencesMockExamReviewCache(context: Context) : MockExamReviewCache {
    private val prefs = context.getSharedPreferences("mock_exam_reviews", Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun get(attemptId: Int): MockExamReview? {
        val raw = prefs.getString(key(attemptId), null) ?: return null
        return runCatching {
            json.decodeFromString<MockExamReview>(raw).copy(fromCache = true)
        }.getOrNull()
    }

    override suspend fun put(review: MockExamReview) {
        prefs.edit()
            .putString(key(review.attemptId), json.encodeToString(review.copy(fromCache = false)))
            .apply()
    }

    private fun key(attemptId: Int): String = "review:$attemptId"
}

class RoomMockExamReviewCache(
    private val finalizedReviewDao: FinalizedReviewDao,
    private val json: Json = Json { ignoreUnknownKeys = true },
) : MockExamReviewCache {
    override suspend fun get(attemptId: Int): MockExamReview? {
        return finalizedReviewDao.get(REVIEW_TYPE, attemptId.toString())?.let { entity ->
            runCatching {
                json.decodeFromString<MockExamReview>(entity.payloadJson).copy(fromCache = true)
            }.getOrNull()
        }
    }

    override suspend fun put(review: MockExamReview) {
        finalizedReviewDao.put(
            FinalizedReviewEntity(
                reviewType = REVIEW_TYPE,
                reviewId = review.attemptId.toString(),
                payloadJson = json.encodeToString(review.copy(fromCache = false)),
                cachedAtMillis = System.currentTimeMillis(),
            ),
        )
    }

    private companion object {
        const val REVIEW_TYPE = "mock_exam"
    }
}

@Serializable
data class MockExamReview(
    val attemptId: Int,
    val submitted: MockExamSubmittedDto? = null,
    val diagnostic: MockDiagnosticDto? = null,
    val recommendations: MockRecommendationsDto? = null,
    val prediction: MockPredictionDto? = null,
    @Transient
    val fromCache: Boolean = false,
)
