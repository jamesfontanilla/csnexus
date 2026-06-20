package com.csnexus.app.feature.settings.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import retrofit2.http.Body
import retrofit2.http.Header
import retrofit2.http.PUT

interface SettingsApi {
    @PUT("v1/goals/me/target")
    suspend fun updateDailyGoal(
        @Body request: DailyGoalRequestDto,
        @Header("Idempotency-Key") idempotencyKey: String? = null,
    ): DailyGoalResponseDto
}

@Serializable
data class DailyGoalRequestDto(
    @SerialName("target_xp")
    val targetXp: Int,
)

@Serializable
data class DailyGoalResponseDto(
    @SerialName("target_xp")
    val targetXp: Int? = null,
    val status: String? = null,
)
