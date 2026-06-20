package com.csnexus.app.feature.flashcards.data

import android.content.Context
import android.content.SharedPreferences
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

interface FlashcardSyncStore {
    fun pendingEvents(): List<PendingFlashcardStudyEvent>
    fun save(events: List<PendingFlashcardStudyEvent>)

    fun enqueue(event: PendingFlashcardStudyEvent) {
        save(pendingEvents() + event)
    }
}

@Serializable
data class PendingFlashcardStudyEvent(
    val eventId: String,
    val sessionId: Int,
    val cardId: Int,
    val responseType: ResponseType,
    val confidence: ConfidenceLevel,
    val queuedAt: String,
)

class SharedPreferencesFlashcardSyncStore(
    context: Context,
) : FlashcardSyncStore {
    private val preferences: SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }

    override fun pendingEvents(): List<PendingFlashcardStudyEvent> {
        val raw = preferences.getString(KEY_EVENTS, null) ?: return emptyList()
        return runCatching {
            json.decodeFromString<List<PendingFlashcardStudyEvent>>(raw)
        }.getOrDefault(emptyList())
    }

    override fun save(events: List<PendingFlashcardStudyEvent>) {
        preferences.edit().putString(KEY_EVENTS, json.encodeToString(events)).apply()
    }

    private companion object {
        const val PREFS_NAME = "flashcard_sync_store"
        const val KEY_EVENTS = "pending_flashcard_events"
    }
}
