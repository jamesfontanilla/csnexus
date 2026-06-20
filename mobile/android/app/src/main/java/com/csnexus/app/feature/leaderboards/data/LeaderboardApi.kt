@file:OptIn(kotlinx.serialization.ExperimentalSerializationApi::class)

package com.csnexus.app.feature.leaderboards.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonNames
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

interface LeaderboardApi {
    @GET("v1/leaderboards/global")
    suspend fun xp(): List<LeaderboardEntryDto>

    @GET("v1/tournaments")
    suspend fun tournaments(): List<TournamentDto>

    @POST("v1/tournaments/{id}:join")
    suspend fun joinTournament(@Path("id") tournamentId: Int)

    @GET("v1/tournaments/{id}/leaderboard")
    suspend fun tournamentLeaderboard(@Path("id") tournamentId: Int): List<TournamentLeaderboardEntryDto>
}

@Serializable
data class LeaderboardEntryDto(
    @SerialName("display_name")
    val displayName: String = "Learner",
    val level: Int = 0,
    @JsonNames("xp_window", "score")
    val score: Int = 0,
    val rank: Int = 0,
    val category: String = "",
    @SerialName("is_current_user")
    val isCurrentUser: Boolean = false,
)

@Serializable
data class TournamentDto(
    val id: Int = 0,
    val title: String = "",
    val description: String? = null,
    val category: String? = null,
    @SerialName("starts_at")
    val startsAt: String = "",
    @SerialName("ends_at")
    val endsAt: String = "",
    val status: String = "",
    @SerialName("max_participants")
    val maxParticipants: Int? = null,
    @SerialName("prize_description")
    val prizeDescription: String? = null,
)

@Serializable
data class TournamentLeaderboardEntryDto(
    @SerialName("user_id")
    val userId: Int = 0,
    @JsonNames("xp_earned", "score")
    val xpEarned: Int = 0,
    val rank: Int = 0,
    @SerialName("display_name")
    val displayName: String? = null,
    @SerialName("is_current_user")
    val isCurrentUser: Boolean = false,
)
