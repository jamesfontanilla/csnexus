package com.csnexus.app.feature.content.data

import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.core.sync.LessonCompletionSyncPayload
import com.csnexus.app.core.sync.OfflineSyncScheduler
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.SyncBannerState
import com.csnexus.app.core.sync.SyncEventType
import com.csnexus.app.core.sync.SyncFeature
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.Lesson
import com.csnexus.app.feature.content.domain.LessonCompletion
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.withContext
import java.util.UUID

data class ContentResult<T>(
    val value: T,
    val fromCache: Boolean = false,
    val cachedAtMillis: Long? = null,
)

class ContentRepository(
    private val contentApi: ContentApi,
    private val lessonCache: LessonCache,
    private val syncStore: OfflineSyncStore? = null,
    private val syncScheduler: OfflineSyncScheduler? = null,
) {
    fun lessonSyncBanner(): Flow<SyncBannerState?>? = syncStore?.observe(SyncFeature.Lessons)

    suspend fun retryLessonSync(): ApiResult<Int> {
        val store = syncStore ?: return ApiResult.Success(0)
        syncScheduler?.schedule()
        return ApiResult.Success(store.pendingCount(SyncFeature.Lessons))
    }

    suspend fun modules(): ApiResult<ContentResult<List<LearningModule>>> {
        return when (val result = safeApiCall { contentApi.modules() }) {
            is ApiResult.Success -> {
                val modules = withContext(Dispatchers.Default) {
                    result.value.items.map { it.toDomain() }
                }
                lessonCache.putModules(modules)
                ApiResult.Success(ContentResult(modules))
            }
            is ApiResult.Failure -> {
                val cached = lessonCache.modules()
                if (cached != null) {
                    ApiResult.Success(
                        ContentResult(
                            value = cached.value,
                            fromCache = true,
                            cachedAtMillis = cached.cachedAtMillis,
                        ),
                    )
                } else {
                    result
                }
            }
        }
    }

    suspend fun lesson(subtopicId: Int): ApiResult<ContentResult<Lesson>> {
        return when (val result = safeApiCall { contentApi.lesson(subtopicId) }) {
            is ApiResult.Success -> {
                val lesson = withContext(Dispatchers.Default) {
                    result.value.toDomain()
                }
                lessonCache.put(lesson)
                ApiResult.Success(ContentResult(lesson))
            }
            is ApiResult.Failure -> {
                val cached = lessonCache.get(subtopicId)
                if (cached != null) ApiResult.Success(ContentResult(cached, fromCache = true)) else result
            }
        }
    }

    suspend fun topics(moduleId: Int): ApiResult<ContentResult<List<LearningTopic>>> {
        return when (val result = safeApiCall { contentApi.topics(moduleId) }) {
            is ApiResult.Success -> {
                val topics = withContext(Dispatchers.Default) {
                    result.value.map { it.toDomain() }
                }
                lessonCache.putTopics(moduleId, topics)
                ApiResult.Success(ContentResult(topics))
            }
            is ApiResult.Failure -> {
                val cached = lessonCache.topics(moduleId)
                if (cached != null) {
                    ApiResult.Success(ContentResult(cached.value, fromCache = true, cachedAtMillis = cached.cachedAtMillis))
                } else {
                    result
                }
            }
        }
    }

    suspend fun subtopics(topicId: Int): ApiResult<ContentResult<List<LearningSubtopic>>> {
        return when (val result = safeApiCall { contentApi.subtopics(topicId) }) {
            is ApiResult.Success -> {
                val subtopics = withContext(Dispatchers.Default) {
                    result.value.map { it.toDomain() }
                }
                lessonCache.putSubtopics(topicId, subtopics)
                ApiResult.Success(ContentResult(subtopics))
            }
            is ApiResult.Failure -> {
                val cached = lessonCache.subtopics(topicId)
                if (cached != null) {
                    ApiResult.Success(ContentResult(cached.value, fromCache = true, cachedAtMillis = cached.cachedAtMillis))
                } else {
                    result
                }
            }
        }
    }

    suspend fun completeLesson(subtopicId: Int): ApiResult<LessonCompletion> {
        val clientEventId = "lesson:${UUID.randomUUID()}"
        return when (
            val result = safeApiCall {
                contentApi.completeLesson(
                    subtopicId = subtopicId,
                    request = LessonCompleteRequestDto(clientEventId = clientEventId),
                    idempotencyKey = clientEventId,
                )
            }
        ) {
            is ApiResult.Success -> ApiResult.Success(
                LessonCompletion(
                    awardedXp = result.value.awardedXp,
                    alreadyCompleted = result.value.alreadyCompleted,
                ),
            )
            is ApiResult.Failure -> {
                if (result.error is AppError.Network && syncStore != null) {
                    syncStore.enqueue(
                        SyncEventType.LessonCompletion,
                        LessonCompletionSyncPayload(subtopicId = subtopicId),
                    )
                    syncScheduler?.schedule()
                    ApiResult.Success(LessonCompletion(queuedOffline = true))
                } else {
                    result
                }
            }
        }
    }
}
