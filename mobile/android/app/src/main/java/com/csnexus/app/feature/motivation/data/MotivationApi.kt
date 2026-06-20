package com.csnexus.app.feature.motivation.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path

interface MotivationApi {
    @POST("v1/onboarding")
    suspend fun submitOnboarding(@Body request: OnboardingRequestDto): OnboardingResponseDto

    @PATCH("v1/onboarding/exam-date")
    suspend fun updateExamDate(@Body request: ExamDateUpdateRequestDto): ExamDateUpdateResponseDto

    @GET("v1/onboarding/plan-summary")
    suspend fun onboardingPlanSummary(): PlanSummaryDto

    @GET("v1/focus/sessions/me/stats")
    suspend fun focusStats(): FocusStatsDto

    @POST("v1/focus/sessions")
    suspend fun startFocusSession(@Body request: FocusSessionCreateRequestDto): FocusSessionDto

    @POST("v1/focus/sessions/{sessionId}:complete")
    suspend fun completeFocusSession(
        @Path("sessionId") sessionId: Int,
        @Body request: FocusSessionCompleteRequestDto,
        @Header("Idempotency-Key") idempotencyKey: String? = null,
    )

    @POST("v1/focus/sessions/{sessionId}:abandon")
    suspend fun abandonFocusSession(@Path("sessionId") sessionId: Int)

    @GET("v1/focus/wellness/me")
    suspend fun focusWellness(): FocusWellnessDto

    @GET("v1/queue")
    suspend fun queue(): DailyQueueDto

    @POST("v1/queue/items/{itemId}/:complete")
    suspend fun completeQueueItem(@Path("itemId") itemId: Int): DailyQueueDto

    @POST("v1/queue/:regenerate")
    suspend fun regenerateQueue(): DailyQueueDto

    @GET("v1/queue/preferences")
    suspend fun queuePreferences(): QueuePreferencesDto

    @PATCH("v1/queue/preferences")
    suspend fun updateQueuePreferences(@Body request: QueuePreferencesRequestDto): QueuePreferencesDto

    @GET("v1/milestones")
    suspend fun milestones(): MilestonesResponseDto

    @GET("v1/consistency")
    suspend fun consistency(): ConsistencyDto
}

@Serializable
enum class OnboardingExamCategory {
    @SerialName("Professional")
    Professional,

    @SerialName("Sub-Professional")
    SubProfessional,
    ;

    val label: String
        get() = when (this) {
            Professional -> "Professional"
            SubProfessional -> "Sub-Professional"
        }
}

@Serializable
data class OnboardingRequestDto(
    @SerialName("exam_date")
    val examDate: String,
    @SerialName("exam_category")
    val examCategory: OnboardingExamCategory,
    @SerialName("time_budget_minutes")
    val timeBudgetMinutes: Int,
)

@Serializable
data class OnboardingResponseDto(
    val confirmation: String = "",
    val warning: String? = null,
)

@Serializable
data class ExamDateUpdateRequestDto(
    @SerialName("exam_date")
    val examDate: String,
)

@Serializable
data class ExamDateUpdateResponseDto(
    val confirmation: String = "",
    val warning: String? = null,
)

@Serializable
data class PlanSummaryDto(
    @SerialName("total_days")
    val totalDays: Int = 0,
    @SerialName("subtopics_per_week")
    val subtopicsPerWeek: Int = 0,
    @SerialName("mock_exams_scheduled")
    val mockExamsScheduled: Int = 0,
    @SerialName("estimated_readiness_at_exam")
    val estimatedReadinessAtExam: Int = 0,
)

@Serializable
data class FocusStatsDto(
    @SerialName("total_sessions")
    val totalSessions: Int = 0,
    @SerialName("total_focus_hours")
    val totalFocusHours: Double = 0.0,
    @SerialName("avg_session_minutes")
    val averageSessionMinutes: Int = 0,
    @SerialName("sessions_today")
    val sessionsToday: Int = 0,
    @SerialName("focus_minutes_today")
    val focusMinutesToday: Int = 0,
)

@Serializable
data class FocusSessionCreateRequestDto(
    val mode: String,
    @SerialName("work_minutes")
    val workMinutes: Int,
    @SerialName("break_minutes")
    val breakMinutes: Int,
)

@Serializable
data class FocusSessionDto(
    val id: Int = 0,
    val mode: String = "",
    @SerialName("work_minutes")
    val workMinutes: Int = 0,
    @SerialName("break_minutes")
    val breakMinutes: Int = 0,
)

@Serializable
data class FocusSessionCompleteRequestDto(
    @SerialName("total_focus_minutes")
    val totalFocusMinutes: Int,
    val distractions: Int,
)

@Serializable
data class FocusWellnessDto(
    @SerialName("is_fatigued")
    val isFatigued: Boolean = false,
    @SerialName("fatigue_level")
    val fatigueLevel: String = "",
    val message: String = "",
    val suggestion: String = "",
)

@Serializable
data class DailyQueueDto(
    val items: List<QueueItemDto> = emptyList(),
    @SerialName("total_estimated_seconds")
    val totalEstimatedSeconds: Int = 0,
    @SerialName("items_remaining")
    val itemsRemaining: Int = 0,
    @SerialName("items_completed")
    val itemsCompleted: Int = 0,
    @SerialName("time_budget_minutes")
    val timeBudgetMinutes: Int = 0,
)

@Serializable
data class QueueItemDto(
    val id: Int = 0,
    val position: Int = 0,
    @SerialName("item_type")
    val itemType: String = "",
    val payload: Map<String, JsonElement> = emptyMap(),
    @SerialName("estimated_seconds")
    val estimatedSeconds: Int = 0,
    @SerialName("completed_at")
    val completedAt: String? = null,
)

@Serializable
data class QueuePreferencesDto(
    @SerialName("time_budget_minutes")
    val timeBudgetMinutes: Int = 30,
)

@Serializable
data class QueuePreferencesRequestDto(
    @SerialName("time_budget_minutes")
    val timeBudgetMinutes: Int,
)

@Serializable
data class MilestonesResponseDto(
    val milestones: List<MilestoneStatusDto> = emptyList(),
)

@Serializable
data class MilestoneStatusDto(
    val id: Int = 0,
    val slug: String = "",
    val name: String = "",
    val description: String = "",
    val category: String = "",
    val status: String = "",
    @SerialName("progress_percentage")
    val progressPercentage: Double = 0.0,
    @SerialName("awarded_at")
    val awardedAt: String? = null,
)

@Serializable
data class ConsistencyDto(
    @SerialName("current_streak")
    val currentStreak: Int = 0,
    @SerialName("longest_streak")
    val longestStreak: Int = 0,
    @SerialName("total_consistent_days")
    val totalConsistentDays: Int = 0,
    @SerialName("last_qualifying_date")
    val lastQualifyingDate: String? = null,
)
