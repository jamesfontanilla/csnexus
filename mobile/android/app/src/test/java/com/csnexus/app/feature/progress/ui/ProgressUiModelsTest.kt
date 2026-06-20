package com.csnexus.app.feature.progress.ui

import com.csnexus.app.feature.progress.data.MasteryDto
import com.csnexus.app.feature.progress.data.ProgressSnapshotDto
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.time.LocalDate

class ProgressUiModelsTest {
    @Test
    fun analyticsModelAppliesSelectedRange() {
        val today = LocalDate.of(2026, 6, 8)
        val recent = MasteryDto(
            subtopicId = 1,
            subtopicTitle = "Subject Verb Agreement",
            masteryLevel = "PROFICIENT",
            masteryScore = 0.82,
            totalAttempts = 10,
            correctAttempts = 8,
            lastPracticedAt = "2026-06-07T09:00:00Z",
        )
        val older = MasteryDto(
            subtopicId = 2,
            subtopicTitle = "Tenses",
            masteryLevel = "BEGINNER",
            masteryScore = 0.40,
            totalAttempts = 20,
            correctAttempts = 10,
            lastPracticedAt = "2026-05-01T09:00:00Z",
        )

        val model = buildAnalyticsModel(
            xpStreak = 5,
            mastery = listOf(recent, older),
            weakest = listOf(older),
            snapshot = ProgressSnapshotDto(totalSubtopics = 10, completedSubtopics = 6),
            readiness = null,
            range = AnalyticsRange.SevenDays,
            today = today,
        )

        assertEquals(10, model.totalSessions)
        assertEquals(80, model.averageAccuracy)
        assertEquals(60, model.readinessPercent)
        assertEquals(1, model.accuracyTrend.size)
        assertEquals("06-07", model.accuracyTrend.single().label)
        assertTrue(model.accessibleSummary.contains("10 study sessions"))
    }

    @Test
    fun goalTargetOptionsIncludeServerOwnedTarget() {
        assertEquals(listOf(25, 50, 75, 100, 150), goalTargetOptions(75))
    }

    @Test
    fun readinessSummaryIsAccessibleAndConcrete() {
        val summary = readinessAccessibleSummary(
            readinessScore = 84,
            confidenceLevel = "high",
            passingProbability = 0.81,
            predictedScore = 0.78,
        )

        assertTrue(summary.contains("Readiness 84 percent"))
        assertTrue(summary.contains("confidence high"))
        assertTrue(summary.contains("passing probability 81 percent"))
        assertTrue(summary.contains("predicted score 78 percent"))
    }
}
