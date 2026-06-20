package com.csnexus.app.feature.flashcards.data

import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.core.sync.FlashcardResponseSyncPayload
import com.csnexus.app.core.sync.OfflineSyncProcessor
import com.csnexus.app.core.sync.OfflineSyncScheduler
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.SyncBannerState
import com.csnexus.app.core.sync.SyncEventType
import com.csnexus.app.core.sync.SyncFeature
import java.io.IOException
import java.time.Instant
import java.util.UUID
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.withContext

class FlashcardRepository(
    private val flashcardApi: FlashcardApi,
    private val syncStore: FlashcardSyncStore = InMemoryFlashcardSyncStore(),
    private val cacheStore: FlashcardCacheStore? = null,
    private val offlineSyncStore: OfflineSyncStore? = null,
    private val syncScheduler: OfflineSyncScheduler? = null,
    private val syncProcessor: OfflineSyncProcessor? = null,
) {
    fun syncBanner(): Flow<SyncBannerState?>? = offlineSyncStore?.observe(SyncFeature.Flashcards)

    suspend fun decks(): ApiResult<List<DeckDto>> {
        return when (val result = safeApiCall { flashcardApi.decks() }) {
            is ApiResult.Success -> {
                withContext(Dispatchers.Default) {
                    cacheStore?.put(KEY_DECKS, result.value)
                }
                result
            }
            is ApiResult.Failure -> {
                withContext(Dispatchers.Default) {
                    cacheStore?.get<List<DeckDto>>(KEY_DECKS)?.let { ApiResult.Success(it.value) }
                } ?: result
            }
        }
    }

    suspend fun queueSummary(): ApiResult<QueueSummaryDto> {
        return when (val result = safeApiCall { flashcardApi.queueSummary() }) {
            is ApiResult.Success -> {
                withContext(Dispatchers.Default) {
                    cacheStore?.put(KEY_QUEUE_SUMMARY, result.value)
                }
                result
            }
            is ApiResult.Failure -> {
                withContext(Dispatchers.Default) {
                    cacheStore?.get<QueueSummaryDto>(KEY_QUEUE_SUMMARY)?.let { ApiResult.Success(it.value) }
                } ?: result
            }
        }
    }

    suspend fun queue(): ApiResult<List<QueueCardDto>> = safeApiCall { flashcardApi.queue() }

    suspend fun deck(deckId: Int): ApiResult<DeckDto> = safeApiCall { flashcardApi.deck(deckId) }

    suspend fun createDeck(request: DeckCreateRequestDto): ApiResult<DeckDto> = safeApiCall {
        flashcardApi.createDeck(request)
    }

    suspend fun updateDeck(deckId: Int, request: DeckUpdateRequestDto): ApiResult<DeckDto> = safeApiCall {
        flashcardApi.updateDeck(deckId, request)
    }

    suspend fun deleteDeck(deckId: Int): ApiResult<Unit> = safeApiCall {
        flashcardApi.deleteDeck(deckId)
    }

    suspend fun duplicateDeck(deckId: Int): ApiResult<DeckDto> = safeApiCall {
        flashcardApi.duplicateDeck(deckId)
    }

    suspend fun deckCards(deckId: Int): ApiResult<List<FlashcardDto>> = safeApiCall {
        flashcardApi.deckCards(deckId)
    }

    suspend fun createCard(deckId: Int, request: CardCreateRequestDto): ApiResult<FlashcardDto> = safeApiCall {
        flashcardApi.createCard(deckId, request)
    }

    suspend fun updateCard(
        deckId: Int,
        cardId: Int,
        request: CardUpdateRequestDto,
    ): ApiResult<FlashcardDto> = safeApiCall {
        flashcardApi.updateCard(deckId, cardId, request)
    }

    suspend fun deleteCard(deckId: Int, cardId: Int): ApiResult<Unit> = safeApiCall {
        flashcardApi.deleteCard(deckId, cardId)
    }

    suspend fun createSession(
        deckIds: List<Int>,
        studyMode: FlashcardStudyMode,
    ): ApiResult<FlashcardStudySessionDto> = safeApiCall {
        flashcardApi.createSession(
            SessionCreateRequestDto(
                deckIds = deckIds,
                studyMode = studyMode,
            ),
        )
    }

    suspend fun sessionCards(sessionId: Int): ApiResult<List<SessionCardDto>> = safeApiCall {
        flashcardApi.sessionCards(sessionId)
    }

    suspend fun respondToCard(
        sessionId: Int,
        cardId: Int,
        responseType: ResponseType,
        confidence: ConfidenceLevel,
    ): ApiResult<FlashcardResponseResult> {
        val request = SessionResponseRequestDto(
            cardId = cardId,
            responseType = responseType,
            confidence = confidence,
        )
        return try {
            flashcardApi.respondToCard(sessionId, request)
            ApiResult.Success(FlashcardResponseResult.Synced)
        } catch (error: IOException) {
            if (offlineSyncStore != null) {
                offlineSyncStore.enqueue(
                    SyncEventType.FlashcardResponse,
                    FlashcardResponseSyncPayload(
                        sessionId = sessionId,
                        cardId = cardId,
                        responseType = responseType,
                        confidence = confidence,
                    ),
                )
                syncScheduler?.schedule()
                ApiResult.Success(
                    FlashcardResponseResult.QueuedOffline(
                        offlineSyncStore.pendingCount(SyncFeature.Flashcards),
                    ),
                )
            } else {
                syncStore.enqueue(
                    PendingFlashcardStudyEvent(
                        eventId = UUID.randomUUID().toString(),
                        sessionId = sessionId,
                        cardId = cardId,
                        responseType = responseType,
                        confidence = confidence,
                        queuedAt = Instant.now().toString(),
                    ),
                )
                ApiResult.Success(FlashcardResponseResult.QueuedOffline(syncStore.pendingEvents().size))
            }
        } catch (error: RuntimeException) {
            ApiResult.Failure(AppError.Unknown(error.message ?: "Something went wrong."))
        }
    }

    suspend fun endSession(sessionId: Int): ApiResult<SessionSummaryDto> = safeApiCall {
        flashcardApi.endSession(sessionId)
    }

    suspend fun pendingSyncCount(): Int {
        return offlineSyncStore?.pendingCount(SyncFeature.Flashcards) ?: syncStore.pendingEvents().size
    }

    suspend fun syncPendingResponses(): ApiResult<Int> {
        if (syncProcessor != null) {
            syncScheduler?.schedule()
            val summary = syncProcessor.process(SyncFeature.Flashcards)
            return ApiResult.Success(summary.synced)
        }
        val pending = syncStore.pendingEvents()
        if (pending.isEmpty()) return ApiResult.Success(0)

        val remaining = mutableListOf<PendingFlashcardStudyEvent>()
        var synced = 0

        pending.forEach { event ->
            when (
                val result = safeApiCall {
                    flashcardApi.respondToCard(
                        sessionId = event.sessionId,
                        request = SessionResponseRequestDto(
                            cardId = event.cardId,
                            responseType = event.responseType,
                            confidence = event.confidence,
                        ),
                    )
                }
            ) {
                is ApiResult.Success -> synced += 1
                is ApiResult.Failure -> {
                    remaining += event
                    if (result.error is AppError.Network) {
                        syncStore.save(remaining + pending.drop(synced + remaining.size))
                        return result
                    }
                }
            }
        }

        syncStore.save(remaining)
        return ApiResult.Success(synced)
    }

    suspend fun marketplace(
        search: String? = null,
        category: DeckCategory? = null,
        sort: MarketplaceSort = MarketplaceSort.Popular,
    ): ApiResult<List<MarketplaceDeckDto>> = safeApiCall {
        flashcardApi.marketplace(
            search = search?.takeIf { it.isNotBlank() },
            category = category?.name?.lowercase(),
            sort = sort.wireValue,
        )
    }

    suspend fun cloneDeck(deckId: Int): ApiResult<DeckDto> = safeApiCall { flashcardApi.cloneDeck(deckId) }

    suspend fun rateDeck(deckId: Int, score: Int, comment: String? = null): ApiResult<Unit> = safeApiCall {
        flashcardApi.rateDeck(deckId, DeckRatingRequestDto(score = score, comment = comment))
    }

    suspend fun comments(deckId: Int): ApiResult<List<DeckCommentDto>> = safeApiCall { flashcardApi.comments(deckId) }

    suspend fun postComment(
        deckId: Int,
        body: String,
        parentCommentId: Int? = null,
    ): ApiResult<CommentCreatedDto> = safeApiCall {
        flashcardApi.postComment(deckId, DeckCommentCreateRequestDto(body = body, parentCommentId = parentCommentId))
    }

    suspend fun deleteComment(commentId: Int): ApiResult<Unit> = safeApiCall {
        flashcardApi.deleteComment(commentId)
    }

    suspend fun bookmarkDeck(deckId: Int): ApiResult<Unit> = safeApiCall { flashcardApi.bookmarkDeck(deckId) }

    suspend fun unbookmarkDeck(deckId: Int): ApiResult<Unit> = safeApiCall { flashcardApi.unbookmarkDeck(deckId) }

    suspend fun analyticsDashboard(): ApiResult<AnalyticsDashboardDto> = safeApiCall {
        flashcardApi.analyticsDashboard()
    }

    suspend fun heatmap(): ApiResult<List<HeatmapEntryDto>> = safeApiCall { flashcardApi.heatmap() }

    suspend fun recommendations(): ApiResult<List<FlashcardRecommendationDto>> = safeApiCall {
        flashcardApi.recommendations()
    }

    suspend fun createExam(
        deckIds: List<Int>,
        cardCount: Int,
        timeLimitMinutes: Int,
    ): ApiResult<ExamSimulationDto> = safeApiCall {
        flashcardApi.createExam(
            ExamCreateRequestDto(
                deckIds = deckIds,
                cardCount = cardCount,
                timeLimitMinutes = timeLimitMinutes,
            ),
        )
    }

    suspend fun examCards(examId: Int): ApiResult<List<ExamCardDto>> = safeApiCall {
        flashcardApi.examCards(examId)
    }

    suspend fun answerExamCard(examId: Int, cardId: Int, answer: String): ApiResult<Unit> = safeApiCall {
        flashcardApi.answerExamCard(examId, ExamAnswerRequestDto(cardId = cardId, answer = answer))
    }

    suspend fun completeExam(examId: Int): ApiResult<ExamResultDto> = safeApiCall {
        flashcardApi.completeExam(examId)
    }

    suspend fun feed(): ApiResult<List<DeckDto>> = safeApiCall { flashcardApi.feed() }

    suspend fun adminAnalytics(): ApiResult<FlashcardAdminAnalyticsDto> = safeApiCall {
        flashcardApi.adminAnalytics()
    }

    suspend fun flagDeck(deckId: Int): ApiResult<Unit> = safeApiCall { flashcardApi.flagDeck(deckId) }

    suspend fun featureDeck(deckId: Int): ApiResult<Unit> = safeApiCall { flashcardApi.featureDeck(deckId) }

    suspend fun generateCards(
        lessonContent: String,
        lessonId: Int,
        requestedCardCount: Int,
    ): ApiResult<GenerateCardsResponseDto> = safeApiCall {
        flashcardApi.generateCards(
            GenerateCardsRequestDto(
                lessonContent = lessonContent,
                lessonId = lessonId,
                requestedCardCount = requestedCardCount,
            ),
        )
    }
}

sealed interface FlashcardResponseResult {
    data object Synced : FlashcardResponseResult
    data class QueuedOffline(val pendingCount: Int) : FlashcardResponseResult
}

enum class MarketplaceSort(val wireValue: String, val label: String) {
    Popular("popular", "Most Popular"),
    Rating("rating", "Highest Rated"),
    Newest("newest", "Newest"),
}

private class InMemoryFlashcardSyncStore : FlashcardSyncStore {
    private var events: List<PendingFlashcardStudyEvent> = emptyList()

    override fun pendingEvents(): List<PendingFlashcardStudyEvent> = events

    override fun save(events: List<PendingFlashcardStudyEvent>) {
        this.events = events
    }
}

private const val KEY_DECKS = "flashcards:decks"
private const val KEY_QUEUE_SUMMARY = "flashcards:queue_summary"
