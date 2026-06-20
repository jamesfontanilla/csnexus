package com.csnexus.app.feature.leaderboards.ui

import com.csnexus.app.feature.leaderboards.data.LeaderboardEntryDto
import com.csnexus.app.feature.leaderboards.data.TournamentDto
import java.time.OffsetDateTime
import java.time.format.DateTimeParseException
import kotlin.math.max

enum class CompetitionSection(val label: String) {
    Global("Leaderboard"),
    Tournaments("Tournaments"),
}

fun leaderboardCategories(entries: List<LeaderboardEntryDto>): List<String> {
    return entries.mapNotNull { entry ->
        entry.category.takeIf(String::isNotBlank)
    }.distinct().sorted()
}

fun filterLeaderboardEntries(
    entries: List<LeaderboardEntryDto>,
    category: String?,
): List<LeaderboardEntryDto> {
    if (category.isNullOrBlank()) return entries
    return entries.filter { it.category.equals(category, ignoreCase = true) }
}

fun tournamentCountdownLabel(
    tournament: TournamentDto,
    nowMillis: Long,
): String {
    val endMillis = tournament.endsAt.toEpochMillisOrNull()
    if (tournament.status.equals("ACTIVE", ignoreCase = true) && endMillis != null) {
        val diffMillis = endMillis - nowMillis
        if (diffMillis <= 0L) return "Ended"
        val hours = diffMillis / (1000L * 60L * 60L)
        val days = hours / 24L
        return if (days > 0L) "${days}d ${hours % 24L}h left" else "${max(1L, hours)}h left"
    }
    return if (tournament.status.equals("ACTIVE", ignoreCase = true)) "Active" else "Upcoming"
}

private fun String.toEpochMillisOrNull(): Long? {
    return try {
        OffsetDateTime.parse(this).toInstant().toEpochMilli()
    } catch (_: DateTimeParseException) {
        null
    }
}
