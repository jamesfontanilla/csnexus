package com.csnexus.app.feature.mockexam.data

import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path

interface MockExamApi {
    @POST("v1/mock-exams/attempts")
    suspend fun start(): MockExamAttemptDto

    @GET("v1/mock-exams/attempts/{attemptId}")
    suspend fun attempt(@Path("attemptId") attemptId: Int): MockExamAttemptDto

    @PATCH("v1/mock-exams/attempts/{attemptId}/answers/{questionId}")
    suspend fun answer(
        @Path("attemptId") attemptId: Int,
        @Path("questionId") questionId: Int,
        @Body request: MockExamAnswerRequestDto,
    )

    @POST("v1/mock-exams/attempts/{attemptId}:report-focus-loss")
    suspend fun reportFocusLoss(
        @Path("attemptId") attemptId: Int,
        @Body request: MockExamFocusLossRequestDto,
    )

    @POST("v1/mock-exams/attempts/{attemptId}:submit")
    suspend fun submit(
        @Path("attemptId") attemptId: Int,
        @Body request: MockExamSubmitRequestDto = MockExamSubmitRequestDto(),
    ): MockExamSubmittedDto

    @GET("v1/mock-analytics/{attemptId}")
    suspend fun diagnostic(@Path("attemptId") attemptId: Int): MockDiagnosticDto

    @GET("v1/mock-analytics/{attemptId}/recommendations")
    suspend fun recommendations(@Path("attemptId") attemptId: Int): MockRecommendationsDto

    @POST("v1/mock-analytics/{attemptId}/recommendations/:accept")
    suspend fun acceptRecommendation(@Path("attemptId") attemptId: Int): MockRecommendationDto

    @GET("v1/mock-analytics/prediction")
    suspend fun prediction(): MockPredictionDto
}

@Serializable
data class MockExamAttemptDto(
    val id: Int = 0,
    @SerialName("attempt_id")
    val attemptId: Int = id,
    val status: String = "IN_PROGRESS",
    val questions: List<QuizQuestionDto> = emptyList(),
    @SerialName("time_limit_minutes")
    val timeLimitMinutes: Int = 180,
    @SerialName("remaining_seconds")
    val remainingSeconds: Int? = null,
    @SerialName("nav_policy")
    val navPolicy: String = "FREE_NAVIGATION",
)

@Serializable
data class MockExamSubmittedDto(
    val id: Int = 0,
    @SerialName("attempt_id")
    val attemptId: Int = id,
    val status: String = "SUBMITTED",
    val score: Int = 0,
    @SerialName("max_score")
    val maxScore: Int = 0,
    val percentage: Double = 0.0,
    val passed: Boolean? = null,
    @SerialName("awarded_xp")
    val awardedXp: Int = 0,
    val questions: List<QuizQuestionDto> = emptyList(),
    @SerialName("per_module_breakdown")
    val perModuleBreakdown: List<MockModuleBreakdownDto> = emptyList(),
    @SerialName("weakness_summary")
    val weaknessSummary: List<MockWeaknessSummaryDto> = emptyList(),
)

@Serializable
data class MockModuleBreakdownDto(
    @SerialName("module_id")
    val moduleId: Int = 0,
    val title: String = "",
    @SerialName("module_title")
    val moduleTitle: String = title,
    val score: Int = 0,
    val max: Int = 0,
    val pct: Double = 0.0,
)

@Serializable
data class MockWeaknessSummaryDto(
    @SerialName("module_id")
    val moduleId: Int = 0,
    @SerialName("module_title")
    val moduleTitle: String = "",
    val pct: Double = 0.0,
    val percentage: Double = pct,
)

@Serializable
data class MockExamAnswerRequestDto(
    val selected: String,
)

@Serializable
data class MockExamFocusLossRequestDto(
    val kind: String,
    val at: String,
)

@Serializable
data class MockExamSubmitRequestDto(
    val mode: String = "MANUAL",
)

@Serializable
data class MockDiagnosticDto(
    @SerialName("total_score")
    val totalScore: Double = 0.0,
    @SerialName("subtopic_breakdowns")
    val subtopicBreakdowns: List<MockSubtopicBreakdownDto> = emptyList(),
    @SerialName("highest_impact_areas")
    val highestImpactAreas: List<MockSubtopicBreakdownDto> = emptyList(),
    @SerialName("regression_alerts")
    val regressionAlerts: List<MockRegressionAlertDto> = emptyList(),
    @SerialName("difficulty_performance")
    val difficultyPerformance: MockDifficultyPerformanceDto = MockDifficultyPerformanceDto(),
)

@Serializable
data class MockSubtopicBreakdownDto(
    @SerialName("subtopic_id")
    val subtopicId: Int = 0,
    @SerialName("subtopic_name")
    val subtopicName: String = "",
    @SerialName("questions_attempted")
    val questionsAttempted: Int = 0,
    @SerialName("questions_correct")
    val questionsCorrect: Int = 0,
    @SerialName("points_lost")
    val pointsLost: Int = 0,
    @SerialName("avg_seconds_per_question")
    val avgSecondsPerQuestion: Double = 0.0,
    @SerialName("accuracy_percentage")
    val accuracyPercentage: Double = 0.0,
)

@Serializable
data class MockRegressionAlertDto(
    @SerialName("subtopic_id")
    val subtopicId: Int = 0,
    @SerialName("decline_percentage_points")
    val declinePercentagePoints: Double = 0.0,
)

@Serializable
data class MockDifficultyPerformanceDto(
    val easy: Double? = null,
    val medium: Double? = null,
    val hard: Double? = null,
)

@Serializable
data class MockPredictionDto(
    @SerialName("lower_bound")
    val lowerBound: Double? = null,
    val midpoint: Double? = null,
    @SerialName("upper_bound")
    val upperBound: Double? = null,
    @SerialName("confidence_level")
    val confidenceLevel: String? = null,
    val message: String? = null,
)

@Serializable
data class MockRecommendationDto(
    val id: Int = 0,
    @SerialName("subtopic_id")
    val subtopicId: Int = 0,
    @SerialName("subtopic_name")
    val subtopicName: String = "",
    @SerialName("current_accuracy")
    val currentAccuracy: Double = 0.0,
    @SerialName("target_accuracy")
    val targetAccuracy: Double = 80.0,
    @SerialName("estimated_point_gain")
    val estimatedPointGain: Double = 0.0,
    @SerialName("recommended_action")
    val recommendedAction: String = "",
    @SerialName("formatted_string")
    val formattedString: String = "",
    @SerialName("accepted_at")
    val acceptedAt: String? = null,
)

@Serializable
data class MockRecommendationsDto(
    val recommendations: List<MockRecommendationDto> = emptyList(),
)
