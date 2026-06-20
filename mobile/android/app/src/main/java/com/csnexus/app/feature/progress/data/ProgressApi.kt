@file:OptIn(kotlinx.serialization.ExperimentalSerializationApi::class)

package com.csnexus.app.feature.progress.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonNames
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface ProgressApi {
    @GET("v1/xp/me")
    suspend fun xp(): XpDto

    @GET("v1/achievements/me")
    suspend fun achievements(): List<AchievementDto>

    @GET("v1/progress/snapshot")
    suspend fun snapshot(): ProgressSnapshotDto

    @GET("v1/mastery/me")
    suspend fun mastery(): List<MasteryDto>

    @GET("v1/mastery/me/weakest")
    suspend fun weakestMastery(): List<MasteryDto>

    @GET("v1/mastery/me/reviews/due")
    suspend fun dueReviews(): List<MasteryReviewDueDto>

    @GET("v1/mastery/me/recommendations")
    suspend fun recommendations(): List<MasteryRecommendationDto>

    @GET("v1/readiness/dashboard")
    suspend fun readinessDashboard(): ReadinessDashboardDto

    @GET("v1/readiness/trend")
    suspend fun readinessTrend(): ReadinessTrendResponseDto

    @GET("v1/readiness/self-assessment/history")
    suspend fun selfAssessmentHistory(): SelfAssessmentHistoryResponseDto

    @GET("v1/readiness/self-assessment/prompt")
    suspend fun selfAssessmentPrompt(): SelfAssessmentPromptDto

    @POST("v1/readiness/self-assessment")
    suspend fun submitSelfAssessment(@Body request: SelfAssessmentRequestDto): SelfAssessmentResponseDto

    @GET("v1/planner/readiness/me")
    suspend fun plannerReadiness(): PlannerReadinessDto

    @GET("v1/goals/me/today")
    suspend fun dailyGoal(): DailyGoalDto

    @GET("v1/goals/me/weekly")
    suspend fun weeklyGoal(): WeeklyGoalDto

    @GET("v1/streak/me/freezes")
    suspend fun freezeCount(): FreezeCountDto

    @PUT("v1/goals/me/target")
    suspend fun updateGoalTarget(
        @Body request: GoalTargetRequestDto,
        @Header("Idempotency-Key") idempotencyKey: String? = null,
    )

    @GET("v1/planner/plans/me")
    suspend fun studyPlan(): StudyPlanDto?

    @GET("v1/planner/plans/me/today")
    suspend fun todayPlanTasks(): List<StudyPlanTaskDto>

    @POST("v1/planner/plans")
    suspend fun createStudyPlan(@Body request: CreateStudyPlanRequestDto): StudyPlanDto

    @POST("v1/planner/plans/me/tasks/{taskId}:complete")
    suspend fun completeStudyTask(@Path("taskId") taskId: Int)

    @DELETE("v1/planner/plans/me")
    suspend fun abandonStudyPlan()
}

@Serializable
data class XpDto(
    @SerialName("cumulative_xp")
    val cumulativeXp: Int = 0,
    val level: Int = 0,
    @JsonNames("streak", "streak_count")
    val streak: Int = 0,
)

@Serializable
data class AchievementDto(
    @SerialName("achievement_id")
    val achievementId: String,
    val title: String,
    val description: String = "",
    @SerialName("granted_at")
    val grantedAt: String = "",
)

@Serializable
data class ProgressSnapshotDto(
    @SerialName("completed_lesson_ids")
    val completedLessonIds: List<Int> = emptyList(),
    @SerialName("cumulative_xp")
    val cumulativeXp: Int = 0,
    val level: Int = 0,
    @JsonNames("streak", "streak_count")
    val streak: Int = 0,
    @SerialName("total_subtopics")
    val totalSubtopics: Int = 0,
    @SerialName("completed_subtopics")
    val completedSubtopics: Int = 0,
    @SerialName("total_lessons")
    val totalLessons: Int = 0,
    @SerialName("completed_lessons")
    val completedLessons: Int = 0,
)

