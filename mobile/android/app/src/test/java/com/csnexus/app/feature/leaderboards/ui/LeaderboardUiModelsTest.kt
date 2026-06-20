package com.csnexus.app.feature.leaderboards.ui

import com.csnexus.app.feature.leaderboards.data.LeaderboardEntryDto
import com.csnexus.app.feature.leaderboards.data.TournamentDto
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class LeaderboardUiModelsTest {
    @Test
    fun filtersLeaderboardByCategory() {
        val entries = listOf(
            LeaderboardEntryDto(displayName = "A", category = "Grammar"),
            LeaderboardEntryDto(displayName = "B", category = "Reading"),
            LeaderboardEntryDto(displayName = "C", category = "Grammar"),
        )

        val filtered = filterLeaderboardEntries(entries, "Grammar")

        assertEquals(2, filtered.size)
        assertTrue(filtered.all { it.category == "Grammar" })
    }

    @Test
    fun countdownShowsDaysAndHoursForActiveTournament() {
        val tournament = TournamentDto(
            id = 4,
            title = "Weekend Push",
            status = "ACTIVE",
            endsAt = "2026-06-10T12:00:00Z",
        )

        val label = tournamentCountdownLabel(
            tournament = tournament,
            nowMillis = java.time.OffsetDateTime.parse("2026-06-08T10:00:00Z").toInstant().toEpochMilli(),
        )

        assertEquals("2d 2h left", label)
    }
}
