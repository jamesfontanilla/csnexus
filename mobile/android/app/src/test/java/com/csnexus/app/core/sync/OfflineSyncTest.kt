package com.csnexus.app.core.sync

import com.csnexus.app.core.database.SyncEventDao
import com.csnexus.app.core.database.SyncEventEntity
import com.csnexus.app.feature.content.data.ContentApi
import com.csnexus.app.feature.content.data.LessonCompleteRequestDto
import com.csnexus.app.feature.content.data.LessonCompletionDto
import com.csnexus.app.feature.content.data.LessonDto
import com.csnexus.app.feature.content.data.ModuleDto
import com.csnexus.app.feature.content.data.PaginatedResponseDto
import com.csnexus.app.feature.content.data.SubtopicDto
import com.csnexus.app.feature.content.data.TopicDto
import com.csnexus.app.feature.flashcards.data.AdminFailedCardDto
import com.csnexus.app.feature.flashcards.data.AnalyticsDashboardDto
import com.csnexus.app.feature.flashcards.data.CardCreateRequestDto
import com.csnexus.app.feature.flashcards.data.CardUpdateRequestDto
import com.csnexus.app.feature.flashcards.data.CommentCreatedDto
import com.csnexus.app.feature.flashcards.data.DeckCommentCreateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckCommentDto
import com.csnexus.app.feature.flashcards.data.DeckCreateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.DeckRatingRequestDto
import com.csnexus.app.feature.flashcards.data.DeckUpdateRequestDto
import com.csnexus.app.feature.flashcards.data.ExamAnswerRequestDto
import com.csnexus.app.feature.flashcards.data.ExamCardDto
import com.csnexus.app.feature.flashcards.data.ExamCreateRequestDto
import com.csnexus.app.feature.flashcards.data.ExamResultDto
import com.csnexus.app.feature.flashcards.data.ExamSimulationDto
import com.csnexus.app.feature.flashcards.data.FlashcardAdminAnalyticsDto
import com.csnexus.app.feature.flashcards.data.FlashcardApi
import com.csnexus.app.feature.flashcards.data.FlashcardDto
import com.csnexus.app.feature.flashcards.data.FlashcardRecommendationDto
import com.csnexus.app.feature.flashcards.data.GenerateCardsRequestDto
import com.csnexus.app.feature.flashcards.data.GenerateCardsResponseDto
import com.csnexus.app.feature.flashcards.data.HeatmapEntryDto
import com.csnexus.app.feature.flashcards.data.MarketplaceDeckDto
import com.csnexus.app.feature.flashcards.data.QueueCardDto
import com.csnexus.app.feature.flashcards.data.QueueSummaryDto
import com.csnexus.app.feature.flashcards.data.SessionCardDto
import com.csnexus.app.feature.flashcards.data.SessionCreateRequestDto
import com.csnexus.app.feature.flashcards.data.SessionResponseRequestDto
import com.csnexus.app.feature.flashcards.data.SessionSummaryDto
import com.csnexus.app.feature.flashcards.data.FlashcardStudySessionDto
import com.csnexus.app.feature.motivation.data.ConsistencyDto
import com.csnexus.app.feature.motivation.data.DailyQueueDto
import com.csnexus.app.feature.motivation.data.ExamDateUpdateRequestDto
import com.csnexus.app.feature.motivation.data.ExamDateUpdateResponseDto
import com.csnexus.app.feature.motivation.data.FocusSessionCompleteRequestDto
import com.csnexus.app.feature.motivation.data.FocusSessionCreateRequestDto
import com.csnexus.app.feature.motivation.data.FocusSessionDto
import com.csnexus.app.feature.motivation.data.FocusStatsDto
import com.csnexus.app.feature.motivation.data.FocusWellnessDto
import com.csnexus.app.feature.motivation.data.MilestonesResponseDto
import com.csnexus.app.feature.motivation.data.MotivationApi
import com.csnexus.app.feature.motivation.data.OnboardingRequestDto
import com.csnexus.app.feature.motivation.data.OnboardingResponseDto
import com.csnexus.app.feature.motivation.data.PlanSummaryDto
import com.csnexus.app.feature.motivation.data.QueuePreferencesDto
import com.csnexus.app.feature.motivation.data.QueuePreferencesRequestDto
import com.csnexus.app.feature.progress.data.AchievementDto
import com.csnexus.app.feature.progress.data.CreateStudyPlanRequestDto
import com.csnexus.app.feature.progress.data.DailyGoalDto
import com.csnexus.app.feature.progress.data.FreezeCountDto
import com.csnexus.app.feature.progress.data.GoalTargetRequestDto
import com.csnexus.app.feature.progress.data.MasteryDto
import com.csnexus.app.feature.progress.data.MasteryRecommendationDto
import com.csnexus.app.feature.progress.data.MasteryReviewDueDto
import com.csnexus.app.feature.progress.data.PlannerReadinessDto
import com.csnexus.app.feature.progress.data.ProgressApi
import com.csnexus.app.feature.progress.data.ProgressSnapshotDto
import com.csnexus.app.feature.progress.data.ReadinessDashboardDto
import com.csnexus.app.feature.progress.data.ReadinessTrendResponseDto
import com.csnexus.app.feature.progress.data.SelfAssessmentHistoryResponseDto
import com.csnexus.app.feature.progress.data.SelfAssessmentPromptDto
import com.csnexus.app.feature.progress.data.SelfAssessmentRequestDto
import com.csnexus.app.feature.progress.data.SelfAssessmentResponseDto
import com.csnexus.app.feature.progress.data.StudyPlanDto
import com.csnexus.app.feature.progress.data.StudyPlanTaskDto
import com.csnexus.app.feature.progress.data.WeeklyGoalDto
import com.csnexus.app.feature.progress.data.XpDto
import com.csnexus.app.feature.settings.data.DailyGoalRequestDto
import com.csnexus.app.feature.settings.data.DailyGoalResponseDto
import com.csnexus.app.feature.settings.data.SettingsApi
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.test.runTest
import kotlinx.serialization.json.JsonNull
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import retrofit2.HttpException
import retrofit2.Response

