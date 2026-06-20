package com.csnexus.app.core.sync

import android.content.Context
import androidx.work.BackoffPolicy
import androidx.work.Constraints
import androidx.work.CoroutineWorker
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import com.csnexus.app.core.auth.EncryptedTokenStore
import com.csnexus.app.core.auth.SessionManager
import com.csnexus.app.core.config.appConfig
import com.csnexus.app.core.database.SyncEventDao
import com.csnexus.app.core.database.SyncEventEntity
import com.csnexus.app.core.di.AppContainer
import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.logging.AppLogger
import com.csnexus.app.core.logging.NoOpAppLogger
import com.csnexus.app.core.logging.toDiagnosticsContext
import com.csnexus.app.core.network.ApiClientFactory
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.AuthInterceptor
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.feature.content.data.ContentApi
import com.csnexus.app.feature.content.data.LessonCompleteRequestDto
import com.csnexus.app.feature.flashcards.data.ConfidenceLevel
import com.csnexus.app.feature.flashcards.data.FlashcardApi
import com.csnexus.app.feature.flashcards.data.ResponseType
import com.csnexus.app.feature.flashcards.data.SessionResponseRequestDto
import com.csnexus.app.feature.auth.data.AuthApi
import com.csnexus.app.feature.motivation.data.FocusSessionCompleteRequestDto
import com.csnexus.app.feature.motivation.data.MotivationApi
import com.csnexus.app.feature.progress.data.GoalTargetRequestDto
import com.csnexus.app.feature.progress.data.ProgressApi
import com.csnexus.app.feature.settings.data.DailyGoalRequestDto
import com.csnexus.app.feature.settings.data.SettingsApi
import java.security.MessageDigest
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

enum class SyncFeature(val wireValue: String) {
    Lessons("lessons"),
    Flashcards("flashcards"),
    Focus("focus"),
    Goals("goals"),
    Settings("settings"),
}

enum class SyncEventType(val wireValue: String, val endpoint: String, val feature: SyncFeature) {
    LessonCompletion("lesson_completion", "v1/subtopics/{subtopicId}/lesson:complete", SyncFeature.Lessons),
    FlashcardResponse("flashcard_response", "v1/flashcards/sessions/{sessionId}/respond", SyncFeature.Flashcards),
    FocusCompletion("focus_completion", "v1/focus/sessions/{sessionId}:complete", SyncFeature.Focus),
    GoalTargetUpdate("goal_target_update", "v1/goals/me/target", SyncFeature.Goals),
    SettingsDailyGoalUpdate("settings_daily_goal_update", "v1/settings/daily-goal", SyncFeature.Settings),
    ;

    companion object {
        fun from(raw: String): SyncEventType = entries.first { it.wireValue == raw }
    }
}

enum class SyncEventStatus(val wireValue: String) {
    Queued("queued"),
    Syncing("syncing"),
    Synced("synced"),
    Failed("failed"),
    Conflict("conflict"),
    ;

    companion object {
        fun from(raw: String): SyncEventStatus = entries.first { it.wireValue == raw }
    }
}

@Serializable
sealed interface SyncPayload

@Serializable
data class LessonCompletionSyncPayload(
    @SerialName("subtopic_id") val subtopicId: Int,
) : SyncPayload

@Serializable
data class FlashcardResponseSyncPayload(
    @SerialName("session_id") val sessionId: Int,
    @SerialName("card_id") val cardId: Int,
    @SerialName("response_type") val responseType: ResponseType,
    val confidence: ConfidenceLevel,
) : SyncPayload

@Serializable
data class FocusCompletionSyncPayload(
    @SerialName("session_id") val sessionId: Int,
    @SerialName("total_focus_minutes") val totalFocusMinutes: Int,
    val distractions: Int,
) : SyncPayload

@Serializable
data class GoalTargetSyncPayload(
    @SerialName("target_xp") val targetXp: Int,
) : SyncPayload

@Serializable
data class SettingsDailyGoalSyncPayload(
    @SerialName("target_xp") val targetXp: Int,
) : SyncPayload

data class SyncBannerState(
    val feature: SyncFeature,
    val status: SyncEventStatus,
    val pendingCount: Int,
    val message: String,
)

