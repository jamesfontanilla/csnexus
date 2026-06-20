package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.csnexus.app.core.design.CSNexusTheme
import com.csnexus.app.feature.flashcards.data.AdminFailedCardDto
import com.csnexus.app.feature.flashcards.data.AnalyticsDashboardDto
import com.csnexus.app.feature.flashcards.data.CardCreateRequestDto
import com.csnexus.app.feature.flashcards.data.CardType
import com.csnexus.app.feature.flashcards.data.CardUpdateRequestDto
import com.csnexus.app.feature.flashcards.data.CommentCreatedDto
import com.csnexus.app.feature.flashcards.data.ConfidenceLevel
import com.csnexus.app.feature.flashcards.data.DeckCategory
import com.csnexus.app.feature.flashcards.data.DeckCommentCreateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckCommentDto
import com.csnexus.app.feature.flashcards.data.DeckCreateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.DeckRatingRequestDto
import com.csnexus.app.feature.flashcards.data.DeckUpdateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckVisibility
import com.csnexus.app.feature.flashcards.data.ExamAnswerRequestDto
import com.csnexus.app.feature.flashcards.data.ExamCardDto
import com.csnexus.app.feature.flashcards.data.ExamCreateRequestDto
import com.csnexus.app.feature.flashcards.data.ExamResultDto
import com.csnexus.app.feature.flashcards.data.ExamSimulationDto
import com.csnexus.app.feature.flashcards.data.FlashcardAdminAnalyticsDto
import com.csnexus.app.feature.flashcards.data.FlashcardApi
import com.csnexus.app.feature.flashcards.data.FlashcardDto
import com.csnexus.app.feature.flashcards.data.FlashcardRecommendationDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.FlashcardStudyMode
import com.csnexus.app.feature.flashcards.data.FlashcardStudySessionDto
import com.csnexus.app.feature.flashcards.data.GenerateCardsRequestDto
import com.csnexus.app.feature.flashcards.data.GenerateCardsResponseDto
import com.csnexus.app.feature.flashcards.data.GeneratedCardDto
import com.csnexus.app.feature.flashcards.data.HeatmapEntryDto
import com.csnexus.app.feature.flashcards.data.MarketplaceDeckDto
import com.csnexus.app.feature.flashcards.data.QueueCardDto
import com.csnexus.app.feature.flashcards.data.QueueSummaryDto
import com.csnexus.app.feature.flashcards.data.ResponseType
import com.csnexus.app.feature.flashcards.data.SessionCardDto
import com.csnexus.app.feature.flashcards.data.SessionCreateRequestDto
import com.csnexus.app.feature.flashcards.data.SessionResponseRequestDto
import com.csnexus.app.feature.flashcards.data.SessionSummaryDto
import org.junit.Rule
import org.junit.Test

class FlashcardStudyScreenTest {
    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun studyScreenFlipsCardAndShowsSummary() {
        composeRule.setContent {
            CSNexusTheme {
                FlashcardStudyScreen(
                    repository = FlashcardRepository(StudyFlashcardApi()),
                    contentPadding = PaddingValues(),
                    deckIds = listOf(1),
                    initialMode = FlashcardStudyMode.Swipe,
                    onBack = {},
                )
            }
        }

        composeRule.onNodeWithText("Prompt").assertIsDisplayed()
        composeRule.onNodeWithText("Reveal Answer").performClick()
        composeRule.onNodeWithText("Answer").assertIsDisplayed()
        composeRule.onNodeWithText("Confident").performClick()
        composeRule.onNodeWithText("Study Summary").assertIsDisplayed()
        composeRule.onNodeWithText("1 cards reviewed").assertIsDisplayed()
    }

    @Test
    fun adminScreenGuardsNonAdminUsers() {
        composeRule.setContent {
            CSNexusTheme {
                FlashcardAdminScreen(
                    repository = FlashcardRepository(StudyFlashcardApi()),
                    contentPadding = PaddingValues(),
                    isAdmin = false,
                )
            }
        }

        composeRule.onNodeWithText("Admin access required").assertIsDisplayed()
    }
}

private class StudyFlashcardApi : FlashcardApi {
    override suspend fun decks(): List<DeckDto> = listOf(
        DeckDto(id = 1, title = "Deck", category = DeckCategory.Verbal, visibility = DeckVisibility.Private),
    )

    override suspend fun deck(deckId: Int): DeckDto = decks().first()

