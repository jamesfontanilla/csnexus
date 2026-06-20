package com.csnexus.app.feature.leaderboards.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall

class LeaderboardRepository(
    private val leaderboardApi: LeaderboardApi,
) {
    suspend fun xp(): ApiResult<List<LeaderboardEntryDto>> = safeApiCall { leaderboardApi.xp() }
    suspend fun tournaments(): ApiResult<List<TournamentDto>> = safeApiCall { leaderboardApi.tournaments() }
    suspend fun joinTournament(tournamentId: Int): ApiResult<Unit> = safeApiCall { leaderboardApi.joinTournament(tournamentId) }
    suspend fun tournamentLeaderboard(tournamentId: Int): ApiResult<List<TournamentLeaderboardEntryDto>> = safeApiCall {
        leaderboardApi.tournamentLeaderboard(tournamentId)
    }
}
