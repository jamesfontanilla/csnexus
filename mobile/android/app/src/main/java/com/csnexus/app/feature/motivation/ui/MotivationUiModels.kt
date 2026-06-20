package com.csnexus.app.feature.motivation.ui

import com.csnexus.app.feature.motivation.data.MilestoneStatusDto
import com.csnexus.app.feature.motivation.data.OnboardingExamCategory
import com.csnexus.app.feature.motivation.data.QueueItemDto
import java.time.LocalDate
import java.time.OffsetDateTime
import java.time.format.DateTimeParseException
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.intOrNull

data class OnboardingValidationResult(
    val errorMessage: String? = null,
    val warningMessage: String? = null,
)

fun validateOnboardingExamDate(
    examDate: String,
    today: LocalDate = LocalDate.now(),
): OnboardingValidationResult {
    if (examDate.isBlank()) {
        return OnboardingValidationResult(errorMessage = "Please select an exam date")
    }
    val selectedDate = runCatching { LocalDate.parse(examDate) }.getOrNull()
        ?: return OnboardingValidationResult(errorMessage = "Exam date must use YYYY-MM-DD")
    val daysUntilExam = java.time.temporal.ChronoUnit.DAYS.between(today, selectedDate)
    if (daysUntilExam < 1) {
        return OnboardingValidationResult(errorMessage = "Exam date must be in the future")
    }
    if (daysUntilExam > 365) {
        return OnboardingValidationResult(errorMessage = "Exam date must be within 365 days")
    }
    if (daysUntilExam < 7) {
        val daysLabel = if (daysUntilExam == 1L) "day" else "days"
        return OnboardingValidationResult(warningMessage = "Your exam is in $daysUntilExam $daysLabel. We'll create an intensive plan.")
    }
    return OnboardingValidationResult()
}

fun onboardingStepLabels(): List<String> = listOf("Date", "Category", "Time")

sealed interface QueueDestination {
    data class Lesson(val subtopicId: Int) : QueueDestination
    data class Quiz(val subtopicId: Int) : QueueDestination
    data class Flashcards(val deckIds: List<Int>) : QueueDestination
    data object Unknown : QueueDestination
}

fun queueDestination(item: QueueItemDto): QueueDestination {
    return when (item.itemType) {
        "flashcard_review" -> QueueDestination.Flashcards(deckIds = item.payload["deck_ids"].jsonIntList())
        "quiz_practice" -> item.payload["subtopic_id"].jsonInt()?.let(QueueDestination::Quiz) ?: QueueDestination.Unknown
        "new_content" -> item.payload["subtopic_id"].jsonInt()?.let(QueueDestination::Lesson) ?: QueueDestination.Unknown
        else -> QueueDestination.Unknown
    }
}

fun queueItemLabel(itemType: String): String {
    return when (itemType) {
        "flashcard_review" -> "Flashcard Review"
        "quiz_practice" -> "Quiz Practice"
        "new_content" -> "New Lesson"
        else -> itemType.replace('_', ' ').replaceFirstChar { it.titlecase() }
    }
}

fun queueItemIcon(itemType: String): String {
    return when (itemType) {
        "flashcard_review" -> "Cards"
        "quiz_practice" -> "Quiz"
        "new_content" -> "Lesson"
        else -> "Task"
    }
}

fun queueDurationLabel(totalSeconds: Int): String {
    if (totalSeconds < 60) return "${totalSeconds}s"
    return "${kotlin.math.round(totalSeconds / 60.0).toInt()} min"
}

fun groupMilestones(milestones: List<MilestoneStatusDto>): List<Pair<String, List<MilestoneStatusDto>>> {
    return milestones
        .groupBy { it.category.ifBlank { "general" } }
        .toSortedMap()
        .map { it.key to it.value.sortedBy { milestone -> milestone.name } }
}

fun milestoneCategoryLabel(category: String): String {
    return when (category) {
        "mastery" -> "Subject Mastery"
        "readiness" -> "Exam Readiness"
        "recovery" -> "Comeback and Resilience"
        else -> category.replace('_', ' ').replaceFirstChar { it.titlecase() }
    }
}

fun milestoneStatusLabel(status: String): String {
    return when (status) {
        "earned" -> "Earned"
        "in_progress" -> "In Progress"
        "locked" -> "Locked"
        else -> status.replace('_', ' ').replaceFirstChar { it.titlecase() }
    }
}

fun onboardingExamCategoryOptions(): List<OnboardingExamCategory> =
    listOf(OnboardingExamCategory.Professional, OnboardingExamCategory.SubProfessional)

fun onboardingTimeBudgets(): List<Int> = listOf(15, 30, 60)

fun formatFriendlyDate(raw: String?): String {
    if (raw.isNullOrBlank()) return "-"
    return try {
        OffsetDateTime.parse(raw).toLocalDate().toString()
    } catch (_: DateTimeParseException) {
        runCatching { LocalDate.parse(raw.take(10)).toString() }.getOrElse { raw.take(10) }
    }
}

private fun JsonElement?.jsonInt(): Int? {
    return when (this) {
        is JsonPrimitive -> intOrNull
        else -> null
    }
}

private fun JsonElement?.jsonIntList(): List<Int> {
    return when (this) {
        is JsonArray -> this.mapNotNull { element ->
            (element as? JsonPrimitive)?.intOrNull
        }
        else -> emptyList()
    }
}
