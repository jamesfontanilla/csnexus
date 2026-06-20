package com.csnexus.app.feature.motivation.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.motivation.ui.FocusTimerSnapshot
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class MotivationRepositoryTest {
    @Test
    fun onboardingDraftPersistsForResumeAndCompletionClearsIt() = runTest {
        val onboardingStore = FakeOnboardingStore()
        val focusStateStore = FakeFocusStateStore()
        val pendingStore = FakePendingFocusStore()
        val api = FakeMotivationApi()
        val repository = MotivationRepository(api, onboardingStore, focusStateStore, pendingStore)
        val draft = OnboardingDraft(examDate = "2026-12-01", timeBudgetMinutes = 60, currentStep = 2)

        repository.saveOnboardingDraft(draft)
        assertEquals(draft, repository.onboardingDraft())
        val result = repository.submitOnboarding(
            OnboardingRequestDto(
                examDate = draft.examDate,
                examCategory = draft.examCategory,
                timeBudgetMinutes = draft.timeBudgetMinutes,
            ),
        )

        assertTrue(result is ApiResult.Success)
        assertEquals(null, onboardingStore.draft)
        assertTrue(onboardingStore.completed)
        assertFalse(onboardingStore.skipped)
    }

    @Test
    fun retryPendingFocusCompletionsRemovesOnlySuccessfulItems() = runTest {
        val pendingStore = FakePendingFocusStore().apply {
            completions = mutableListOf(
                PendingFocusCompletion(sessionId = 1, totalFocusMinutes = 25, distractions = 0),
                PendingFocusCompletion(sessionId = 2, totalFocusMinutes = 50, distractions = 1),
            )
        }
        val api = FakeMotivationApi().apply {
            failingCompletionIds += 2
        }
        val repository = MotivationRepository(api, FakeOnboardingStore(), FakeFocusStateStore(), pendingStore)

        val result = repository.retryPendingFocusCompletions()

        assertTrue(result is ApiResult.Success)
        val summary = (result as ApiResult.Success).value
        assertEquals(1, summary.syncedCount)
        assertEquals(1, summary.remainingCount)
        assertEquals(listOf(2), pendingStore.completions.map { it.sessionId })
    }

    @Test
    fun updateQueuePreferencesReturnsRefreshedQueue() = runTest {
        val api = FakeMotivationApi().apply {
            preferencesResponse = QueuePreferencesDto(timeBudgetMinutes = 60)
            queueResponse = DailyQueueDto(itemsRemaining = 1, itemsCompleted = 2)
        }
        val repository = MotivationRepository(api, FakeOnboardingStore(), FakeFocusStateStore(), FakePendingFocusStore())

        val result = repository.updateQueuePreferences(60)

        assertTrue(result is ApiResult.Success)
        val payload = (result as ApiResult.Success).value
        assertEquals(60, payload.first.timeBudgetMinutes)
        assertEquals(1, payload.second.itemsRemaining)
        assertEquals(60, api.lastUpdatedQueuePreference)
    }
}

private class FakeMotivationApi : MotivationApi {
    var preferencesResponse = QueuePreferencesDto()
    var queueResponse = DailyQueueDto()
    var lastUpdatedQueuePreference: Int? = null
    val failingCompletionIds = mutableSetOf<Int>()

    override suspend fun submitOnboarding(request: OnboardingRequestDto): OnboardingResponseDto = OnboardingResponseDto(confirmation = "ok")
    override suspend fun updateExamDate(request: ExamDateUpdateRequestDto): ExamDateUpdateResponseDto = ExamDateUpdateResponseDto(confirmation = "ok")
    override suspend fun onboardingPlanSummary(): PlanSummaryDto = PlanSummaryDto()
    override suspend fun focusStats(): FocusStatsDto = FocusStatsDto()
    override suspend fun startFocusSession(request: FocusSessionCreateRequestDto): FocusSessionDto = FocusSessionDto(id = 1)
    override suspend fun completeFocusSession(
        sessionId: Int,
        request: FocusSessionCompleteRequestDto,
        idempotencyKey: String?,
    ) {
        if (sessionId in failingCompletionIds) {
            throw java.io.IOException("offline")
        }
    }
    override suspend fun abandonFocusSession(sessionId: Int) = Unit
    override suspend fun focusWellness(): FocusWellnessDto = FocusWellnessDto()
    override suspend fun queue(): DailyQueueDto = queueResponse
    override suspend fun completeQueueItem(itemId: Int): DailyQueueDto = queueResponse
    override suspend fun regenerateQueue(): DailyQueueDto = queueResponse
    override suspend fun queuePreferences(): QueuePreferencesDto = preferencesResponse
    override suspend fun updateQueuePreferences(request: QueuePreferencesRequestDto): QueuePreferencesDto {
        lastUpdatedQueuePreference = request.timeBudgetMinutes
        return preferencesResponse
    }
    override suspend fun milestones(): MilestonesResponseDto = MilestonesResponseDto()
    override suspend fun consistency(): ConsistencyDto = ConsistencyDto()
}

private class FakeOnboardingStore : OnboardingStore {
    var draft: OnboardingDraft? = null
    var skipped: Boolean = false
    var completed: Boolean = false

    override fun loadDraft(): OnboardingDraft? = draft
    override fun saveDraft(draft: OnboardingDraft) {
        this.draft = draft
    }
    override fun clearDraft() {
        draft = null
    }
    override fun markSkipped(skipped: Boolean) {
        this.skipped = skipped
    }
    override fun isSkipped(): Boolean = skipped
    override fun markCompleted(completed: Boolean) {
        this.completed = completed
    }
    override fun isCompleted(): Boolean = completed
}

private class FakeFocusStateStore : FocusStateStore {
    var snapshot: FocusTimerSnapshot? = null

    override fun loadState(): FocusTimerSnapshot? = snapshot
    override fun saveState(snapshot: FocusTimerSnapshot) {
        this.snapshot = snapshot
    }
    override fun clearState() {
        snapshot = null
    }
}

private class FakePendingFocusStore : FocusCompletionQueueStore {
    var completions = mutableListOf<PendingFocusCompletion>()

    override suspend fun pendingCompletions(): List<PendingFocusCompletion> = completions.toList()
    override suspend fun enqueue(completion: PendingFocusCompletion) {
        completions.removeAll { it.sessionId == completion.sessionId }
        completions.add(completion)
    }
    override suspend fun remove(sessionId: Int) {
        completions.removeAll { it.sessionId == sessionId }
    }
    override suspend fun clear() {
        completions.clear()
    }
}