data class SyncProcessSummary(
    val synced: Int = 0,
    val failed: Int = 0,
    val conflicts: Int = 0,
    val remaining: Int = 0,
)

class OfflineSyncStore(
    private val dao: SyncEventDao,
    private val json: Json = Json { ignoreUnknownKeys = true; explicitNulls = false },
) {
    suspend fun enqueue(type: SyncEventType, payload: SyncPayload): SyncEventEntity {
        val payloadJson = encodePayload(type, payload)
        val payloadHash = hashPayload(payloadJson)
        val idempotencyKey = "${type.wireValue}:$payloadHash"
        val now = System.currentTimeMillis()
        val entity = SyncEventEntity(
            id = idempotencyKey,
            feature = type.feature.wireValue,
            eventType = type.wireValue,
            endpoint = type.endpoint,
            payloadJson = payloadJson,
            payloadHash = payloadHash,
            idempotencyKey = idempotencyKey,
            status = SyncEventStatus.Queued.wireValue,
            attemptCount = 0,
            createdAtMillis = now,
            updatedAtMillis = now,
        )
        dao.upsert(entity)
        return entity
    }

    suspend fun pending(): List<SyncEventEntity> = dao.pending()

    suspend fun pending(feature: SyncFeature): List<SyncEventEntity> = dao.pendingByFeature(feature.wireValue)

    suspend fun pendingCount(feature: SyncFeature): Int = pending(feature).size

    suspend fun markStatus(
        event: SyncEventEntity,
        status: SyncEventStatus,
        attemptCount: Int = event.attemptCount,
        lastError: String? = event.lastError,
    ) {
        dao.upsert(
            event.copy(
                status = status.wireValue,
                attemptCount = attemptCount,
                lastError = lastError,
                updatedAtMillis = System.currentTimeMillis(),
                lastAttemptAtMillis = System.currentTimeMillis(),
            ),
        )
    }

    suspend fun delete(id: String) = dao.delete(id)

    fun observe(feature: SyncFeature): Flow<SyncBannerState?> {
        return dao.observeFeature(feature.wireValue).map { events ->
            if (events.isEmpty()) return@map null
            val status = events.firstNotNullOfOrNull { entity ->
                when (SyncEventStatus.from(entity.status)) {
                    SyncEventStatus.Conflict -> SyncEventStatus.Conflict
                    SyncEventStatus.Failed -> SyncEventStatus.Failed
                    SyncEventStatus.Syncing -> SyncEventStatus.Syncing
                    SyncEventStatus.Queued -> SyncEventStatus.Queued
                    SyncEventStatus.Synced -> null
                }
            } ?: SyncEventStatus.Synced
            SyncBannerState(
                feature = feature,
                status = status,
                pendingCount = events.size,
                message = bannerMessage(feature, status, events.size),
            )
        }
    }

    private fun bannerMessage(feature: SyncFeature, status: SyncEventStatus, count: Int): String {
        val noun = when (feature) {
            SyncFeature.Lessons -> "lesson updates"
            SyncFeature.Flashcards -> "flashcard responses"
            SyncFeature.Focus -> "focus sessions"
            SyncFeature.Goals -> "goal changes"
            SyncFeature.Settings -> "settings changes"
        }
        return when (status) {
            SyncEventStatus.Queued -> "Offline. $count $noun queued for sync."
            SyncEventStatus.Syncing -> "Syncing $noun..."
            SyncEventStatus.Synced -> "$noun synced."
            SyncEventStatus.Failed -> "Could not sync $noun yet. Retry when you're online."
            SyncEventStatus.Conflict -> "$noun need attention before they can sync."
        }
    }

    private fun encodePayload(type: SyncEventType, payload: SyncPayload): String {
        return when (type) {
            SyncEventType.LessonCompletion -> json.encodeToString(payload as LessonCompletionSyncPayload)
            SyncEventType.FlashcardResponse -> json.encodeToString(payload as FlashcardResponseSyncPayload)
            SyncEventType.FocusCompletion -> json.encodeToString(payload as FocusCompletionSyncPayload)
            SyncEventType.GoalTargetUpdate -> json.encodeToString(payload as GoalTargetSyncPayload)
            SyncEventType.SettingsDailyGoalUpdate -> json.encodeToString(payload as SettingsDailyGoalSyncPayload)
        }
    }

    fun decodePayload(type: SyncEventType, payloadJson: String): SyncPayload {
        return when (type) {
            SyncEventType.LessonCompletion -> json.decodeFromString<LessonCompletionSyncPayload>(payloadJson)
            SyncEventType.FlashcardResponse -> json.decodeFromString<FlashcardResponseSyncPayload>(payloadJson)
            SyncEventType.FocusCompletion -> json.decodeFromString<FocusCompletionSyncPayload>(payloadJson)
            SyncEventType.GoalTargetUpdate -> json.decodeFromString<GoalTargetSyncPayload>(payloadJson)
            SyncEventType.SettingsDailyGoalUpdate -> json.decodeFromString<SettingsDailyGoalSyncPayload>(payloadJson)
        }
    }

    private fun hashPayload(payloadJson: String): String {
        return MessageDigest.getInstance("SHA-256")
            .digest(payloadJson.toByteArray())
            .joinToString("") { byte -> "%02x".format(byte) }
    }
}