@Serializable
data class MasteryDto(
    @SerialName("subtopic_id")
    val subtopicId: Int,
    @SerialName("subtopic_title")
    val subtopicTitle: String,
    @SerialName("mastery_level")
    val masteryLevel: String,
    @SerialName("mastery_score")
    val masteryScore: Double,
    @SerialName("confidence_score")
    val confidenceScore: Double = 0.0,
    @SerialName("retention_score")
    val retentionScore: Double = 0.0,
    @SerialName("total_attempts")
    val totalAttempts: Int = 0,
    @SerialName("correct_attempts")
    val correctAttempts: Int = 0,
    @SerialName("last_practiced_at")
    val lastPracticedAt: String? = null,
)

@Serializable
data class MasteryReviewDueDto(
    @SerialName("subtopic_id")
    val subtopicId: Int,
    @SerialName("subtopic_title")
    val subtopicTitle: String,
    @SerialName("next_review_at")
    val nextReviewAt: String = "",
    @SerialName("days_overdue")
    val daysOverdue: Double = 0.0,
    @SerialName("interval_days")
    val intervalDays: Int = 0,
)

@Serializable
data class MasteryRecommendationDto(
    @SerialName("subtopic_id")
    val subtopicId: Int,
    @SerialName("subtopic_title")
    val subtopicTitle: String,
    val reason: String = "",
    val priority: Int = 0,
    @SerialName("recommended_difficulty")
    val recommendedDifficulty: String = "",
)

@Serializable
data class ReadinessDashboardDto(
    val score: Double = 0.0,
    val components: ReadinessComponentsDto = ReadinessComponentsDto(),
    val delta: Double? = null,
    @SerialName("top_impact_subtopics")
    val topImpactSubtopics: List<TopImpactSubtopicDto> = emptyList(),
    @SerialName("readiness_level")
    val readinessLevel: String = "",
    @SerialName("score_change_summary")
    val scoreChangeSummary: ScoreChangeSummaryDto? = null,
    @SerialName("stale_data")
    val staleData: Boolean = false,
    @SerialName("computed_at")
    val computedAt: String? = null,
)

@Serializable
data class ReadinessComponentsDto(
    @SerialName("mastery_component")
    val masteryComponent: Double = 0.0,
    @SerialName("retention_component")
    val retentionComponent: Double = 0.0,
    @SerialName("mock_component")
    val mockComponent: Double = 0.0,
    @SerialName("coverage_component")
    val coverageComponent: Double = 0.0,
)

@Serializable
data class TopImpactSubtopicDto(
    @SerialName("subtopic_id")
    val subtopicId: Int,
    @JsonNames("subtopic_name", "subtopic_title")
    val subtopicName: String = "",
    @SerialName("point_impact")
    val pointImpact: Double = 0.0,
)

@Serializable
data class ScoreChangeSummaryDto(
    @SerialName("primary_component")
    val primaryComponent: String = "",
    @SerialName("component_direction")
    val componentDirection: String = "",
    @SerialName("component_magnitude")
    val componentMagnitude: Double = 0.0,
    @SerialName("overall_delta")
    val overallDelta: Double = 0.0,
)

@Serializable
data class ReadinessTrendResponseDto(
    val trend: List<ReadinessTrendPointDto> = emptyList(),
)

@Serializable
data class ReadinessTrendPointDto(
    val date: String = "",
    val score: Double = 0.0,
)

@Serializable
data class SelfAssessmentRequestDto(
    @SerialName("self_assessed_score")
    val selfAssessedScore: Int,
)

@Serializable
data class SelfAssessmentResponseDto(
    @SerialName("self_assessed_score")
    val selfAssessedScore: Int = 0,
    @SerialName("computed_score")
    val computedScore: Double = 0.0,
    val delta: Double = 0.0,
    @SerialName("calibration_status")
    val calibrationStatus: String = "",
    val message: String = "",
    @SerialName("calibration_warning")
    val calibrationWarning: String? = null,
)

