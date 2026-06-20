package com.csnexus.app.feature.flashcards.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface FlashcardApi {
    @GET("v1/flashcards/decks")
    suspend fun decks(): List<DeckDto>

    @GET("v1/flashcards/decks/{deckId}")
    suspend fun deck(@Path("deckId") deckId: Int): DeckDto

    @POST("v1/flashcards/decks")
    suspend fun createDeck(@Body request: DeckCreateRequestDto): DeckDto

    @PATCH("v1/flashcards/decks/{deckId}")
    suspend fun updateDeck(
        @Path("deckId") deckId: Int,
        @Body request: DeckUpdateRequestDto,
    ): DeckDto

    @DELETE("v1/flashcards/decks/{deckId}")
    suspend fun deleteDeck(@Path("deckId") deckId: Int)

    @POST("v1/flashcards/decks/{deckId}/duplicate")
    suspend fun duplicateDeck(@Path("deckId") deckId: Int): DeckDto

    @GET("v1/flashcards/decks/{deckId}/cards")
    suspend fun deckCards(@Path("deckId") deckId: Int): List<FlashcardDto>

    @POST("v1/flashcards/decks/{deckId}/cards")
    suspend fun createCard(
        @Path("deckId") deckId: Int,
        @Body request: CardCreateRequestDto,
    ): FlashcardDto

    @PATCH("v1/flashcards/decks/{deckId}/cards/{cardId}")
    suspend fun updateCard(
        @Path("deckId") deckId: Int,
        @Path("cardId") cardId: Int,
        @Body request: CardUpdateRequestDto,
    ): FlashcardDto

    @DELETE("v1/flashcards/decks/{deckId}/cards/{cardId}")
    suspend fun deleteCard(
        @Path("deckId") deckId: Int,
        @Path("cardId") cardId: Int,
    )

    @POST("v1/flashcards/sessions")
    suspend fun createSession(@Body request: SessionCreateRequestDto): FlashcardStudySessionDto

    @GET("v1/flashcards/sessions/{sessionId}/cards")
    suspend fun sessionCards(@Path("sessionId") sessionId: Int): List<SessionCardDto>

    @POST("v1/flashcards/sessions/{sessionId}/respond")
    suspend fun respondToCard(
        @Path("sessionId") sessionId: Int,
        @Body request: SessionResponseRequestDto,
        @Header("Idempotency-Key") idempotencyKey: String? = null,
    )

    @POST("v1/flashcards/sessions/{sessionId}/end")
    suspend fun endSession(@Path("sessionId") sessionId: Int): SessionSummaryDto

    @GET("v1/flashcards/queue")
    suspend fun queue(): List<QueueCardDto>

    @GET("v1/flashcards/queue/summary")
    suspend fun queueSummary(): QueueSummaryDto

    @GET("v1/flashcards/marketplace")
    suspend fun marketplace(
        @Query("search") search: String? = null,
        @Query("category") category: String? = null,
        @Query("sort") sort: String? = null,
    ): List<MarketplaceDeckDto>

    @POST("v1/flashcards/marketplace/{deckId}/clone")
    suspend fun cloneDeck(@Path("deckId") deckId: Int): DeckDto

    @POST("v1/flashcards/marketplace/{deckId}/ratings")
    suspend fun rateDeck(
        @Path("deckId") deckId: Int,
        @Body request: DeckRatingRequestDto,
    )

    @GET("v1/flashcards/marketplace/{deckId}/comments")
    suspend fun comments(@Path("deckId") deckId: Int): List<DeckCommentDto>

    @POST("v1/flashcards/marketplace/{deckId}/comments")
    suspend fun postComment(
        @Path("deckId") deckId: Int,
        @Body request: DeckCommentCreateRequestDto,
    ): CommentCreatedDto

    @DELETE("v1/flashcards/comments/{commentId}")
    suspend fun deleteComment(@Path("commentId") commentId: Int)

    @POST("v1/flashcards/marketplace/{deckId}/bookmark")
    suspend fun bookmarkDeck(@Path("deckId") deckId: Int)

    @DELETE("v1/flashcards/marketplace/{deckId}/bookmark")
    suspend fun unbookmarkDeck(@Path("deckId") deckId: Int)

    @GET("v1/flashcards/analytics/dashboard")
    suspend fun analyticsDashboard(): AnalyticsDashboardDto

    @GET("v1/flashcards/analytics/heatmap")
    suspend fun heatmap(): List<HeatmapEntryDto>

    @GET("v1/flashcards/recommendations")
    suspend fun recommendations(): List<FlashcardRecommendationDto>

    @POST("v1/flashcards/exam-simulations")
    suspend fun createExam(@Body request: ExamCreateRequestDto): ExamSimulationDto

    @GET("v1/flashcards/exam-simulations/{examId}/cards")
    suspend fun examCards(@Path("examId") examId: Int): List<ExamCardDto>

    @POST("v1/flashcards/exam-simulations/{examId}/answer")
    suspend fun answerExamCard(
        @Path("examId") examId: Int,
        @Body request: ExamAnswerRequestDto,
    )

    @POST("v1/flashcards/exam-simulations/{examId}/complete")
    suspend fun completeExam(@Path("examId") examId: Int): ExamResultDto

    @GET("v1/flashcards/feed")
    suspend fun feed(): List<DeckDto>

    @GET("v1/flashcards/admin/analytics")
    suspend fun adminAnalytics(): FlashcardAdminAnalyticsDto

    @POST("v1/flashcards/admin/decks/{deckId}/:flag")
    suspend fun flagDeck(@Path("deckId") deckId: Int)

    @POST("v1/flashcards/admin/decks/{deckId}/:feature")
    suspend fun featureDeck(@Path("deckId") deckId: Int)

    @POST("v1/flashcards/generate")
    suspend fun generateCards(@Body request: GenerateCardsRequestDto): GenerateCardsResponseDto
}