class OfflineSyncProcessor(
    private val store: OfflineSyncStore,
    private val contentApi: ContentApi,
    private val flashcardApi: FlashcardApi,
    private val motivationApi: MotivationApi,
    private val progressApi: ProgressApi,
    private val settingsApi: SettingsApi,
    private val logger: AppLogger = NoOpAppLogger,
) {
    suspend fun process(feature: SyncFeature? = null): SyncProcessSummary {
        val events = feature?.let { store.pending(it) } ?: store.pending()
        var synced = 0
        var failed = 0
        var conflicts = 0

        events.forEach { event ->
            val type = SyncEventType.from(event.eventType)
            store.markStatus(event, SyncEventStatus.Syncing, attemptCount = event.attemptCount + 1, lastError = null)
            logger.syncEvent(
                event = "sync_processing",
                syncEventId = event.id,
                endpoint = event.endpoint,
                message = "Sync event processing started",
            )
            when (val result = processEvent(type, event)) {
                is ApiResult.Success -> {
                    synced += 1
                    logger.syncEvent(
                        event = "sync_success",
                        syncEventId = event.id,
                        endpoint = event.endpoint,
                        message = "Sync event applied",
                    )
                    store.delete(event.id)
                }
                is ApiResult.Failure -> {
                    when (result.error) {
                        is AppError.Http -> {
                            val statusCode = result.error.statusCode
                            if (statusCode == 409 || statusCode == 412) {
                                conflicts += 1
                                logger.log(
                                    level = com.csnexus.app.core.logging.LogLevel.Error,
                                    event = "sync_conflict",
                                    context = result.error.toDiagnosticsContext(
                                        endpoint = event.endpoint,
                                        syncEventId = event.id,
                                    ),
                                    message = result.error.message,
                                )
                                store.markStatus(event, SyncEventStatus.Conflict, attemptCount = event.attemptCount + 1, lastError = result.error.message)
                            } else {
                                failed += 1
                                logger.log(
                                    level = com.csnexus.app.core.logging.LogLevel.Error,
                                    event = "sync_failure",
                                    context = result.error.toDiagnosticsContext(
                                        endpoint = event.endpoint,
                                        syncEventId = event.id,
                                    ),
                                    message = result.error.message,
                                )
                                store.markStatus(event, SyncEventStatus.Failed, attemptCount = event.attemptCount + 1, lastError = result.error.message)
                            }
                        }
                        else -> {
                            failed += 1
                            logger.log(
                                level = com.csnexus.app.core.logging.LogLevel.Error,
                                event = "sync_failure",
                                context = result.error.toDiagnosticsContext(
                                    endpoint = event.endpoint,
                                    syncEventId = event.id,
                                ),
                                message = result.error.toString(),
                            )
                            store.markStatus(event, SyncEventStatus.Failed, attemptCount = event.attemptCount + 1, lastError = result.error.toString())
                        }
                    }
                }
            }
        }

        val remaining = (feature?.let { store.pending(it) } ?: store.pending()).size
        return SyncProcessSummary(synced = synced, failed = failed, conflicts = conflicts, remaining = remaining)
    }

    private suspend fun processEvent(type: SyncEventType, event: SyncEventEntity): ApiResult<Unit> {
        return when (type) {
            SyncEventType.LessonCompletion -> {
                val payload = store.decodePayload(type, event.payloadJson) as LessonCompletionSyncPayload
                val clientEventId = event.idempotencyKey.take(64)
                safeApiCall {
                    contentApi.completeLesson(
                        subtopicId = payload.subtopicId,
                        request = LessonCompleteRequestDto(clientEventId = clientEventId),
                        idempotencyKey = clientEventId,
                    )
                    Unit
                }
            }
            SyncEventType.FlashcardResponse -> {
                val payload = store.decodePayload(type, event.payloadJson) as FlashcardResponseSyncPayload
                safeApiCall {
                    flashcardApi.respondToCard(
                        payload.sessionId,
                        SessionResponseRequestDto(
                            cardId = payload.cardId,
                            responseType = payload.responseType,
                            confidence = payload.confidence,
                        ),
                        event.idempotencyKey,
                    )
                    Unit
                }
            }
            SyncEventType.FocusCompletion -> {
                val payload = store.decodePayload(type, event.payloadJson) as FocusCompletionSyncPayload
                safeApiCall {
                    motivationApi.completeFocusSession(
                        payload.sessionId,
                        FocusSessionCompleteRequestDto(
                            totalFocusMinutes = payload.totalFocusMinutes,
                            distractions = payload.distractions,
                        ),
                        event.idempotencyKey,
                    )
                    Unit
                }
            }
            SyncEventType.GoalTargetUpdate -> {
                val payload = store.decodePayload(type, event.payloadJson) as GoalTargetSyncPayload
                safeApiCall {
                    progressApi.updateGoalTarget(GoalTargetRequestDto(payload.targetXp), event.idempotencyKey)
                    Unit
                }
            }
            SyncEventType.SettingsDailyGoalUpdate -> {
                val payload = store.decodePayload(type, event.payloadJson) as SettingsDailyGoalSyncPayload
                safeApiCall {
                    settingsApi.updateDailyGoal(DailyGoalRequestDto(payload.targetXp), event.idempotencyKey)
                    Unit
                }
            }
        }
    }
}

