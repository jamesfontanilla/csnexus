package com.csnexus.app.feature.motivation.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class FocusTimerModelsTest {
    @Test
    fun workingTickTransitionsIntoBreak() {
        val snapshot = FocusTimerSnapshot(
            mode = FocusModePreset.TwentyFiveFive,
            timerState = FocusTimerState.WORKING,
            pausedFromState = FocusTimerState.WORKING,
            secondsLeft = 1,
            currentSession = 1,
            totalFocusSeconds = 24,
        )

        val result = tickFocusSnapshot(snapshot, totalSessions = 4)

        assertEquals(FocusTransition.StartedBreak, result.transition)
        assertEquals(FocusTimerState.BREAK, result.snapshot.timerState)
        assertEquals(5 * 60, result.snapshot.secondsLeft)
        assertEquals(25, result.snapshot.totalFocusSeconds)
    }

    @Test
    fun breakTickTransitionsIntoNextSession() {
        val snapshot = FocusTimerSnapshot(
            mode = FocusModePreset.FiftyTen,
            timerState = FocusTimerState.BREAK,
            pausedFromState = FocusTimerState.BREAK,
            secondsLeft = 1,
            currentSession = 2,
        )

        val result = tickFocusSnapshot(snapshot, totalSessions = 4)

        assertEquals(FocusTransition.StartedNextSession, result.transition)
        assertEquals(FocusTimerState.WORKING, result.snapshot.timerState)
        assertEquals(3, result.snapshot.currentSession)
        assertEquals(50 * 60, result.snapshot.secondsLeft)
    }

    @Test
    fun finalWorkingTickCompletesSession() {
        val snapshot = FocusTimerSnapshot(
            timerState = FocusTimerState.WORKING,
            pausedFromState = FocusTimerState.WORKING,
            secondsLeft = 1,
            currentSession = 4,
            totalFocusSeconds = 99,
        )

        val result = tickFocusSnapshot(snapshot, totalSessions = 4)

        assertEquals(FocusTransition.Completed, result.transition)
        assertEquals(FocusTimerState.DONE, result.snapshot.timerState)
        assertEquals(100, result.snapshot.totalFocusSeconds)
    }

    @Test
    fun pauseResumeAndSkipBreakPreserveSessionState() {
        val working = startFocusSnapshot(
            mode = FocusModePreset.Custom,
            customWorkMinutes = 40,
            customBreakMinutes = 7,
            sessionId = 3,
        )

        val paused = pauseFocusSnapshot(working)
        val resumed = resumeFocusSnapshot(paused)
        val skipped = skipBreak(
            resumed.copy(timerState = FocusTimerState.BREAK, currentSession = 1),
            totalSessions = 4,
        )

        assertEquals(FocusTimerState.PAUSED, paused.timerState)
        assertEquals(FocusTimerState.WORKING, resumed.timerState)
        assertEquals(FocusTimerState.WORKING, skipped.timerState)
        assertEquals(2, skipped.currentSession)
        assertEquals(40 * 60, skipped.secondsLeft)
        assertTrue(formatFocusClock(skipped.secondsLeft).startsWith("40:"))
    }
}