    override suspend fun createDeck(request: DeckCreateRequestDto): DeckDto = deck(1)

    override suspend fun updateDeck(deckId: Int, request: DeckUpdateRequestDto): DeckDto = deck(deckId)

    override suspend fun deleteDeck(deckId: Int) = Unit

    override suspend fun duplicateDeck(deckId: Int): DeckDto = deck(deckId)

    override suspend fun deckCards(deckId: Int): List<FlashcardDto> = listOf(
        FlashcardDto(id = 1, deckId = deckId, front = "Prompt", back = "Answer"),
    )

    override suspend fun createCard(deckId: Int, request: CardCreateRequestDto): FlashcardDto =
        FlashcardDto(id = 1, deckId = deckId, front = request.front, back = request.back, cardType = request.cardType)

    override suspend fun updateCard(deckId: Int, cardId: Int, request: CardUpdateRequestDto): FlashcardDto =
        FlashcardDto(id = cardId, deckId = deckId, front = request.front ?: "Prompt", back = request.back ?: "Answer")

    override suspend fun deleteCard(deckId: Int, cardId: Int) = Unit

    override suspend fun createSession(request: SessionCreateRequestDto): FlashcardStudySessionDto =
        FlashcardStudySessionDto(id = 4, deckIds = request.deckIds, studyMode = request.studyMode)

    override suspend fun sessionCards(sessionId: Int): List<SessionCardDto> = listOf(
        SessionCardDto(id = 1, cardId = 1, front = "Prompt", back = "Answer"),
    )

    override suspend fun respondToCard(
        sessionId: Int,
        request: SessionResponseRequestDto,
        idempotencyKey: String?,
    ) = Unit

    override suspend fun endSession(sessionId: Int): SessionSummaryDto = SessionSummaryDto(
        cardsReviewed = 1,
        cardsCorrect = 1,
        xpEarned = 10,
        durationSeconds = 30,
    )

    override suspend fun queue(): List<QueueCardDto> = listOf(
        QueueCardDto(id = 1, cardId = 1, front = "Prompt", back = "Answer", deckTitle = "Deck", dueAt = "2026-06-08"),
    )

    override suspend fun queueSummary(): QueueSummaryDto = QueueSummaryDto(dueCount = 1, overdueCount = 0, estimatedMinutes = 1)

    override suspend fun marketplace(search: String?, category: String?, sort: String?): List<MarketplaceDeckDto> = emptyList()

    override suspend fun cloneDeck(deckId: Int): DeckDto = deck(deckId)

    override suspend fun rateDeck(deckId: Int, request: DeckRatingRequestDto) = Unit

    override suspend fun comments(deckId: Int): List<DeckCommentDto> = emptyList()

    override suspend fun postComment(deckId: Int, request: DeckCommentCreateRequestDto): CommentCreatedDto = CommentCreatedDto(1)

    override suspend fun deleteComment(commentId: Int) = Unit

    override suspend fun bookmarkDeck(deckId: Int) = Unit

    override suspend fun unbookmarkDeck(deckId: Int) = Unit

    override suspend fun analyticsDashboard(): AnalyticsDashboardDto = AnalyticsDashboardDto()

    override suspend fun heatmap(): List<HeatmapEntryDto> = emptyList()

    override suspend fun recommendations(): List<FlashcardRecommendationDto> = emptyList()

    override suspend fun createExam(request: ExamCreateRequestDto): ExamSimulationDto = ExamSimulationDto(id = 1)

    override suspend fun examCards(examId: Int): List<ExamCardDto> = emptyList()

    override suspend fun answerExamCard(examId: Int, request: ExamAnswerRequestDto) = Unit

    override suspend fun completeExam(examId: Int): ExamResultDto = ExamResultDto()

    override suspend fun feed(): List<DeckDto> = decks()

    override suspend fun adminAnalytics(): FlashcardAdminAnalyticsDto = FlashcardAdminAnalyticsDto(
        topFailedCards = listOf(AdminFailedCardDto(cardId = 1, failCount = 2)),
        activeReviewers7d = 3,
    )

    override suspend fun flagDeck(deckId: Int) = Unit

    override suspend fun featureDeck(deckId: Int) = Unit

    override suspend fun generateCards(request: GenerateCardsRequestDto): GenerateCardsResponseDto = GenerateCardsResponseDto(
        cards = listOf(GeneratedCardDto(front = "Prompt", back = "Answer", cardType = CardType.Basic)),
        termsExtracted = 1,
    )
}
