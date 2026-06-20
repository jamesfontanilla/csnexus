package com.csnexus.app.feature.progress.data

import com.csnexus.app.core.network.ApiResult
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class ProgressRepositoryTest {
    @Test
    fun updateGoalTargetReturnsRefreshedServerValues() = runTest {
        val api = FakeProgressApi().apply {
            dailyGoal = DailyGoalDto(targetXp = 25, currentXp = 10)
            weeklyGoal = WeeklyGoalDto(completedCount = 2, totalDays = 7)
            freezeCount = FreezeCountDto(available = 1)
            updatedGoal = DailyGoalDto(targetXp = 75, currentXp = 12)
        }
        val repository = ProgressRepository(api)

        val result = repository.updateGoalTarget(50)

        assertTrue(result is ApiResult.Success)
        val bundle = (result as ApiResult.Success).value
        assertEquals(50, api.lastUpdatedGoalTarget)
        assertEquals(75, bundle.goal.targetXp)
        assertEquals(2, bundle.weekly.completedCount)
        assertEquals(1, bundle.freezes.available)
    }

    @Test
    fun createStudyPlanReturnsPlanAndTodayTasks() = runTest {
        val api = FakeProgressApi().apply {
            createdPlan = StudyPlanDto(id = 4, targetExamDate = "2026-12-01", completionPercentage = 12.0)
            todayTasks = listOf(
                StudyPlanTaskDto(id = 9, subtopicTitle = "Inference", activityType = "quiz", estimatedMinutes = 20),
            )
        }
        val repository = ProgressRepository(api)

        val result = repository.createStudyPlan(
            targetExamDate = "2026-12-01",
            availableHoursPerDay = 2.0,
            targetScore = 0.8,
        )

        assertTrue(result is ApiResult.Success)
        val value = (result as ApiResult.Success).value
        assertEquals(4, value.first.id)
        assertEquals(1, value.second.size)
        assertEquals("Inference", value.second.single().subtopicTitle)
    }
}

private class FakeProgressApi : ProgressApi {
    var dailyGoal: DailyGoalDto = DailyGoalDto()
    var weeklyGoal: WeeklyGoalDto = WeeklyGoalDto()
    var freezeCount: FreezeCountDto = FreezeCountDto()
    var updatedGoal: DailyGoalDto = DailyGoalDto()
    var createdPlan: StudyPlanDto? = null
    var todayTasks: List<StudyPlanTaskDto> = emptyList()
    var lastUpdatedGoalTarget: Int? = null

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
    override suspend fun dailyGoal(): DailyGoalDto = if (lastUpdatedGoalTarget == null) dailyGoal else updatedGoal
    override suspend fun weeklyGoal(): WeeklyGoalDto = weeklyGoal
    override suspend fun freezeCount(): FreezeCountDto = freezeCount
    override suspend fun updateGoalTarget(request: GoalTargetRequestDto, idempotencyKey: String?) {
        lastUpdatedGoalTarget = request.targetXp
    }
    override suspend fun studyPlan(): StudyPlanDto? = createdPlan
    override suspend fun todayPlanTasks(): List<StudyPlanTaskDto> = todayTasks
    override suspend fun createStudyPlan(request: CreateStudyPlanRequestDto): StudyPlanDto = createdPlan ?: StudyPlanDto()
    override suspend fun completeStudyTask(taskId: Int) = Unit
    override suspend fun abandonStudyPlan() = Unit
}
