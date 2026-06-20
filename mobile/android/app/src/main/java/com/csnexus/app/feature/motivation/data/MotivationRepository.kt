package com.csnexus.app.feature.motivation.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.core.sync.OfflineSyncProcessor
import com.csnexus.app.core.sync.OfflineSyncScheduler
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.SyncBannerState
import com.csnexus.app.core.sync.SyncFeature
import com.csnexus.app.feature.motivation.ui.FocusTimerSnapshot
import com.csnexus.app.feature.motivation.ui.OnboardingValidationResult
import com.csnexus.app.feature.motivation.ui.validateOnboardingExamDate
import kotlinx.coroutines.flow.Flow

class MotivationRepository(
    private val motivationApi: MotivationApi,
    private val onboardingStore: OnboardingStore,
    private val focusStateStore: FocusStateStore,
    private val focusCompletionQueueStore: FocusCompletionQueueStore,
    private val syncStore: OfflineSyncStore? = null,
    private val syncScheduler: OfflineSyncScheduler? = null,
    private val syncProcessor: OfflineSyncProcessor? = null,
) {
    fun onboardingDraft(): OnboardingDraft? = onboardingStore.loadDraft()

    fun saveOnboardingDraft(draft: OnboardingDraft) {
        onboardingStore.saveDraft(draft)
    }

    fun clearOnboardingDraft() {
        onboardingStore.clearDraft()
    }

    fun isOnboardingSkipped(): Boolean = onboardingStore.isSkipped()

    fun isOnboardingCompleted(): Boolean = onboardingStore.isCompleted()

    fun markOnboardingSkipped(skipped: Boolean) {
        onboardingStore.markSkipped(skipped)
    }

    suspend fun onboardingPlanSummary(): ApiResult<PlanSummaryDto> = safeApiCall { motivationApi.onboardingPlanSummary() }

    suspend fun submitOnboarding(request: OnboardingRequestDto): ApiResult<OnboardingResponseDto> {
        return safeApiCall {
            val result = motivationApi.submitOnboarding(request)
            onboardingStore.clearDraft()
            onboardingStore.markSkipped(false)
            onboardingStore.markCompleted(true)
            result
        }
    }

    suspend fun updateExamDate(examDate: String): ApiResult<ExamDateUpdateResponseDto> = safeApiCall {
        motivationApi.updateExamDate(ExamDateUpdateRequestDto(examDate = examDate))
    }

    fun validateOnboardingDate(examDate: String): OnboardingValidationResult =
        validateOnboardingExamDate(examDate)

    fun loadFocusState(): FocusTimerSnapshot? = focusStateStore.loadState()

    fun saveFocusState(snapshot: FocusTimerSnapshot) {
        focusStateStore.saveState(snapshot)
    }

    fun clearFocusState() {
        focusStateStore.clearState()
    }

    fun focusSyncBanner(): Flow<SyncBannerState?>? = syncStore?.observe(SyncFeature.Focus)

    suspend fun focusStats(): ApiResult<FocusStatsDto> = safeApiCall { motivationApi.focusStats() }

    suspend fun focusWellness(): ApiResult<FocusWellnessDto> = safeApiCall { motivationApi.focusWellness() }

    suspend fun startFocusSession(
        mode: String,
        workMinutes: Int,
        breakMinutes: Int,
    ): ApiResult<FocusSessionDto> = safeApiCall {
        motivationApi.startFocusSession(
            FocusSessionCreateRequestDto(
                mode = mode,
                workMinutes = workMinutes,
                breakMinutes = breakMinutes,
            ),
        )
    }

    suspend fun completeFocusSession(
        sessionId: Int,
        totalFocusMinutes: Int,
        distractions: Int,
    ): ApiResult<Unit> = safeApiCall {
        motivationApi.completeFocusSession(
            sessionId = sessionId,
            request = FocusSessionCompleteRequestDto(
                totalFocusMinutes = totalFocusMinutes,
                distractions = distractions,
            ),
        )
    }

    suspend fun abandonFocusSession(sessionId: Int): ApiResult<Unit> = safeApiCall {
        motivationApi.abandonFocusSession(sessionId)
    }

    fun queuePendingFocusCompletion(sessionId: Int, totalFocusMinutes: Int, distractions: Int) {
        kotlinx.coroutines.runBlocking {
            focusCompletionQueueStore.enqueue(
                PendingFocusCompletion(
                    sessionId = sessionId,
                    totalFocusMinutes = totalFocusMinutes,
                    distractions = distractions,
                ),
            )
        }
        syncScheduler?.schedule()
    }

    suspend fun retryPendingFocusCompletions(): ApiResult<PendingFocusSyncResult> = safeApiCall {
        if (syncProcessor != null) {
            syncScheduler?.schedule()
            val summary = syncProcessor.process(SyncFeature.Focus)
            PendingFocusSyncResult(
                syncedCount = summary.synced,
                remainingCount = summary.remaining,
            )
        } else {
        var synced = 0
        var failed = 0
        focusCompletionQueueStore.pendingCompletions().forEach { pending ->
            when (
                val result = completeFocusSession(
                    sessionId = pending.sessionId,
                    totalFocusMinutes = pending.totalFocusMinutes,
                    distractions = pending.distractions,
                )
            ) {
                is ApiResult.Success -> {
                    focusCompletionQueueStore.remove(pending.sessionId)
                    synced += 1
                }
                is ApiResult.Failure -> failed += 1
            }
        }
        PendingFocusSyncResult(syncedCount = synced, remainingCount = failed)
        }
    }

    suspend fun queue(): ApiResult<DailyQueueDto> = safeApiCall { motivationApi.queue() }

    suspend fun completeQueueItem(itemId: Int): ApiResult<DailyQueueDto> = safeApiCall { motivationApi.completeQueueItem(itemId) }

    suspend fun regenerateQueue(): ApiResult<DailyQueueDto> = safeApiCall { motivationApi.regenerateQueue() }

    suspend fun queuePreferences(): ApiResult<QueuePreferencesDto> = safeApiCall { motivationApi.queuePreferences() }

    suspend fun updateQueuePreferences(timeBudgetMinutes: Int): ApiResult<Pair<QueuePreferencesDto, DailyQueueDto>> = safeApiCall {
        val preferences = motivationApi.updateQueuePreferences(
            QueuePreferencesRequestDto(timeBudgetMinutes = timeBudgetMinutes),
        )
        preferences to motivationApi.queue()
    }

    suspend fun milestones(): ApiResult<MilestonesResponseDto> = safeApiCall { motivationApi.milestones() }

    suspend fun consistency(): ApiResult<ConsistencyDto> = safeApiCall { motivationApi.consistency() }
}

data class PendingFocusSyncResult(
    val syncedCount: Int,
    val remainingCount: Int,
)