@Serializable
enum class DeckCategory {
    @SerialName("verbal")
    Verbal,

    @SerialName("numerical")
    Numerical,

    @SerialName("analytical")
    Analytical,
    ;

    val label: String
        get() = when (this) {
            Verbal -> "Verbal"
            Numerical -> "Numerical"
            Analytical -> "Analytical"
        }
}

@Serializable
enum class DeckVisibility {
    @SerialName("private")
    Private,

    @SerialName("public")
    Public,

    @SerialName("unlisted")
    Unlisted,
    ;

    val label: String
        get() = when (this) {
            Private -> "Private"
            Public -> "Public"
            Unlisted -> "Unlisted"
        }
}

@Serializable
enum class CardType {
    @SerialName("basic")
    Basic,

    @SerialName("reverse")
    Reverse,

    @SerialName("cloze")
    Cloze,

    @SerialName("mcq")
    MultipleChoice,

    @SerialName("true_false")
    TrueFalse,

    @SerialName("matching")
    Matching,

    @SerialName("sequence")
    Sequence,
    ;

    val label: String
        get() = when (this) {
            Basic -> "Basic"
            Reverse -> "Reverse"
            Cloze -> "Cloze"
            MultipleChoice -> "MCQ"
            TrueFalse -> "True / False"
            Matching -> "Matching"
            Sequence -> "Sequence"
        }
}

@Serializable
enum class FlashcardStudyMode {
    @SerialName("swipe")
    Swipe,

    @SerialName("typing")
    Typing,

    @SerialName("rapid_recall")
    RapidRecall,

    @SerialName("quiz")
    Quiz,

    @SerialName("timed")
    Timed,

    @SerialName("exam_simulation")
    ExamSimulation,
    ;

    val label: String
        get() = when (this) {
            Swipe -> "Swipe"
            Typing -> "Typing"
            RapidRecall -> "Rapid Recall"
            Quiz -> "Quiz"
            Timed -> "Timed"
            ExamSimulation -> "Exam Simulation"
        }
}

@Serializable
enum class ResponseType {
    @SerialName("forgot")
    Forgot,

    @SerialName("remembered")
    Remembered,

    @SerialName("skipped")
    Skipped,
}

@Serializable
enum class ConfidenceLevel {
    @SerialName("guessed")
    Guessed,

    @SerialName("unsure")
    Unsure,

    @SerialName("confident")
    Confident,

    @SerialName("mastered")
    Mastered,
    ;

    val label: String
        get() = when (this) {
            Guessed -> "Forgot"
            Unsure -> "Unsure"
            Confident -> "Confident"
            Mastered -> "Mastered"
        }
}

@Serializable
data class DeckDto(
    val id: Int,
    val title: String,
    val description: String? = null,
    val category: DeckCategory = DeckCategory.Verbal,
    val visibility: DeckVisibility = DeckVisibility.Private,
    val tags: List<String>? = null,
    @SerialName("card_count")
    val cardCount: Int = 0,
    @SerialName("average_rating")
    val averageRating: Double = 0.0,
    @SerialName("created_at")
    val createdAt: String = "",
    @SerialName("updated_at")
    val updatedAt: String = createdAt,
)

