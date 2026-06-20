package com.csnexus.app.feature.motivation.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusOfflineBanner
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.motivation.data.FocusStatsDto
import com.csnexus.app.feature.motivation.data.FocusWellnessDto
import com.csnexus.app.feature.motivation.data.MotivationRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

private const val TotalFocusSessions = 4

// Timer ring colors
private val GoldAccent = Color(0xFFC9A84C)
private val GoldMetallic = Color(0xFFE8C96A)
private val TrackColor = Color(0x14FFFFFF)
private val GlowColor = Color(0x66C9A84C)

@Composable
fun FocusScreen(
    repository: MotivationRepository,
    contentPadding: PaddingValues,
) {
    val scope = rememberCoroutineScope()
    val lifecycleOwner = LocalLifecycleOwner.current
    val syncBannerFlow = repository.focusSyncBanner()
    val syncBanner by (syncBannerFlow?.collectAsState(initial = null) ?: remember { mutableStateOf(null) })
    var snapshot by remember { mutableStateOf(repository.loadFocusState() ?: FocusTimerSnapshot()) }
    var stats by remember { mutableStateOf<FocusStatsDto?>(null) }
    var wellness by remember { mutableStateOf<FocusWellnessDto?>(null) }
    var loadingStats by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var statusMessage by remember { mutableStateOf<String?>(null) }
    var customWork by remember { mutableStateOf(snapshot.customWorkMinutes.toString()) }
    var customBreak by remember { mutableStateOf(snapshot.customBreakMinutes.toString()) }

    fun refreshFocusMeta() {
        loadingStats = true
        scope.launch {
            when (val syncResult = repository.retryPendingFocusCompletions()) {
                is ApiResult.Success -> {
                    if (syncResult.value.syncedCount > 0) {
                        statusMessage = "Synced ${syncResult.value.syncedCount} pending focus sessions."
                    }
                }
                is ApiResult.Failure -> Unit
            }
            when (val result = repository.focusStats()) {
                is ApiResult.Success -> stats = result.value
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
            when (val result = repository.focusWellness()) {
                is ApiResult.Success -> wellness = result.value
                is ApiResult.Failure -> Unit
            }
            loadingStats = false
        }
    }

    fun completeSessionIfNeeded() {
        val sessionId = snapshot.sessionId ?: return
        val totalMinutes = kotlin.math.round(snapshot.totalFocusSeconds / 60.0).toInt()
        scope.launch {
            when (
                val result = repository.completeFocusSession(
                    sessionId = sessionId,
                    totalFocusMinutes = totalMinutes,
                    distractions = snapshot.distractions,
                )
            ) {
                is ApiResult.Success -> {
                    statusMessage = "Focus session saved."
                    refreshFocusMeta()
                }
                is ApiResult.Failure -> {
                    repository.queuePendingFocusCompletion(
                        sessionId = sessionId,
                        totalFocusMinutes = totalMinutes,
                        distractions = snapshot.distractions,
                    )
                    statusMessage = "Offline. Focus session queued for sync."
                }
            }
        }
    }

    fun startSession() {
        val customWorkMinutes = customWork.toIntOrNull()?.coerceIn(5, 120) ?: 25
        val customBreakMinutes = customBreak.toIntOrNull()?.coerceIn(1, 30) ?: 5
        scope.launch {
            val workMinutes = when (snapshot.mode) {
                FocusModePreset.TwentyFiveFive -> 25
                FocusModePreset.FiftyTen -> 50
                FocusModePreset.Custom -> customWorkMinutes
            }
            val breakMinutes = when (snapshot.mode) {
                FocusModePreset.TwentyFiveFive -> 5
                FocusModePreset.FiftyTen -> 10
                FocusModePreset.Custom -> customBreakMinutes
            }
            val sessionId = when (
                val result = repository.startFocusSession(
                    mode = snapshot.mode.name.lowercase(),
                    workMinutes = workMinutes,
                    breakMinutes = breakMinutes,
                )
            ) {
                is ApiResult.Success -> result.value.id
                is ApiResult.Failure -> {
                    errorMessage = result.error.userMessage()
                    null
                }
            }
            snapshot = startFocusSnapshot(
                mode = snapshot.mode,
                customWorkMinutes = customWorkMinutes,
                customBreakMinutes = customBreakMinutes,
                sessionId = sessionId,
            )
        }
    }

    fun resetSession() {
        val sessionId = snapshot.sessionId
        scope.launch {
            if (sessionId != null) {
                when (val result = repository.abandonFocusSession(sessionId)) {
                    is ApiResult.Success -> statusMessage = "Focus session reset."
                    is ApiResult.Failure -> errorMessage = result.error.userMessage()
                }
            }
        }
        snapshot = resetFocusSnapshot(snapshot)
    }

    LaunchedEffect(Unit) {
        refreshFocusMeta()
    }

    LaunchedEffect(snapshot) {
        if (snapshot.timerState == FocusTimerState.IDLE || snapshot.timerState == FocusTimerState.DONE) {
            repository.clearFocusState()
        } else {
            repository.saveFocusState(snapshot)
        }
    }

    LaunchedEffect(snapshot.timerState, snapshot.secondsLeft, snapshot.currentSession) {
        if (snapshot.timerState == FocusTimerState.WORKING || snapshot.timerState == FocusTimerState.BREAK) {
            delay(1000)
            val tick = tickFocusSnapshot(snapshot, totalSessions = TotalFocusSessions)
            snapshot = tick.snapshot
            if (tick.transition == FocusTransition.Completed) {
                completeSessionIfNeeded()
            }
        }
    }

    DisposableEffect(lifecycleOwner, snapshot.timerState) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_STOP && snapshot.timerState == FocusTimerState.WORKING) {
                snapshot = incrementDistraction(snapshot)
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    // Compute timer progress for the ring
    val timerProgress = run {
        val totalSeconds = if (snapshot.timerState == FocusTimerState.BREAK) {
            breakMinutesFor(snapshot) * 60
        } else {
            workMinutesFor(snapshot) * 60
        }
        if (totalSeconds == 0) 0f
        else ((totalSeconds - snapshot.secondsLeft).toFloat() / totalSeconds.toFloat()).coerceIn(0f, 1f)
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
        contentAlignment = Alignment.TopCenter,
    ) {
        Column(
            modifier = Modifier
                .widthIn(max = 600.dp)
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            // Header
            MetallicText(
                text = "Focus mode",
                style = MaterialTheme.typography.headlineLarge,
            )

            if (syncBanner != null) {
                CSNexusOfflineBanner(message = syncBanner!!.message)
            }

            if (snapshot.timerState == FocusTimerState.IDLE) {
                Text(
                    "Stay with one thing for a while. The app keeps the timer state locally and syncs completed sessions when it can.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            // Wellness alert
            if (wellness?.isFatigued == true) {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text(
                            "Wellness alert",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.primary,
                        )
                        Text(wellness?.message.orEmpty())
                        if (wellness?.suggestion == "take_break") {
                            Text(
                                "Try a session with a built-in break.",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }

            // Mode selector — glass toggle buttons
            if (snapshot.timerState == FocusTimerState.IDLE) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    FocusModePreset.entries.forEach { mode ->
                        CSNexusButton(
                            text = mode.label,
                            onClick = { snapshot = snapshot.copy(mode = mode) },
                            variant = if (snapshot.mode == mode) {
                                CSNexusButtonVariant.Primary
                            } else {
                                CSNexusButtonVariant.Ghost
                            },
                            modifier = Modifier.weight(1f),
                        )
                    }
                }
                if (snapshot.mode == FocusModePreset.Custom) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        CSNexusTextField(
                            value = customWork,
                            onValueChange = { customWork = it.filter(Char::isDigit).take(3) },
                            label = "Work minutes",
                            modifier = Modifier.weight(1f),
                        )
                        CSNexusTextField(
                            value = customBreak,
                            onValueChange = { customBreak = it.filter(Char::isDigit).take(2) },
                            label = "Break minutes",
                            modifier = Modifier.weight(1f),
                        )
                    }
                }
            }

            // Timer — 220dp Canvas conic-gradient progress ring + inner glass circle + MetallicText
            Spacer(modifier = Modifier.height(8.dp))
            Box(
                modifier = Modifier.size(220.dp),
                contentAlignment = Alignment.Center,
            ) {
                // Conic-gradient progress ring via Canvas
                Canvas(
                    modifier = Modifier
                        .size(220.dp)
                        .semantics {
                            contentDescription = "${formatFocusClock(snapshot.secondsLeft)} remaining"
                        },
                ) {
                    val strokeWidth = 14.dp.toPx()
                    val padding = strokeWidth / 2f + 4.dp.toPx()
                    val arcSize = Size(size.width - padding * 2, size.height - padding * 2)
                    val topLeft = Offset(padding, padding)
                    val sweepAngle = timerProgress * 360f

                    // Track circle
                    drawArc(
                        color = TrackColor,
                        startAngle = 0f,
                        sweepAngle = 360f,
                        useCenter = false,
                        topLeft = topLeft,
                        size = arcSize,
                        style = Stroke(width = strokeWidth, cap = StrokeCap.Round),
                    )

                    // Glow behind progress arc
                    if (sweepAngle > 0f) {
                        drawArc(
                            color = GlowColor,
                            startAngle = -90f,
                            sweepAngle = sweepAngle,
                            useCenter = false,
                            topLeft = topLeft - Offset(2.dp.toPx(), 2.dp.toPx()),
                            size = Size(arcSize.width + 4.dp.toPx(), arcSize.height + 4.dp.toPx()),
                            style = Stroke(width = strokeWidth + 4.dp.toPx(), cap = StrokeCap.Round),
                        )
                    }

                    // Progress arc with gold gradient
                    if (sweepAngle > 0f) {
                        drawArc(
                            brush = Brush.sweepGradient(
                                colors = listOf(GoldAccent, GoldMetallic, GoldAccent),
                            ),
                            startAngle = -90f,
                            sweepAngle = sweepAngle,
                            useCenter = false,
                            topLeft = topLeft,
                            size = arcSize,
                            style = Stroke(width = strokeWidth, cap = StrokeCap.Round),
                        )
                    }
                }

                // Inner glass circle (190dp)
                GlassMedium(
                    modifier = Modifier.size(190.dp),
                    borderRadius = 95.dp,
                ) {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center,
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            MetallicText(
                                text = formatFocusClock(snapshot.secondsLeft),
                                style = MaterialTheme.typography.displayLarge,
                            )
                            Text(
                                when (snapshot.timerState) {
                                    FocusTimerState.BREAK -> "Break"
                                    FocusTimerState.PAUSED -> "Paused"
                                    FocusTimerState.DONE -> "Done"
                                    FocusTimerState.WORKING -> "Focus"
                                    FocusTimerState.IDLE -> "Ready"
                                },
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.bodyMedium,
                            )
                            if (snapshot.timerState != FocusTimerState.IDLE) {
                                Text(
                                    "Session ${snapshot.currentSession} of $TotalFocusSessions",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    style = MaterialTheme.typography.bodySmall,
                                )
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(8.dp))

            // Controls — context-dependent primary/secondary buttons
            Row(
                horizontalArrangement = Arrangement.spacedBy(10.dp),
                modifier = Modifier.fillMaxWidth(),
            ) {
                when (snapshot.timerState) {
                    FocusTimerState.IDLE -> {
                        CSNexusButton(
                            text = "Start",
                            onClick = ::startSession,
                            modifier = Modifier.weight(1f),
                        )
                    }
                    FocusTimerState.WORKING -> {
                        CSNexusButton(
                            text = "Pause",
                            onClick = { snapshot = pauseFocusSnapshot(snapshot) },
                            variant = CSNexusButtonVariant.Secondary,
                            modifier = Modifier.weight(1f),
                        )
                    }
                    FocusTimerState.PAUSED -> {
                        CSNexusButton(
                            text = "Resume",
                            onClick = { snapshot = resumeFocusSnapshot(snapshot) },
                            modifier = Modifier.weight(1f),
                        )
                    }
                    FocusTimerState.BREAK -> {
                        CSNexusButton(
                            text = "Skip Break",
                            onClick = { snapshot = skipBreak(snapshot, totalSessions = TotalFocusSessions) },
                            variant = CSNexusButtonVariant.Secondary,
                            modifier = Modifier.weight(1f),
                        )
                    }
                    FocusTimerState.DONE -> {
                        CSNexusButton(
                            text = "New Session",
                            onClick = { snapshot = newFocusSessionSnapshot(snapshot) },
                            modifier = Modifier.weight(1f),
                        )
                    }
                }
                if (snapshot.timerState != FocusTimerState.IDLE) {
                    CSNexusButton(
                        text = "Reset",
                        onClick = ::resetSession,
                        variant = CSNexusButtonVariant.Danger,
                    )
                }
            }

            // Distraction notice
            if (snapshot.distractions > 0 && snapshot.timerState != FocusTimerState.IDLE) {
                Text(
                    "App backgrounded ${snapshot.distractions} times during this session.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            if (errorMessage != null) {
                Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
            }
            if (statusMessage != null) {
                Text(statusMessage!!, color = MaterialTheme.colorScheme.primary)
            }

            // Stats — 2×2 grid in GlassMedium card
            if (loadingStats) {
                Text("Loading focus stats...", color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                stats?.let { focusStats ->
                    GlassMedium(modifier = Modifier.fillMaxWidth()) {
                        Column(
                            modifier = Modifier.padding(16.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp),
                        ) {
                            MetallicText(
                                text = "Focus stats",
                                style = MaterialTheme.typography.titleMedium,
                            )
                            // 2×2 grid
                            Row(
                                horizontalArrangement = Arrangement.spacedBy(14.dp),
                                modifier = Modifier.fillMaxWidth(),
                            ) {
                                FocusStat(
                                    label = "Today",
                                    value = "${focusStats.focusMinutesToday} min",
                                    modifier = Modifier.weight(1f),
                                )
                                FocusStat(
                                    label = "Sessions",
                                    value = focusStats.sessionsToday.toString(),
                                    modifier = Modifier.weight(1f),
                                )
                            }
                            Row(
                                horizontalArrangement = Arrangement.spacedBy(14.dp),
                                modifier = Modifier.fillMaxWidth(),
                            ) {
                                FocusStat(
                                    label = "Total hours",
                                    value = "${focusStats.totalFocusHours}",
                                    modifier = Modifier.weight(1f),
                                )
                                FocusStat(
                                    label = "Avg session",
                                    value = "${focusStats.averageSessionMinutes} min",
                                    modifier = Modifier.weight(1f),
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun FocusStat(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
) {
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(label, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall)
        Text(value, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.SemiBold)
    }
}
