package com.csnexus.app.feature.progress.data

import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.core.sync.GoalTargetSyncPayload
import com.csnexus.app.core.sync.OfflineSyncProcessor
import com.csnexus.app.core.sync.OfflineSyncScheduler
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.SyncBannerState
import com.csnexus.app.core.sync.SyncEventType
import com.csnexus.app.core.sync.SyncFeature
import kotlinx.coroutines.flow.Flow

data class GoalBundle(
    val goal: DailyGoalDto,
    val weekly: WeeklyGoalDto,
    val freezes: FreezeCountDto,
)

class ProgressRepository(
    private val progressApi: ProgressApi,
    private val cacheStore: ProgressCacheStore? = null,
    private val syncStore: OfflineSyncStore? = null,
    private val syncScheduler: OfflineSyncScheduler? = null,
    private val syncProcessor: OfflineSyncProcessor? = null,
) {
    fun goalSyncBanner(): Flow<SyncBannerState?>? = syncStore?.observe(SyncFeature.Goals)

    suspend fun xp(): ApiResult<XpDto> = safeApiCall { progressApi.xp() }
    suspend fun achievements(): ApiResult<List<AchievementDto>> = safeApiCall { progressApi.achievements() }
    suspend fun snapshot(): ApiResult<ProgressSnapshotDto> = cacheBacked(KEY_SNAPSHOT) { progressApi.snapshot() }
    suspend fun mastery(): ApiResult<List<MasteryDto>> = safeApiCall { progressApi.mastery() }
    suspend fun weakestMastery(): ApiResult<List<MasteryDto>> = safeApiCall { progressApi.weakestMastery() }
    suspend fun dueReviews(): ApiResult<List<MasteryReviewDueDto>> = safeApiCall { progressApi.dueReviews() }
    suspend fun recommendations(): ApiResult<List<MasteryRecommendationDto>> = safeApiCall { progressApi.recommendations() }
    suspend fun readiness(): ApiResult<ReadinessDashboardDto> = cacheBacked(KEY_READINESS) { progressApi.readinessDashboard() }
    suspend fun readinessTrend(): ApiResult<ReadinessTrendResponseDto> = safeApiCall { progressApi.readinessTrend() }
    suspend fun selfAssessmentHistory(): ApiResult<SelfAssessmentHistoryResponseDto> = safeApiCall { progressApi.selfAssessmentHistory() }
    suspend fun selfAssessmentPrompt(): ApiResult<SelfAssessmentPromptDto> = safeApiCall { progressApi.selfAssessmentPrompt() }
    suspend fun plannerReadiness(): ApiResult<PlannerReadinessDto> = safeApiCall { progressApi.plannerReadiness() }
    suspend fun dailyGoal(): ApiResult<DailyGoalDto> = cacheBacked(KEY_DAILY_GOAL) { progressApi.dailyGoal() }
    suspend fun weeklyGoal(): ApiResult<WeeklyGoalDto> = cacheBacked(KEY_WEEKLY_GOAL) { progressApi.weeklyGoal() }
    suspend fun freezeCount(): ApiResult<FreezeCountDto> = cacheBacked(KEY_FREEZE_COUNT) { progressApi.freezeCount() }
    suspend fun studyPlan(): ApiResult<StudyPlanDto?> = safeApiCall { progressApi.studyPlan() }
    suspend fun todayPlanTasks(): ApiResult<List<StudyPlanTaskDto>> = safeApiCall { progressApi.todayPlanTasks() }

    suspend fun submitSelfAssessment(score: Int): ApiResult<SelfAssessmentResponseDto> = safeApiCall {
        progressApi.submitSelfAssessment(SelfAssessmentRequestDto(selfAssessedScore = score))
    }

    suspend fun updateGoalTarget(targetXp: Int): ApiResult<GoalBundle> = safeApiCall {
        try {
            progressApi.updateGoalTarget(GoalTargetRequestDto(targetXp))
            val bundle = GoalBundle(
                goal = progressApi.dailyGoal(),
                weekly = progressApi.weeklyGoal(),
                freezes = progressApi.freezeCount(),
            )
            cacheStore?.put(KEY_DAILY_GOAL, bundle.goal)
            cacheStore?.put(KEY_WEEKLY_GOAL, bundle.weekly)
            cacheStore?.put(KEY_FREEZE_COUNT, bundle.freezes)
            bundle
        } catch (error: java.io.IOException) {
            if (syncStore == null) throw error
            syncStore.enqueue(
                SyncEventType.GoalTargetUpdate,
                GoalTargetSyncPayload(targetXp = targetXp),
            )
            syncScheduler?.schedule()
            buildQueuedGoalBundle(targetXp)
        }
    }

    suspend fun createStudyPlan(
        targetExamDate: String,
        availableHoursPerDay: Double,
        targetScore: Double,
    ): ApiResult<Pair<StudyPlanDto, List<StudyPlanTaskDto>>> = safeApiCall {
        val plan = progressApi.createStudyPlan(
            CreateStudyPlanRequestDto(
                targetExamDate = targetExamDate,
                availableHoursPerDay = availableHoursPerDay,
                targetScore = targetScore,
            ),
        )
        plan to progressApi.todayPlanTasks()
    }

    suspend fun completeStudyTask(taskId: Int): ApiResult<Unit> = safeApiCall {
        progressApi.completeStudyTask(taskId)
    }

    suspend fun abandonStudyPlan(): ApiResult<Unit> = safeApiCall {
        progressApi.abandonStudyPlan()
    }

    suspend fun retryGoalSync(): ApiResult<Int> {
        val processor = syncProcessor ?: return ApiResult.Success(0)
        syncScheduler?.schedule()
        return ApiResult.Success(processor.process(SyncFeature.Goals).synced)
    }

    private suspend inline fun <reified T> cacheBacked(
        key: String,
        crossinline block: suspend () -> T,
    ): ApiResult<T> {
        return when (val result = safeApiCall { block() }) {
            is ApiResult.Success -> {
                cacheStore?.put(key, result.value)
                result
            }
            is ApiResult.Failure -> {
                cacheStore?.get<T>(key)?.let { ApiResult.Success(it.value) } ?: result
            }
        }
    }

    private suspend fun buildQueuedGoalBundle(targetXp: Int): GoalBundle {
        val cachedGoal = cacheStore?.get<DailyGoalDto>(KEY_DAILY_GOAL)?.value
        val cachedWeekly = cacheStore?.get<WeeklyGoalDto>(KEY_WEEKLY_GOAL)?.value ?: WeeklyGoalDto()
        val cachedFreezes = cacheStore?.get<FreezeCountDto>(KEY_FREEZE_COUNT)?.value ?: FreezeCountDto()
        val queuedGoal = (cachedGoal ?: DailyGoalDto()).copy(targetXp = targetXp)
        cacheStore?.put(KEY_DAILY_GOAL, queuedGoal)
        return GoalBundle(
            goal = queuedGoal,
            weekly = cachedWeekly,
            freezes = cachedFreezes,
        )
    }
}

private const val KEY_SNAPSHOT = "progress:snapshot"
private const val KEY_READINESS = "progress:readiness"
private const val KEY_DAILY_GOAL = "progress:daily_goal"
private const val KEY_WEEKLY_GOAL = "progress:weekly_goal"
private const val KEY_FREEZE_COUNT = "progress:freeze_count"