class OfflineSyncScheduler(
    private val workManager: WorkManager,
) {
    fun schedule() {
        val request = OneTimeWorkRequestBuilder<OfflineSyncWorker>()
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 15, TimeUnit.SECONDS)
            .setConstraints(
                Constraints.Builder()
                    .setRequiredNetworkType(NetworkType.CONNECTED)
                    .build(),
            )
            .build()
        workManager.enqueueUniqueWork(OfflineSyncWorker.WORK_NAME, ExistingWorkPolicy.KEEP, request)
    }
}

class OfflineSyncWorker(
    appContext: Context,
    workerParameters: WorkerParameters,
) : CoroutineWorker(appContext, workerParameters) {
    override suspend fun doWork(): Result {
        val container = AppContainer(applicationContext)
        val summary = container.offlineSyncProcessor.process()
        return when {
            summary.failed > 0 && summary.synced == 0 && summary.conflicts == 0 -> Result.retry()
            else -> Result.success()
        }
    }

    companion object {
        const val WORK_NAME = "offline-sync"
    }
}

fun buildSyncProcessor(
    context: Context,
    dao: SyncEventDao,
    logger: AppLogger = NoOpAppLogger,
): Pair<OfflineSyncStore, OfflineSyncProcessor> {
    val tokenStore = EncryptedTokenStore(context)
    val sessionManager = SessionManager({ tokenStore }, logger)
    val apiFactory = ApiClientFactory(
        baseUrl = appConfig().apiBaseUrl,
        authInterceptor = AuthInterceptor(tokenStore),
        sessionManager = sessionManager,
        logger = logger,
    )
    apiFactory.create(AuthApi::class.java).also(sessionManager::bindAuthApi)
    val store = OfflineSyncStore(dao)
    val processor = OfflineSyncProcessor(
        store = store,
        contentApi = apiFactory.create(ContentApi::class.java),
        flashcardApi = apiFactory.create(FlashcardApi::class.java),
        motivationApi = apiFactory.create(MotivationApi::class.java),
        progressApi = apiFactory.create(ProgressApi::class.java),
        settingsApi = apiFactory.create(SettingsApi::class.java),
        logger = logger,
    )
    return store to processor
}