class OfflineSyncTest {
    @Test
    fun offlineSyncAllowListMatchesImplementedEventTypes() = runTest {
        val allowedKinds = SyncEventType.entries.map { it.wireValue }

        assertEquals(
            listOf(
                "lesson_completion",
                "flashcard_response",
                "focus_completion",
                "goal_target_update",
                "settings_daily_goal_update",
            ),
            allowedKinds,
        )
    }

    @Test
    fun enqueueDeduplicatesEquivalentPayloads() = runTest {
        val dao = FakeSyncEventDao()
        val store = OfflineSyncStore(dao)

        val first = store.enqueue(SyncEventType.LessonCompletion, LessonCompletionSyncPayload(subtopicId = 12))
        val second = store.enqueue(SyncEventType.LessonCompletion, LessonCompletionSyncPayload(subtopicId = 12))

        assertEquals(first.id, second.id)
        assertEquals(1, store.pending().size)
    }

    @Test
    fun processRemovesSyncedEventsOnSuccess() = runTest {
        val dao = FakeSyncEventDao()
        val store = OfflineSyncStore(dao)
        store.enqueue(SyncEventType.FocusCompletion, FocusCompletionSyncPayload(sessionId = 7, totalFocusMinutes = 25, distractions = 1))
        val processor = OfflineSyncProcessor(
            store = store,
            contentApi = FakeContentApi(),
            flashcardApi = FakeFlashcardApi(),
            motivationApi = FakeMotivationApi(),
            progressApi = FakeProgressApi(),
            settingsApi = FakeSettingsApi(),
        )

        val summary = processor.process()

        assertEquals(1, summary.synced)
        assertEquals(0, store.pending().size)
    }

