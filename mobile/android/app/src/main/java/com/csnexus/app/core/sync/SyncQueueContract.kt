package com.csnexus.app.core.sync

/**
 * Offline progress events should only be queued after the backend exposes an
 * idempotent sync endpoint for the event type.
 */
data class PendingSyncEvent(
    val id: String,
    val endpoint: String,
    val payloadJson: String,
    val createdAtEpochMillis: Long,
)
