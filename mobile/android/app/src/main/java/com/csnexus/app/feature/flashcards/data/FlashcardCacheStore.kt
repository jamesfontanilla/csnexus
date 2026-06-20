package com.csnexus.app.feature.flashcards.data

import com.csnexus.app.core.database.FlashcardCacheDao
import com.csnexus.app.core.database.FlashcardCacheEntity
import com.csnexus.app.feature.content.data.CachedContent
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

class FlashcardCacheStore(
    @PublishedApi internal val dao: FlashcardCacheDao,
    @PublishedApi internal val json: Json = Json { ignoreUnknownKeys = true },
) {
    suspend inline fun <reified T> get(key: String): CachedContent<T>? {
        val entity = dao.get(key) ?: return null
        return runCatching {
            CachedContent(
                value = json.decodeFromString<T>(entity.payloadJson),
                cachedAtMillis = entity.cachedAtMillis,
            )
        }.getOrNull()
    }

    suspend inline fun <reified T> put(key: String, value: T) {
        dao.put(
            FlashcardCacheEntity(
                cacheKey = key,
                payloadJson = json.encodeToString(value),
                cachedAtMillis = System.currentTimeMillis(),
            ),
        )
    }
}
