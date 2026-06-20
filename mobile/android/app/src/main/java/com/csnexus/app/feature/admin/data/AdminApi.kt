package com.csnexus.app.feature.admin.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.Path
import retrofit2.http.Query

// ── DTOs ─────────────────────────────────────────────────────────────────────

@Serializable
data class WeakSubtopicDto(
    @SerialName("subtopic_id") val subtopicId: Int,
    val title: String,
    @SerialName("avg_score") val avgScore: Double,
)

@Serializable
data class AdminAnalyticsDto(
    @SerialName("total_users") val totalUsers: Int,
    @SerialName("verified_users") val verifiedUsers: Int,
    @SerialName("banned_users") val bannedUsers: Int,
    @SerialName("total_lessons_completed") val totalLessonsCompleted: Int,
    @SerialName("total_quiz_attempts") val totalQuizAttempts: Int,
    @SerialName("total_mock_attempts") val totalMockAttempts: Int,
    @SerialName("mock_pass_rate") val mockPassRate: Double,
    @SerialName("weakest_subtopics") val weakestSubtopics: List<WeakSubtopicDto> = emptyList(),
)

@Serializable
data class AdminUserDto(
    val id: Int,
    val email: String,
    @SerialName("display_name") val displayName: String,
    val username: String? = null,
    @SerialName("google_id") val googleId: String? = null,
    val role: String,
    @SerialName("account_state") val accountState: String? = null,
    @SerialName("is_banned") val isBanned: Boolean = false,
)

@Serializable
data class AdminUsersResponseDto(
    val items: List<AdminUserDto>,
    val total: Int,
)

@Serializable
data class AdminUpdateUserRequestDto(
    @SerialName("is_banned") val isBanned: Boolean,
)

// ── Retrofit interface ────────────────────────────────────────────────────────

interface AdminApi {
    @GET("v1/admin/analytics")
    suspend fun analytics(): AdminAnalyticsDto

    @GET("v1/admin/users")
    suspend fun users(
        @Query("limit") limit: Int = 50,
        @Query("search") search: String? = null,
    ): AdminUsersResponseDto

    @PATCH("v1/admin/users/{userId}")
    suspend fun updateUser(
        @Path("userId") userId: Int,
        @Body request: AdminUpdateUserRequestDto,
    ): AdminUserDto

    @DELETE("v1/admin/users/{userId}")
    suspend fun deleteUser(@Path("userId") userId: Int)
}