@Serializable
data class DeckCreateRequestDto(
    val title: String,
    val category: DeckCategory,
    val visibility: DeckVisibility,
    val description: String? = null,
    val tags: List<String>? = null,
)

@Serializable
data class DeckUpdateRequestDto(
    val title: String? = null,
    val description: String? = null,
    val category: DeckCategory? = null,
    val visibility: DeckVisibility? = null,
)

@Serializable
data class FlashcardDto(
    val id: Int,
    @SerialName("deck_id")
    val deckId: Int = 0,
    val front: String,
    val back: String,
    @SerialName("card_type")
    val cardType: CardType = CardType.Basic,
    val hints: List<String>? = null,
    val tags: List<String>? = null,
    @SerialName("created_at")
    val createdAt: String = "",
)

@Serializable
data class CardCreateRequestDto(
    val front: String,
    val back: String,
    @SerialName("card_type")
    val cardType: CardType,
    val hints: List<String>? = null,
    val tags: List<String>? = null,
)

@Serializable
data class CardUpdateRequestDto(
    val front: String? = null,
    val back: String? = null,
    @SerialName("card_type")
    val cardType: CardType? = null,
    val hints: List<String>? = null,
    val tags: List<String>? = null,
)

@Serializable
data class FlashcardStudySessionDto(
    val id: Int,
    @SerialName("deck_ids")
    val deckIds: List<Int> = emptyList(),
    @SerialName("study_mode")
    val studyMode: FlashcardStudyMode = FlashcardStudyMode.Swipe,
    val status: String = "IN_PROGRESS",
    @SerialName("cards_reviewed")
    val cardsReviewed: Int = 0,
    @SerialName("cards_correct")
    val cardsCorrect: Int = 0,
    @SerialName("xp_earned")
    val xpEarned: Int = 0,
    @SerialName("started_at")
    val startedAt: String = "",
    @SerialName("ended_at")
    val endedAt: String? = null,
)

@Serializable
data class SessionCreateRequestDto(
    @SerialName("deck_ids")
    val deckIds: List<Int>,
    @SerialName("study_mode")
    val studyMode: FlashcardStudyMode,
)

@Serializable
data class SessionCardDto(
    val id: Int,
    @SerialName("card_id")
    val cardId: Int,
    val front: String,
    val back: String,
    @SerialName("card_type")
    val cardType: CardType = CardType.Basic,
    val hints: List<String> = emptyList(),
)

@Serializable
data class SessionResponseRequestDto(
    @SerialName("card_id")
    val cardId: Int,
    @SerialName("response_type")
    val responseType: ResponseType,
    val confidence: ConfidenceLevel,
)

@Serializable
data class SessionSummaryDto(
    @SerialName("cards_reviewed")
    val cardsReviewed: Int = 0,
    @SerialName("cards_correct")
    val cardsCorrect: Int = 0,
    @SerialName("xp_earned")
    val xpEarned: Int = 0,
    @SerialName("duration_seconds")
    val durationSeconds: Int = 0,
)

@Serializable
data class QueueCardDto(
    val id: Int,
    @SerialName("card_id")
    val cardId: Int,
    val front: String,
    val back: String,
    @SerialName("deck_title")
    val deckTitle: String,
    @SerialName("due_at")
    val dueAt: String,
)

@Serializable
data class QueueSummaryDto(
    @SerialName("due_count")
    val dueCount: Int = 0,
    @SerialName("overdue_count")
    val overdueCount: Int = 0,
    @SerialName("estimated_minutes")
    val estimatedMinutes: Int = 0,
)

@Serializable
data class MarketplaceDeckDto(
    val id: Int,
    val title: String,
    val description: String? = null,
    val category: DeckCategory = DeckCategory.Verbal,
    @SerialName("creator_name")
    val creatorName: String = "",
    @SerialName("average_rating")
    val averageRating: Double = 0.0,
    @SerialName("rating_count")
    val ratingCount: Int = 0,
    @SerialName("clone_count")
    val cloneCount: Int = 0,
    @SerialName("card_count")
    val cardCount: Int = 0,
)

@Serializable
data class DeckRatingRequestDto(
    val score: Int,
    val comment: String? = null,
)

