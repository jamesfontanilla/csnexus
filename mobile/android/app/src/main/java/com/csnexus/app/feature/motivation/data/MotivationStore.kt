package com.csnexus.app.feature.motivation.data

import android.content.Context
import com.csnexus.app.core.sync.FocusCompletionSyncPayload
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.SyncEventType
import com.csnexus.app.core.sync.SyncFeature
import com.csnexus.app.feature.motivation.ui.FocusTimerSnapshot
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

interface OnboardingStore {
    fun loadDraft(): OnboardingDraft?
    fun saveDraft(draft: OnboardingDraft)
    fun clearDraft()
    fun markSkipped(skipped: Boolean)
    fun isSkipped(): Boolean
    fun markCompleted(completed: Boolean)
    fun isCompleted(): Boolean
}

interface FocusStateStore {
    fun loadState(): FocusTimerSnapshot?
    fun saveState(snapshot: FocusTimerSnapshot)
    fun clearState()
}

interface FocusCompletionQueueStore {
    suspend fun pendingCompletions(): List<PendingFocusCompletion>
    suspend fun enqueue(completion: PendingFocusCompletion)
    suspend fun remove(sessionId: Int)
    suspend fun clear()
}

@Serializable
data class OnboardingDraft(
    val examDate: String = "",
    val examCategory: OnboardingExamCategory = OnboardingExamCategory.Professional,
    val timeBudgetMinutes: Int = 30,
    val currentStep: Int = 0,
)

@Serializable
data class PendingFocusCompletion(
    val sessionId: Int,
    val totalFocusMinutes: Int,
    val distractions: Int,
)

class SharedPreferencesMotivationStore(context: Context) :
    OnboardingStore,
    FocusStateStore,
    FocusCompletionQueueStore {
    private val preferences = context.getSharedPreferences("motivation_state", Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }

    override fun loadDraft(): OnboardingDraft? =
        preferences.getString(KEY_ONBOARDING_DRAFT, null)?.let(::decodeDraft)

    override fun saveDraft(draft: OnboardingDraft) {
        preferences.edit().putString(KEY_ONBOARDING_DRAFT, json.encodeToString(draft)).apply()
    }

    override fun clearDraft() {
        preferences.edit().remove(KEY_ONBOARDING_DRAFT).apply()
    }

    override fun markSkipped(skipped: Boolean) {
        preferences.edit().putBoolean(KEY_ONBOARDING_SKIPPED, skipped).apply()
    }

    override fun isSkipped(): Boolean = preferences.getBoolean(KEY_ONBOARDING_SKIPPED, false)

    override fun markCompleted(completed: Boolean) {
        preferences.edit().putBoolean(KEY_ONBOARDING_COMPLETED, completed).apply()
    }

    override fun isCompleted(): Boolean = preferences.getBoolean(KEY_ONBOARDING_COMPLETED, false)

    override fun loadState(): FocusTimerSnapshot? =
        preferences.getString(KEY_FOCUS_STATE, null)?.let(::decodeFocusState)

    override fun saveState(snapshot: FocusTimerSnapshot) {
        preferences.edit().putString(KEY_FOCUS_STATE, json.encodeToString(snapshot)).apply()
    }

    override fun clearState() {
        preferences.edit().remove(KEY_FOCUS_STATE).apply()
    }

    override suspend fun pendingCompletions(): List<PendingFocusCompletion> =
        preferences.getString(KEY_FOCUS_PENDING, null)?.let(::decodePendingCompletions).orEmpty()

    override suspend fun enqueue(completion: PendingFocusCompletion) {
        val updated = pendingCompletions().filterNot { it.sessionId == completion.sessionId } + completion
        preferences.edit().putString(KEY_FOCUS_PENDING, json.encodeToString(updated)).apply()
    }

    override suspend fun remove(sessionId: Int) {
        val updated = pendingCompletions().filterNot { it.sessionId == sessionId }
        preferences.edit().putString(KEY_FOCUS_PENDING, json.encodeToString(updated)).apply()
    }

    override suspend fun clear() {
        preferences.edit().remove(KEY_FOCUS_PENDING).apply()
    }

    private fun decodeDraft(raw: String): OnboardingDraft? =
        runCatching { json.decodeFromString<OnboardingDraft>(raw) }.getOrNull()

    private fun decodeFocusState(raw: String): FocusTimerSnapshot? =
        runCatching { json.decodeFromString<FocusTimerSnapshot>(raw) }.getOrNull()

    private fun decodePendingCompletions(raw: String): List<PendingFocusCompletion>? =
        runCatching { json.decodeFromString<List<PendingFocusCompletion>>(raw) }.getOrNull()

    private companion object {
        const val KEY_ONBOARDING_DRAFT = "onboarding_draft"
        const val KEY_ONBOARDING_SKIPPED = "onboarding_skipped"
        const val KEY_ONBOARDING_COMPLETED = "onboarding_completed"
        const val KEY_FOCUS_STATE = "focus_state"
        const val KEY_FOCUS_PENDING = "focus_pending"
    }
}

class OfflineSyncFocusQueueStore(
    private val syncStore: OfflineSyncStore,
) : FocusCompletionQueueStore {
    override suspend fun pendingCompletions(): List<PendingFocusCompletion> {
        return syncStore.pending(SyncFeature.Focus).mapNotNull { event ->
            if (event.eventType != SyncEventType.FocusCompletion.wireValue) {
                null
            } else {
                val payload = syncStore.decodePayload(SyncEventType.FocusCompletion, event.payloadJson) as FocusCompletionSyncPayload
                PendingFocusCompletion(
                    sessionId = payload.sessionId,
                    totalFocusMinutes = payload.totalFocusMinutes,
                    distractions = payload.distractions,
                )
            }
        }
    }

    override suspend fun enqueue(completion: PendingFocusCompletion) {
        syncStore.enqueue(
            SyncEventType.FocusCompletion,
            FocusCompletionSyncPayload(
                sessionId = completion.sessionId,
                totalFocusMinutes = completion.totalFocusMinutes,
                distractions = completion.distractions,
            ),
        )
    }

    override suspend fun remove(sessionId: Int) {
        syncStore.pending(SyncFeature.Focus).forEach { event ->
            if (event.eventType == SyncEventType.FocusCompletion.wireValue) {
                val payload = syncStore.decodePayload(SyncEventType.FocusCompletion, event.payloadJson) as FocusCompletionSyncPayload
                if (payload.sessionId == sessionId) {
                    syncStore.delete(event.id)
                }
            }
        }
    }

    override suspend fun clear() {
        syncStore.pending(SyncFeature.Focus).forEach { event ->
            syncStore.delete(event.id)
        }
    }
}