    @Test
    fun processMarksConflictOnServerConflict() = runTest {
        val dao = FakeSyncEventDao()
        val store = OfflineSyncStore(dao)
        val event = store.enqueue(SyncEventType.GoalTargetUpdate, GoalTargetSyncPayload(targetXp = 90))
        val processor = OfflineSyncProcessor(
            store = store,
            contentApi = FakeContentApi(),
            flashcardApi = FakeFlashcardApi(),
            motivationApi = FakeMotivationApi(),
            progressApi = FakeProgressApi { throw httpError(409, "SERVER_CONFLICT") },
            settingsApi = FakeSettingsApi(),
        )

        val summary = processor.process()
        val saved = dao.get(event.id)

        assertEquals(1, summary.conflicts)
        assertNotNull(saved)
        assertEquals(SyncEventStatus.Conflict.wireValue, saved?.status)
    }

    @Test
    fun processMarksFailedWhenAuthExpired() = runTest {
        val dao = FakeSyncEventDao()
        val store = OfflineSyncStore(dao)
        val event = store.enqueue(SyncEventType.SettingsDailyGoalUpdate, SettingsDailyGoalSyncPayload(targetXp = 40))
        val processor = OfflineSyncProcessor(
            store = store,
            contentApi = FakeContentApi(),
            flashcardApi = FakeFlashcardApi(),
            motivationApi = FakeMotivationApi(),
            progressApi = FakeProgressApi(),
            settingsApi = FakeSettingsApi { throw httpError(401, "AUTH_EXPIRED") },
        )

        val summary = processor.process()
        val saved = dao.get(event.id)

        assertEquals(1, summary.failed)
        assertEquals(SyncEventStatus.Failed.wireValue, saved?.status)
    }

    @Test
    fun processMarksFailedWhenForbiddenAuthExpired() = runTest {
        val dao = FakeSyncEventDao()
        val store = OfflineSyncStore(dao)
        val event = store.enqueue(SyncEventType.SettingsDailyGoalUpdate, SettingsDailyGoalSyncPayload(targetXp = 40))
        val processor = OfflineSyncProcessor(
            store = store,
            contentApi = FakeContentApi(),
            flashcardApi = FakeFlashcardApi(),
            motivationApi = FakeMotivationApi(),
            progressApi = FakeProgressApi(),
            settingsApi = FakeSettingsApi { throw httpError(403, "AUTH_EXPIRED") },
        )

        val summary = processor.process()
        val saved = dao.get(event.id)

        assertEquals(1, summary.failed)
        assertEquals(SyncEventStatus.Failed.wireValue, saved?.status)
    }

    @Test
    fun queuedEventsRemainVisibleAcrossNewStoreInstances() = runTest {
        val dao = FakeSyncEventDao()
        val firstStore = OfflineSyncStore(dao)
        firstStore.enqueue(SyncEventType.FlashcardResponse, FlashcardResponseSyncPayload(sessionId = 3, cardId = 8, responseType = com.csnexus.app.feature.flashcards.data.ResponseType.Remembered, confidence = com.csnexus.app.feature.flashcards.data.ConfidenceLevel.Confident))

        val secondStore = OfflineSyncStore(dao)

        assertEquals(1, secondStore.pending(SyncFeature.Flashcards).size)
        assertTrue(secondStore.observe(SyncFeature.Flashcards) is Flow<SyncBannerState?>)
    }
}

private class FakeSyncEventDao : SyncEventDao {
    private val state = MutableStateFlow<List<SyncEventEntity>>(emptyList())

    override suspend fun upsert(entity: SyncEventEntity) {
        state.value = state.value.filterNot { it.id == entity.id } + entity
    }

    override suspend fun get(id: String): SyncEventEntity? = state.value.firstOrNull { it.id == id }

    override suspend fun pending(): List<SyncEventEntity> =
        state.value.filter { it.status == SyncEventStatus.Queued.wireValue || it.status == SyncEventStatus.Failed.wireValue }

    override fun observeFeature(feature: String): Flow<List<SyncEventEntity>> =
        state.map { items ->
            items.filter {
                it.feature == feature && it.status in setOf(
                    SyncEventStatus.Queued.wireValue,
                    SyncEventStatus.Syncing.wireValue,
                    SyncEventStatus.Failed.wireValue,
                    SyncEventStatus.Conflict.wireValue,
                )
            }
        }

    override suspend fun pendingByFeature(feature: String): List<SyncEventEntity> =
        pending().filter { it.feature == feature }

