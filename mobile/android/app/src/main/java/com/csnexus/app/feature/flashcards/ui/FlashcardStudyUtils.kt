package com.csnexus.app.feature.flashcards.ui

import com.csnexus.app.feature.flashcards.data.ConfidenceLevel
import com.csnexus.app.feature.flashcards.data.ResponseType
import java.util.Locale
import kotlin.math.max

data class StudyConfidenceChoice(
    val confidence: ConfidenceLevel,
    val responseType: ResponseType,
)

data class StudyProgressSnapshot(
    val reviewed: Int = 0,
    val correct: Int = 0,
)

fun flashcardSimilarity(left: String, right: String): Double {
    val a = left.trim().lowercase(Locale.US)
    val b = right.trim().lowercase(Locale.US)
    if (a == b) return 1.0
    if (a.isEmpty() && b.isEmpty()) return 1.0

    val width = b.length + 1
    val height = a.length + 1
    val matrix = Array(height) { IntArray(width) }

    for (i in 0 until height) matrix[i][0] = i
    for (j in 0 until width) matrix[0][j] = j

    for (i in 1 until height) {
        for (j in 1 until width) {
            val cost = if (a[i - 1] == b[j - 1]) 0 else 1
            matrix[i][j] = minOf(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost,
            )
        }
    }

    val maxLen = max(a.length, b.length).coerceAtLeast(1)
    return 1.0 - (matrix[a.length][b.length].toDouble() / maxLen.toDouble())
}

fun confidenceChoiceForSimilarity(similarity: Double, correct: Boolean): StudyConfidenceChoice {
    return when {
        !correct -> StudyConfidenceChoice(ConfidenceLevel.Guessed, ResponseType.Forgot)
        similarity >= 0.99 -> StudyConfidenceChoice(ConfidenceLevel.Mastered, ResponseType.Remembered)
        similarity >= 0.8 -> StudyConfidenceChoice(ConfidenceLevel.Confident, ResponseType.Remembered)
        else -> StudyConfidenceChoice(ConfidenceLevel.Unsure, ResponseType.Remembered)
    }
}

fun StudyProgressSnapshot.afterResponse(responseType: ResponseType): StudyProgressSnapshot {
    return copy(
        reviewed = reviewed + 1,
        correct = correct + if (responseType == ResponseType.Remembered) 1 else 0,
    )
}

fun formatFlashcardDuration(seconds: Int): String {
    val minutes = seconds / 60
    val remainingSeconds = seconds % 60
    return "${minutes}m ${remainingSeconds}s"
}
