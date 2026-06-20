package com.csnexus.app.feature.motivation.ui

import com.csnexus.app.feature.motivation.data.MilestoneStatusDto
import com.csnexus.app.feature.motivation.data.QueueItemDto
import kotlinx.serialization.json.JsonPrimitive
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class MotivationUiModelsTest {
    @Test
    fun onboardingValidationReturnsUrgencyWarningForNearExam() {
        val result = validateOnboardingExamDate(
            examDate = "2026-06-10",
            today = java.time.LocalDate.of(2026, 6, 8),
        )

        assertEquals(null, result.errorMessage)
        assertTrue(result.warningMessage?.contains("intensive plan") == true)
    }

    @Test
    fun queueDestinationMapsQuizAndFlashcardRoutes() {
        val quiz = QueueItemDto(
            id = 1,
            itemType = "quiz_practice",
            payload = mapOf("subtopic_id" to JsonPrimitive(42)),
        )
        val flashcards = QueueItemDto(
            id = 2,
            itemType = "flashcard_review",
            payload = mapOf(
                "deck_ids" to kotlinx.serialization.json.buildJsonArray {
                    add(JsonPrimitive(4))
                    add(JsonPrimitive(9))
                },
            ),
        )

        assertEquals(QueueDestination.Quiz(42), queueDestination(quiz))
        assertEquals(QueueDestination.Flashcards(listOf(4, 9)), queueDestination(flashcards))
    }

    @Test
    fun milestonesGroupByCategoryAndKeepLabels() {
        val grouped = groupMilestones(
            listOf(
                MilestoneStatusDto(id = 1, name = "Ready", category = "readiness", status = "earned"),
                MilestoneStatusDto(id = 2, name = "Mastered", category = "mastery", status = "in_progress"),
            ),
        )

        assertEquals(2, grouped.size)
        assertEquals("mastery", grouped.first().first)
        assertEquals("Subject Mastery", milestoneCategoryLabel("mastery"))
        assertEquals("In Progress", milestoneStatusLabel("in_progress"))
    }
}
