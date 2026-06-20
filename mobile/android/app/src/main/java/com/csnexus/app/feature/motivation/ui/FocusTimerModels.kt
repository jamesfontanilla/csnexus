package com.csnexus.app.feature.motivation.ui

import kotlinx.serialization.Serializable
import kotlin.math.max

enum class FocusModePreset(val label: String) {
    TwentyFiveFive("25/5"),
    FiftyTen("50/10"),
    Custom("Custom"),
}

@Serializable
enum class FocusTimerState {
    IDLE,
    WORKING,
    BREAK,
    PAUSED,
    DONE,
}

@Serializable
data class FocusTimerSnapshot(
    val mode: FocusModePreset = FocusModePreset.TwentyFiveFive,
    val customWorkMinutes: Int = 25,
    val customBreakMinutes: Int = 5,
    val timerState: FocusTimerState = FocusTimerState.IDLE,
    val pausedFromState: FocusTimerState = FocusTimerState.WORKING,
    val secondsLeft: Int = 25 * 60,
    val currentSession: Int = 1,
    val distractions: Int = 0,
    val totalFocusSeconds: Int = 0,
    val sessionId: Int? = null,
)

data class FocusTickResult(
    val snapshot: FocusTimerSnapshot,
    val transition: FocusTransition = FocusTransition.None,
)

enum class FocusTransition {
    None,
    StartedBreak,
    StartedNextSession,
    Completed,
}

fun workMinutesFor(snapshot: FocusTimerSnapshot): Int {
    return when (snapshot.mode) {
        FocusModePreset.TwentyFiveFive -> 25
        FocusModePreset.FiftyTen -> 50
        FocusModePreset.Custom -> snapshot.customWorkMinutes
    }
}

fun breakMinutesFor(snapshot: FocusTimerSnapshot): Int {
    return when (snapshot.mode) {
        FocusModePreset.TwentyFiveFive -> 5
        FocusModePreset.FiftyTen -> 10
        FocusModePreset.Custom -> snapshot.customBreakMinutes
    }
}

fun initialSecondsFor(snapshot: FocusTimerSnapshot): Int = workMinutesFor(snapshot) * 60

fun startFocusSnapshot(
    mode: FocusModePreset,
    customWorkMinutes: Int,
    customBreakMinutes: Int,
    sessionId: Int?,
): FocusTimerSnapshot {
    val base = FocusTimerSnapshot(
        mode = mode,
        customWorkMinutes = customWorkMinutes,
        customBreakMinutes = customBreakMinutes,
        sessionId = sessionId,
    )
    return base.copy(
        timerState = FocusTimerState.WORKING,
        pausedFromState = FocusTimerState.WORKING,
        secondsLeft = initialSecondsFor(base),
        currentSession = 1,
        distractions = 0,
        totalFocusSeconds = 0,
    )
}

fun pauseFocusSnapshot(snapshot: FocusTimerSnapshot): FocusTimerSnapshot {
    return snapshot.copy(
        timerState = FocusTimerState.PAUSED,
        pausedFromState = if (snapshot.timerState == FocusTimerState.PAUSED) snapshot.pausedFromState else snapshot.timerState,
    )
}

fun resumeFocusSnapshot(snapshot: FocusTimerSnapshot): FocusTimerSnapshot {
    return snapshot.copy(timerState = snapshot.pausedFromState)
}

fun incrementDistraction(snapshot: FocusTimerSnapshot): FocusTimerSnapshot {
    if (snapshot.timerState != FocusTimerState.WORKING) return snapshot
    return snapshot.copy(distractions = snapshot.distractions + 1)
}

fun resetFocusSnapshot(snapshot: FocusTimerSnapshot): FocusTimerSnapshot {
    return snapshot.copy(
        timerState = FocusTimerState.IDLE,
        pausedFromState = FocusTimerState.WORKING,
        secondsLeft = initialSecondsFor(snapshot),
        currentSession = 1,
        distractions = 0,
        totalFocusSeconds = 0,
        sessionId = null,
    )
}

fun newFocusSessionSnapshot(snapshot: FocusTimerSnapshot): FocusTimerSnapshot {
    return resetFocusSnapshot(snapshot)
}

fun skipBreak(snapshot: FocusTimerSnapshot, totalSessions: Int = 4): FocusTimerSnapshot {
    if (snapshot.timerState != FocusTimerState.BREAK) return snapshot
    val nextSession = minOf(snapshot.currentSession + 1, totalSessions)
    return snapshot.copy(
        timerState = FocusTimerState.WORKING,
        pausedFromState = FocusTimerState.WORKING,
        currentSession = nextSession,
        secondsLeft = workMinutesFor(snapshot) * 60,
    )
}

fun tickFocusSnapshot(
    snapshot: FocusTimerSnapshot,
    totalSessions: Int = 4,
): FocusTickResult {
    if (snapshot.timerState != FocusTimerState.WORKING && snapshot.timerState != FocusTimerState.BREAK) {
        return FocusTickResult(snapshot)
    }

    val nextSeconds = max(0, snapshot.secondsLeft - 1)
    val updated = snapshot.copy(
        secondsLeft = nextSeconds,
        totalFocusSeconds = if (snapshot.timerState == FocusTimerState.WORKING) snapshot.totalFocusSeconds + 1 else snapshot.totalFocusSeconds,
    )

    if (nextSeconds > 0) {
        return FocusTickResult(updated)
    }

    return when (snapshot.timerState) {
        FocusTimerState.WORKING -> {
            if (snapshot.currentSession >= totalSessions) {
                FocusTickResult(
                    snapshot = updated.copy(timerState = FocusTimerState.DONE),
                    transition = FocusTransition.Completed,
                )
            } else {
                FocusTickResult(
                    snapshot = updated.copy(
                        timerState = FocusTimerState.BREAK,
                        pausedFromState = FocusTimerState.BREAK,
                        secondsLeft = breakMinutesFor(snapshot) * 60,
                    ),
                    transition = FocusTransition.StartedBreak,
                )
            }
        }
        FocusTimerState.BREAK -> {
            FocusTickResult(
                snapshot = updated.copy(
                    timerState = FocusTimerState.WORKING,
                    pausedFromState = FocusTimerState.WORKING,
                    currentSession = minOf(snapshot.currentSession + 1, totalSessions),
                    secondsLeft = workMinutesFor(snapshot) * 60,
                ),
                transition = FocusTransition.StartedNextSession,
            )
        }
        else -> FocusTickResult(updated)
    }
}

fun formatFocusClock(seconds: Int): String {
    val minutes = seconds / 60
    val remainder = seconds % 60
    return "${minutes.toString().padStart(2, '0')}:${remainder.toString().padStart(2, '0')}"
}
