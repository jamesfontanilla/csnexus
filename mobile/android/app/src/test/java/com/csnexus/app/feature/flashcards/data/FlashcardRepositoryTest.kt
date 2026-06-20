package com.csnexus.app.feature.flashcards.data

import com.csnexus.app.core.network.ApiResult
import kotlinx.coroutines.test.runTest
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.IOException

class FlashcardRepositoryTest {
    @Test
    fun deckDecodingAcceptsNullTagsFromBackend() {
        val json = Json { ignoreUnknownKeys = true; explicitNulls = false }

        val deck = json.decodeFromString<DeckDto>(
            """
            {
              "id": 7,
              "title": "Backend Deck",
              "visibility": "private",
              "tags": null,
              "clone_count": 0,
              "bookmark_count": 0
            }
            """.trimIndent(),
        )

        assertEquals(emptyList<String>(), deck.tags.orEmpty())
    }

    @Test
    fun deckCrudAndMarketplaceImportUseNativeContracts() = runTest {
        val api = RecordingFlashcardApi()
        val repository = FlashcardRepository(api, InMemoryStore())

        val created = repository.createDeck(
            DeckCreateRequestDto(
                title = "Grammar",
                category = DeckCategory.Verbal,
                visibility = DeckVisibility.Private,
            ),
        )
        val updated = repository.updateDeck(9, DeckUpdateRequestDto(title = "Grammar Updated"))
        val cloned = repository.cloneDeck(55)
        val deleted = repository.deleteDeck(9)

        assertTrue(created is ApiResult.Success)
        assertTrue(updated is ApiResult.Success)
        assertTrue(cloned is ApiResult.Success)
        assertTrue(deleted is ApiResult.Success)
        assertEquals("Grammar", api.createdDeckTitle)
        assertEquals("Grammar Updated", api.updatedDeckTitle)
        assertEquals(55, api.clonedDeckId)
        assertEquals(9, api.deletedDeckId)
    }

    @Test
    fun offlineStudyResponsesQueueAndRetry() = runTest {
        val api = RecordingFlashcardApi().apply { failStudyResponse = true }
        val store = InMemoryStore()
        val repository = FlashcardRepository(api, store)

        val queued = repository.respondToCard(
            sessionId = 5,
            cardId = 12,
            responseType = ResponseType.Remembered,
            confidence = ConfidenceLevel.Confident,
        )

        assertTrue(queued is ApiResult.Success)
        assertEquals(1, store.pendingEvents().size)

        api.failStudyResponse = false
        val synced = repository.syncPendingResponses()

        assertTrue(synced is ApiResult.Success)
        assertEquals(0, store.pendingEvents().size)
        assertEquals("5:12", api.lastStudyResponse)
    }

    @Test
    fun generationAndAdminAnalyticsMapResponses() = runTest {
        val repository = FlashcardRepository(RecordingFlashcardApi(), InMemoryStore())

        val generated = repository.generateCards("x".repeat(80), lessonId = 0, requestedCardCount = 20)
        val admin = repository.adminAnalytics()

        assertTrue(generated is ApiResult.Success)
        assertTrue(admin is ApiResult.Success)
        assertEquals(2, (generated as ApiResult.Success).value.termsExtracted)
        assertEquals(14, (admin as ApiResult.Success).value.activeReviewers7d)
    }
}

private class InMemoryStore : FlashcardSyncStore {
    private var events: List<PendingFlashcardStudyEvent> = emptyList()

    override fun pendingEvents(): List<PendingFlashcardStudyEvent> = events

    override fun save(events: List<PendingFlashcardStudyEvent>) {
        this.events = events
    }
}

private class RecordingFlashcardApi : FlashcardApi {
    var createdDeckTitle: String? = null
    var updatedDeckTitle: String? = null
    var clonedDeckId: Int? = null
    var deletedDeckId: Int? = null
    var failStudyResponse = false
    var lastStudyResponse: String? = null

    override suspend fun decks(): List<DeckDto> = listOf(sampleDeck())

    override suspend fun deck(deckId: Int): DeckDto = sampleDeck(deckId)

    override suspend fun createDeck(request: DeckCreateRequestDto): DeckDto {
        createdDeckTitle = request.title
        return sampleDeck(9).copy(title = request.title)
    }

    override suspend fun updateDeck(deckId: Int, request: DeckUpdateRequestDto): DeckDto {
        updatedDeckTitle = request.title
        return sampleDeck(deckId).copy(title = request.title ?: "Updated")
    }

    override suspend fun deleteDeck(deckId: Int) {
        deletedDeckId = deckId
    }

    override suspend fun duplicateDeck(deckId: Int): DeckDto = sampleDeck(deckId + 1)

