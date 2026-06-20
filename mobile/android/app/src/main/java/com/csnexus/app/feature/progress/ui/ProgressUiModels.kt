package com.csnexus.app.feature.progress.ui

import com.csnexus.app.feature.progress.data.DailyGoalDto
import com.csnexus.app.feature.progress.data.MasteryDto
import com.csnexus.app.feature.progress.data.ProgressSnapshotDto
import com.csnexus.app.feature.progress.data.ReadinessDashboardDto
import java.time.LocalDate
import java.time.OffsetDateTime
import java.time.format.DateTimeParseException
import kotlin.math.roundToInt

enum class ProgressSection(val label: String) {
    Analytics("Analytics"),
    Mastery("Mastery"),
    Goals("Goals"),
    StudyPlan("Study Plan"),
    Readiness("Readiness"),
}

enum class AnalyticsRange(val label: String, val days: Long?) {
    SevenDays("7D", 7),
    FourteenDays("14D", 14),
    ThirtyDays("30D", 30),
    All("All", null),
}

data class AnalyticsTrendPointUi(
    val date: String,
    val label: String,
    val accuracyPercent: Int,
    val sessions: Int,
)

data class AnalyticsHeatmapEntryUi(
    val date: String,
    val label: String,
    val count: Int,
)

data class MasteryLevelCountUi(
    val level: String,
    val count: Int,
)

data class AnalyticsModel(
    val totalSessions: Int,
    val averageAccuracy: Int,
    val readinessPercent: Int,
    val streak: Int,
    val distribution: List<MasteryLevelCountUi>,
    val accuracyTrend: List<AnalyticsTrendPointUi>,
    val consistencyHeatmap: List<AnalyticsHeatmapEntryUi>,
    val strongest: List<MasteryDto>,
    val weakest: List<MasteryDto>,
    val accessibleSummary: String,
)

private val masteryOrder = listOf("BEGINNER", "FAMILIAR", "PROFICIENT", "ADVANCED", "MASTERED")
private val defaultGoalTargets = listOf(25, 50, 100, 150)

fun buildAnalyticsModel(
    xpStreak: Int,
    mastery: List<MasteryDto>,
    weakest: List<MasteryDto>,
    snapshot: ProgressSnapshotDto?,
    readiness: ReadinessDashboardDto?,
    range: AnalyticsRange,
    today: LocalDate = LocalDate.now(),
): AnalyticsModel {
    val filteredMastery = mastery.filter { item ->
        val practicedOn = item.lastPracticedAt.toLocalDateOrNull()
        when {
            range.days == null -> true
            practicedOn == null -> false
            else -> !practicedOn.isBefore(today.minusDays(range.days - 1))
        }
    }
    val source = filteredMastery.ifEmpty { if (range == AnalyticsRange.All) mastery else emptyList() }

    val totalSessions = source.sumOf(MasteryDto::totalAttempts)
    val totalCorrect = source.sumOf(MasteryDto::correctAttempts)
    val averageAccuracy = if (totalSessions > 0) ((totalCorrect.toDouble() / totalSessions) * 100).roundToInt() else 0
    val readinessPercent = when {
        snapshot != null && snapshot.totalSubtopics > 0 ->
            ((snapshot.completedSubtopics.toDouble() / snapshot.totalSubtopics) * 100).roundToInt()
        readiness != null -> readiness.score.roundToInt()
        else -> 0
    }.coerceIn(0, 100)

    val distribution = masteryOrder.mapNotNull { level ->
        val count = source.count { it.masteryLevel.equals(level, ignoreCase = true) }
        if (count == 0) null else MasteryLevelCountUi(level = level, count = count)
    }

    val groupedAccuracy = linkedMapOf<String, Pair<Int, Int>>()
    source.forEach { item ->
        val date = item.lastPracticedAt?.take(10) ?: return@forEach
        val current = groupedAccuracy[date] ?: (0 to 0)
        groupedAccuracy[date] = (current.first + item.correctAttempts) to (current.second + item.totalAttempts)
    }
    val accuracyTrend = groupedAccuracy.entries
        .sortedBy { it.key }
        .takeLast(14)
        .map { (date, counts) ->
            val total = counts.second
            AnalyticsTrendPointUi(
                date = date,
                label = date.drop(5),
                accuracyPercent = if (total > 0) ((counts.first.toDouble() / total) * 100).roundToInt() else 0,
                sessions = total,
            )
        }

    val groupedHeatmap = source.mapNotNull { item ->
        item.lastPracticedAt?.take(10)
    }.groupingBy { it }.eachCount()
    val consistencyHeatmap = groupedHeatmap.entries
        .sortedBy { it.key }
        .takeLast(84)
        .map { (date, count) ->
            AnalyticsHeatmapEntryUi(
                date = date,
                label = date.drop(5),
                count = count,
            )
        }

    val strongest = source.sortedByDescending(MasteryDto::masteryScore).take(5)
    val weakestItems = weakest.take(5)
    val accessibleSummary = buildString {
        append("$totalSessions study sessions")
        append(", $averageAccuracy percent average accuracy")
        append(", readiness $readinessPercent percent")
        append(", streak $xpStreak days")
        if (accuracyTrend.isNotEmpty()) {
            append(", trend points ${accuracyTrend.size}")
        }
    }

    return AnalyticsModel(
        totalSessions = totalSessions,
        averageAccuracy = averageAccuracy,
        readinessPercent = readinessPercent,
        streak = xpStreak,
        distribution = distribution,
        accuracyTrend = accuracyTrend,
        consistencyHeatmap = consistencyHeatmap,
        strongest = strongest,
        weakest = weakestItems,
        accessibleSummary = accessibleSummary,
    )
}

fun goalProgress(goal: DailyGoalDto?): Float {
    if (goal == null || goal.targetXp <= 0) return 0f
    return (goal.currentXp.toFloat() / goal.targetXp.toFloat()).coerceIn(0f, 1f)
}

fun goalTargetOptions(currentTarget: Int): List<Int> {
    return (defaultGoalTargets + listOf(currentTarget))
        .filter { it > 0 }
        .distinct()
        .sorted()
}

fun readinessAccessibleSummary(
    readinessScore: Int,
    confidenceLevel: String,
    passingProbability: Double,
    predictedScore: Double,
): String {
    return buildString {
        append("Readiness $readinessScore percent")
        append(", confidence ${confidenceLevel.ifBlank { "unknown" }}")
        append(", passing probability ${(passingProbability * 100).roundToInt()} percent")
        append(", predicted score ${(predictedScore * 100).roundToInt()} percent")
    }
}

private fun String?.toLocalDateOrNull(): LocalDate? {
    if (this.isNullOrBlank()) return null
    return try {
        OffsetDateTime.parse(this).toLocalDate()
    } catch (_: DateTimeParseException) {
        runCatching { LocalDate.parse(this.take(10)) }.getOrNull()
    }
}