@Serializable
data class DeckCommentDto(
    val id: Int,
    @SerialName("user_name")
    val userName: String = "",
    val comment: String = "",
    val score: Int = 0,
    @SerialName("created_at")
    val createdAt: String = "",
)

@Serializable
data class DeckCommentCreateRequestDto(
    val body: String,
    @SerialName("parent_comment_id")
    val parentCommentId: Int? = null,
)

@Serializable
data class CommentCreatedDto(
    val id: Int,
)

@Serializable
data class AnalyticsDashboardDto(
    @SerialName("overall_retention")
    val overallRetention: Double = 0.0,
    @SerialName("total_cards_studied")
    val totalCardsStudied: Int = 0,
    @SerialName("total_sessions")
    val totalSessions: Int = 0,
    @SerialName("strongest_subjects")
    val strongestSubjects: List<SubjectStatDto> = emptyList(),
    @SerialName("weakest_subjects")
    val weakestSubjects: List<SubjectStatDto> = emptyList(),
    @SerialName("predicted_readiness")
    val predictedReadiness: Double = 0.0,
)

@Serializable
data class SubjectStatDto(
    val category: String,
    @SerialName("retention_rate")
    val retentionRate: Double = 0.0,
    @SerialName("cards_studied")
    val cardsStudied: Int = 0,
)

@Serializable
data class HeatmapEntryDto(
    val date: String,
    @SerialName("cards_reviewed")
    val cardsReviewed: Int = 0,
    @SerialName("retention_rate")
    val retentionRate: Double = 0.0,
)

@Serializable
data class FlashcardRecommendationDto(
    val id: Int,
    @SerialName("deck_id")
    val deckId: Int,
    @SerialName("deck_title")
    val deckTitle: String,
    val reason: String = "",
    val priority: Int = 0,
)

@Serializable
data class ExamSimulationDto(
    val id: Int,
    @SerialName("deck_ids")
    val deckIds: List<Int> = emptyList(),
    @SerialName("card_count")
    val cardCount: Int = 0,
    @SerialName("time_limit_minutes")
    val timeLimitMinutes: Int = 0,
    val status: String = "IN_PROGRESS",
    val score: Int? = null,
    val percentage: Double? = null,
    @SerialName("time_taken_seconds")
    val timeTakenSeconds: Int? = null,
    @SerialName("started_at")
    val startedAt: String = "",
    @SerialName("completed_at")
    val completedAt: String? = null,
)

@Serializable
data class ExamCreateRequestDto(
    @SerialName("deck_ids")
    val deckIds: List<Int>,
    @SerialName("card_count")
    val cardCount: Int,
    @SerialName("time_limit_minutes")
    val timeLimitMinutes: Int,
)

@Serializable
data class ExamCardDto(
    val id: Int,
    @SerialName("card_id")
    val cardId: Int,
    val front: String,
    val back: String,
    @SerialName("card_type")
    val cardType: CardType = CardType.Basic,
)

@Serializable
data class ExamAnswerRequestDto(
    @SerialName("card_id")
    val cardId: Int,
    val answer: String,
)

@Serializable
data class ExamResultDto(
    val score: Int = 0,
    val total: Int = 0,
    val percentage: Double = 0.0,
    @SerialName("time_taken_seconds")
    val timeTakenSeconds: Int = 0,
    @SerialName("xp_earned")
    val xpEarned: Int = 0,
)

@Serializable
data class FlashcardAdminAnalyticsDto(
    @SerialName("top_failed_cards")
    val topFailedCards: List<AdminFailedCardDto> = emptyList(),
    @SerialName("active_reviewers_7d")
    val activeReviewers7d: Int = 0,
)

@Serializable
data class AdminFailedCardDto(
    @SerialName("card_id")
    val cardId: Int,
    @SerialName("fail_count")
    val failCount: Int,
)

@Serializable
data class GenerateCardsRequestDto(
    @SerialName("lesson_content")
    val lessonContent: String,
    @SerialName("lesson_id")
    val lessonId: Int,
    @SerialName("requested_card_count")
    val requestedCardCount: Int,
)

@Serializable
data class GenerateCardsResponseDto(
    val cards: List<GeneratedCardDto> = emptyList(),
    @SerialName("terms_extracted")
    val termsExtracted: Int = 0,
)

@Serializable
data class GeneratedCardDto(
    val front: String,
    val back: String,
    @SerialName("card_type")
    val cardType: CardType = CardType.Basic,
    val difficulty: String = "",
)