    override suspend fun delete(id: String) {
        state.value = state.value.filterNot { it.id == id }
    }

    override suspend fun deleteSynced() {
        state.value = state.value.filterNot { it.status == SyncEventStatus.Synced.wireValue }
    }
}

private class FakeContentApi : ContentApi {
    override suspend fun modules(): PaginatedResponseDto<ModuleDto> = PaginatedResponseDto(emptyList(), 0, 0, 20)
    override suspend fun topics(moduleId: Int): List<TopicDto> = emptyList()
    override suspend fun subtopics(topicId: Int): List<SubtopicDto> = emptyList()
    override suspend fun lesson(subtopicId: Int): LessonDto = LessonDto(1, subtopicId, "Lesson", "published", JsonNull)
    override suspend fun completeLesson(
        subtopicId: Int,
        request: LessonCompleteRequestDto,
        idempotencyKey: String?,
    ): LessonCompletionDto = LessonCompletionDto()
}

private class FakeFlashcardApi : FlashcardApi {
    override suspend fun decks(): List<DeckDto> = emptyList()
    override suspend fun deck(deckId: Int): DeckDto = DeckDto(deckId, "Deck")
    override suspend fun createDeck(request: DeckCreateRequestDto): DeckDto = DeckDto(1, request.title)
    override suspend fun updateDeck(deckId: Int, request: DeckUpdateRequestDto): DeckDto = DeckDto(deckId, request.title ?: "Deck")
    override suspend fun deleteDeck(deckId: Int) = Unit
    override suspend fun duplicateDeck(deckId: Int): DeckDto = DeckDto(deckId + 1, "Copy")
    override suspend fun deckCards(deckId: Int): List<FlashcardDto> = emptyList()
    override suspend fun createCard(deckId: Int, request: CardCreateRequestDto): FlashcardDto = FlashcardDto(1, deckId, request.front, request.back)
    override suspend fun updateCard(deckId: Int, cardId: Int, request: CardUpdateRequestDto): FlashcardDto = FlashcardDto(cardId, deckId, request.front ?: "F", request.back ?: "B")
    override suspend fun deleteCard(deckId: Int, cardId: Int) = Unit
    override suspend fun createSession(request: SessionCreateRequestDto): FlashcardStudySessionDto = FlashcardStudySessionDto(id = 1)
    override suspend fun sessionCards(sessionId: Int): List<SessionCardDto> = emptyList()
    override suspend fun respondToCard(sessionId: Int, request: SessionResponseRequestDto, idempotencyKey: String?) = Unit
    override suspend fun endSession(sessionId: Int): SessionSummaryDto = SessionSummaryDto()
    override suspend fun queue(): List<QueueCardDto> = emptyList()
    override suspend fun queueSummary(): QueueSummaryDto = QueueSummaryDto()
    override suspend fun marketplace(search: String?, category: String?, sort: String?): List<MarketplaceDeckDto> = emptyList()
    override suspend fun cloneDeck(deckId: Int): DeckDto = DeckDto(deckId, "Deck")
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
    override suspend fun feed(): List<DeckDto> = emptyList()
    override suspend fun adminAnalytics(): FlashcardAdminAnalyticsDto = FlashcardAdminAnalyticsDto(topFailedCards = listOf(AdminFailedCardDto(cardId = 1, failCount = 1)))
    override suspend fun flagDeck(deckId: Int) = Unit
    override suspend fun featureDeck(deckId: Int) = Unit
    override suspend fun generateCards(request: GenerateCardsRequestDto): GenerateCardsResponseDto = GenerateCardsResponseDto()
}