    override suspend fun deckCards(deckId: Int): List<FlashcardDto> = listOf(
        FlashcardDto(id = 1, deckId = deckId, front = "Front", back = "Back"),
    )

    override suspend fun createCard(deckId: Int, request: CardCreateRequestDto): FlashcardDto = FlashcardDto(
        id = 2,
        deckId = deckId,
        front = request.front,
        back = request.back,
        cardType = request.cardType,
    )

    override suspend fun updateCard(deckId: Int, cardId: Int, request: CardUpdateRequestDto): FlashcardDto =
        FlashcardDto(
            id = cardId,
            deckId = deckId,
            front = request.front ?: "Front",
            back = request.back ?: "Back",
            cardType = request.cardType ?: CardType.Basic,
        )

    override suspend fun deleteCard(deckId: Int, cardId: Int) = Unit

    override suspend fun createSession(request: SessionCreateRequestDto): FlashcardStudySessionDto =
        FlashcardStudySessionDto(id = 5, deckIds = request.deckIds, studyMode = request.studyMode)

    override suspend fun sessionCards(sessionId: Int): List<SessionCardDto> = listOf(
        SessionCardDto(id = 1, cardId = 12, front = "Prompt", back = "Answer"),
    )

    override suspend fun respondToCard(
        sessionId: Int,
        request: SessionResponseRequestDto,
        idempotencyKey: String?,
    ) {
        if (failStudyResponse) throw IOException("offline")
        lastStudyResponse = "$sessionId:${request.cardId}"
    }

    override suspend fun endSession(sessionId: Int): SessionSummaryDto = SessionSummaryDto(
        cardsReviewed = 1,
        cardsCorrect = 1,
        xpEarned = 10,
        durationSeconds = 30,
    )

    override suspend fun queue(): List<QueueCardDto> = listOf(
        QueueCardDto(id = 1, cardId = 12, front = "Prompt", back = "Answer", deckTitle = "Deck", dueAt = "2026-06-08"),
    )

    override suspend fun queueSummary(): QueueSummaryDto = QueueSummaryDto(dueCount = 3, overdueCount = 1, estimatedMinutes = 5)

    override suspend fun marketplace(search: String?, category: String?, sort: String?): List<MarketplaceDeckDto> = listOf(
        MarketplaceDeckDto(id = 55, title = "Imported", creatorName = "CSNexus"),
    )

    override suspend fun cloneDeck(deckId: Int): DeckDto {
        clonedDeckId = deckId
        return sampleDeck(deckId)
    }

    override suspend fun rateDeck(deckId: Int, request: DeckRatingRequestDto) = Unit

    override suspend fun comments(deckId: Int): List<DeckCommentDto> = emptyList()

    override suspend fun postComment(deckId: Int, request: DeckCommentCreateRequestDto): CommentCreatedDto = CommentCreatedDto(1)

    override suspend fun deleteComment(commentId: Int) = Unit

    override suspend fun bookmarkDeck(deckId: Int) = Unit

    override suspend fun unbookmarkDeck(deckId: Int) = Unit

    override suspend fun analyticsDashboard(): AnalyticsDashboardDto = AnalyticsDashboardDto()

    override suspend fun heatmap(): List<HeatmapEntryDto> = emptyList()

    override suspend fun recommendations(): List<FlashcardRecommendationDto> = emptyList()

    override suspend fun createExam(request: ExamCreateRequestDto): ExamSimulationDto = ExamSimulationDto(id = 7)

    override suspend fun examCards(examId: Int): List<ExamCardDto> = emptyList()

    override suspend fun answerExamCard(examId: Int, request: ExamAnswerRequestDto) = Unit

    override suspend fun completeExam(examId: Int): ExamResultDto = ExamResultDto()

    override suspend fun feed(): List<DeckDto> = listOf(sampleDeck())

    override suspend fun adminAnalytics(): FlashcardAdminAnalyticsDto = FlashcardAdminAnalyticsDto(
        topFailedCards = listOf(AdminFailedCardDto(cardId = 5, failCount = 3)),
        activeReviewers7d = 14,
    )

    override suspend fun flagDeck(deckId: Int) = Unit

    override suspend fun featureDeck(deckId: Int) = Unit

    override suspend fun generateCards(request: GenerateCardsRequestDto): GenerateCardsResponseDto =
        GenerateCardsResponseDto(
            cards = listOf(
                GeneratedCardDto(front = "Q1", back = "A1"),
                GeneratedCardDto(front = "Q2", back = "A2"),
            ),
            termsExtracted = 2,
        )
}

private fun sampleDeck(deckId: Int = 1): DeckDto = DeckDto(
    id = deckId,
    title = "Sample Deck",
    category = DeckCategory.Verbal,
    visibility = DeckVisibility.Private,
    cardCount = 12,
)