@Serializable
data class SelfAssessmentHistoryResponseDto(
    val records: List<SelfAssessmentHistoryItemDto> = emptyList(),
)

@Serializable
data class SelfAssessmentHistoryItemDto(
    @SerialName("self_assessed_score")
    val selfAssessedScore: Int = 0,
    @SerialName("computed_score")
    val computedScore: Double = 0.0,
    val delta: Double = 0.0,
    @SerialName("calibration_status")
    val calibrationStatus: String = "",
    @SerialName("assessed_at")
    val assessedAt: String = "",
)

@Serializable
data class SelfAssessmentPromptDto(
    @SerialName("is_due")
    val isDue: Boolean = false,
    @SerialName("last_assessed_at")
    val lastAssessedAt: String? = null,
)

@Serializable
data class PlannerReadinessDto(
    @SerialName("passing_probability")
    val passingProbability: Double = 0.0,
    @SerialName("predicted_score")
    val predictedScore: Double = 0.0,
    @SerialName("readiness_percentage")
    val readinessPercentage: Int = 0,
    @SerialName("recommended_hours_remaining")
    val recommendedHoursRemaining: Double = 0.0,
    val strengths: List<String> = emptyList(),
    val weaknesses: List<String> = emptyList(),
    @SerialName("confidence_level")
    val confidenceLevel: String = "",
)

@Serializable
data class DailyGoalDto(
    val id: Int = 0,
    @SerialName("target_xp")
    val targetXp: Int = 0,
    @SerialName("current_xp")
    val currentXp: Int = 0,
    @SerialName("goal_date")
    val goalDate: String = "",
    val completed: Boolean = false,
    @SerialName("completed_at")
    val completedAt: String? = null,
)

@Serializable
data class WeeklyGoalDto(
    val days: List<GoalDaySummaryDto> = emptyList(),
    @SerialName("completed_count")
    val completedCount: Int = 0,
    @SerialName("total_days")
    val totalDays: Int = 0,
)

@Serializable
data class GoalDaySummaryDto(
    @SerialName("goal_date")
    val goalDate: String = "",
    @SerialName("target_xp")
    val targetXp: Int = 0,
    @SerialName("current_xp")
    val currentXp: Int = 0,
    val completed: Boolean = false,
)

@Serializable
data class FreezeCountDto(
    val available: Int = 0,
)

@Serializable
data class GoalTargetRequestDto(
    @SerialName("target_xp")
    val targetXp: Int,
)

@Serializable
data class StudyPlanDto(
    val id: Int = 0,
    @SerialName("target_exam_date")
    val targetExamDate: String = "",
    @SerialName("available_hours_per_day")
    val availableHoursPerDay: Double = 0.0,
    @SerialName("target_score")
    val targetScore: Double = 0.0,
    val status: String = "",
    @SerialName("total_days")
    val totalDays: Int = 0,
    @SerialName("days_remaining")
    val daysRemaining: Int = 0,
    @SerialName("completion_percentage")
    val completionPercentage: Double = 0.0,
)

@Serializable
data class CreateStudyPlanRequestDto(
    @SerialName("target_exam_date")
    val targetExamDate: String,
    @SerialName("available_hours_per_day")
    val availableHoursPerDay: Double,
    @SerialName("target_score")
    val targetScore: Double,
)

@Serializable
data class StudyPlanTaskDto(
    val id: Int = 0,
    @SerialName("plan_date")
    val planDate: String = "",
    @SerialName("subtopic_title")
    val subtopicTitle: String = "",
    @SerialName("activity_type")
    val activityType: String = "",
    @SerialName("estimated_minutes")
    val estimatedMinutes: Int = 0,
    val completed: Boolean = false,
)