private class FakeMotivationApi : MotivationApi {
    override suspend fun submitOnboarding(request: OnboardingRequestDto): OnboardingResponseDto = OnboardingResponseDto()
    override suspend fun updateExamDate(request: ExamDateUpdateRequestDto): ExamDateUpdateResponseDto = ExamDateUpdateResponseDto()
    override suspend fun onboardingPlanSummary(): PlanSummaryDto = PlanSummaryDto()
    override suspend fun focusStats(): FocusStatsDto = FocusStatsDto()
    override suspend fun startFocusSession(request: FocusSessionCreateRequestDto): FocusSessionDto = FocusSessionDto(id = 1)
    override suspend fun completeFocusSession(sessionId: Int, request: FocusSessionCompleteRequestDto, idempotencyKey: String?) = Unit
    override suspend fun abandonFocusSession(sessionId: Int) = Unit
    override suspend fun focusWellness(): FocusWellnessDto = FocusWellnessDto()
    override suspend fun queue(): DailyQueueDto = DailyQueueDto()
    override suspend fun completeQueueItem(itemId: Int): DailyQueueDto = DailyQueueDto()
    override suspend fun regenerateQueue(): DailyQueueDto = DailyQueueDto()
    override suspend fun queuePreferences(): QueuePreferencesDto = QueuePreferencesDto()
    override suspend fun updateQueuePreferences(request: QueuePreferencesRequestDto): QueuePreferencesDto = QueuePreferencesDto()
    override suspend fun milestones(): MilestonesResponseDto = MilestonesResponseDto()
    override suspend fun consistency(): ConsistencyDto = ConsistencyDto()
}

private class FakeProgressApi(
    private val onUpdateGoal: suspend (GoalTargetRequestDto) -> Unit = {},
) : ProgressApi {
    override suspend fun xp(): XpDto = XpDto()
    override suspend fun achievements(): List<AchievementDto> = emptyList()
    override suspend fun snapshot(): ProgressSnapshotDto = ProgressSnapshotDto()
    override suspend fun mastery(): List<MasteryDto> = emptyList()
    override suspend fun weakestMastery(): List<MasteryDto> = emptyList()
    override suspend fun dueReviews(): List<MasteryReviewDueDto> = emptyList()
    override suspend fun recommendations(): List<MasteryRecommendationDto> = emptyList()
    override suspend fun readinessDashboard(): ReadinessDashboardDto = ReadinessDashboardDto()
    override suspend fun readinessTrend(): ReadinessTrendResponseDto = ReadinessTrendResponseDto()
    override suspend fun selfAssessmentHistory(): SelfAssessmentHistoryResponseDto = SelfAssessmentHistoryResponseDto()
    override suspend fun selfAssessmentPrompt(): SelfAssessmentPromptDto = SelfAssessmentPromptDto()
    override suspend fun submitSelfAssessment(request: SelfAssessmentRequestDto): SelfAssessmentResponseDto = SelfAssessmentResponseDto()
    override suspend fun plannerReadiness(): PlannerReadinessDto = PlannerReadinessDto()
    override suspend fun dailyGoal(): DailyGoalDto = DailyGoalDto()
    override suspend fun weeklyGoal(): WeeklyGoalDto = WeeklyGoalDto()
    override suspend fun freezeCount(): FreezeCountDto = FreezeCountDto()
    override suspend fun updateGoalTarget(request: GoalTargetRequestDto, idempotencyKey: String?) = onUpdateGoal(request)
    override suspend fun studyPlan(): StudyPlanDto? = null
    override suspend fun todayPlanTasks(): List<StudyPlanTaskDto> = emptyList()
    override suspend fun createStudyPlan(request: CreateStudyPlanRequestDto): StudyPlanDto = StudyPlanDto()
    override suspend fun completeStudyTask(taskId: Int) = Unit
    override suspend fun abandonStudyPlan() = Unit
}

private class FakeSettingsApi(
    private val onUpdateGoal: suspend (DailyGoalRequestDto) -> Unit = {},
) : SettingsApi {
    override suspend fun updateDailyGoal(request: DailyGoalRequestDto, idempotencyKey: String?): DailyGoalResponseDto {
        onUpdateGoal(request)
        return DailyGoalResponseDto(targetXp = request.targetXp, status = "ok")
    }
}

private fun httpError(statusCode: Int, code: String): HttpException {
    val body = """{"error":{"code":"$code","message":"$code"}}"""
        .toResponseBody("application/json".toMediaType())
    return HttpException(Response.error<Unit>(statusCode, body))
}
