package com.csnexus.app.feature.flashcards.ui

import com.csnexus.app.feature.flashcards.data.ConfidenceLevel
import com.csnexus.app.feature.flashcards.data.ResponseType
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class FlashcardStudyUtilsTest {
    @Test
    fun similarityTreatsCloseAnswersAsHighConfidence() {
        val similarity = flashcardSimilarity("Constitution", "constitution")

        assertTrue(similarity >= 0.99)
    }

    @Test
    fun confidenceChoiceMapsSimilarityToSpacedRepetitionBucket() {
        val mastered = confidenceChoiceForSimilarity(similarity = 1.0, correct = true)
        val unsure = confidenceChoiceForSimilarity(similarity = 0.65, correct = true)
        val forgot = confidenceChoiceForSimilarity(similarity = 0.4, correct = false)

        assertEquals(ConfidenceLevel.Mastered, mastered.confidence)
        assertEquals(ConfidenceLevel.Unsure, unsure.confidence)
        assertEquals(ResponseType.Forgot, forgot.responseType)
    }

    @Test
    fun progressSnapshotTracksReviewedAndCorrectCounts() {
        val snapshot = StudyProgressSnapshot()
            .afterResponse(ResponseType.Remembered)
            .afterResponse(ResponseType.Forgot)

        assertEquals(2, snapshot.reviewed)
        assertEquals(1, snapshot.correct)
    }
}
