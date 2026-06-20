package com.csnexus.app.core.design

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay

// Toast variant colors at 90% opacity
private val ToastSuccessBg = Color(0xE68FBC8F) // sage green 90%
private val ToastErrorBg = Color(0xE6D4645C)   // terracotta 90%
private val ToastInfoBg = Color(0xE6C9A84C)    // gold 90%

// Border colors (slightly lighter variant at 40% opacity)
private val ToastSuccessBorder = Color(0x668FBC8F)
private val ToastErrorBorder = Color(0x66D4645C)
private val ToastInfoBorder = Color(0x66C9A84C)

// Progress indicator track (dimmed variant)
private val ToastSuccessProgress = Color(0xCC8FBC8F)
private val ToastErrorProgress = Color(0xCCD4645C)
private val ToastInfoProgress = Color(0xCCC9A84C)

private const val AUTO_DISMISS_MS = 4000L
private val ToastMaxWidth = 360.dp
private val ToastBorderRadius = 12.dp // radius-md

/**
 * Visual variant for the glass toast notification.
 */
enum class GlassToastVariant {
    Success,
    Error,
    Info,
}

/**
 * Immutable state representing a single toast message.
 */
data class GlassToastState(
    val message: String,
    val variant: GlassToastVariant,
    val id: Long = System.currentTimeMillis(),
)

/**
 * A premium glass-styled toast notification matching the web's toast component.
 *
 * Features:
 * - Glass background with blur (API 31+) and shadow-depth
 * - Slide-in from right with spring easing (or fade-only under reduced motion)
 * - Auto-dismiss after 4000ms with a depleting progress indicator
 * - Accessibility: liveRegion Assertive for errors, Polite for others
 *
 * @param state The toast state to display, or null to hide.
 * @param onDismiss Callback invoked when the toast should be removed.
 */
@Composable
fun GlassToast(
    state: GlassToastState?,
    onDismiss: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val performanceTier = LocalCSNexusPerformanceTier.current
    val visible = state != null

    // Auto-dismiss timer
    LaunchedEffect(state?.id) {
        if (state != null) {
            delay(AUTO_DISMISS_MS)
            onDismiss()
        }
    }

    AnimatedVisibility(
        visible = visible,
        enter = if (reducedMotion) {
            fadeIn(animationSpec = tween(CSNexusMotion.DurationFast))
        } else {
            slideInHorizontally(
                animationSpec = spring(
                    dampingRatio = Spring.DampingRatioMediumBouncy,
                    stiffness = Spring.StiffnessMediumLow,
                ),
                initialOffsetX = { fullWidth -> fullWidth },
            ) + fadeIn(animationSpec = tween(CSNexusMotion.DurationFast))
        },
        exit = if (reducedMotion) {
            fadeOut(animationSpec = tween(CSNexusMotion.DurationFast))
        } else {
            slideOutHorizontally(
                animationSpec = tween(CSNexusMotion.DurationFast),
                targetOffsetX = { fullWidth -> fullWidth },
            ) + fadeOut(animationSpec = tween(CSNexusMotion.DurationFast))
        },
        modifier = modifier,
    ) {
        state?.let { toast ->
            GlassToastContent(
                state = toast,
                performanceTier = performanceTier,
            )
        }
    }
}

@Composable
private fun GlassToastContent(
    state: GlassToastState,
    performanceTier: PerformanceTier,
) {
    val shape = RoundedCornerShape(ToastBorderRadius)
    val backgroundColor = when (state.variant) {
        GlassToastVariant.Success -> ToastSuccessBg
        GlassToastVariant.Error -> ToastErrorBg
        GlassToastVariant.Info -> ToastInfoBg
    }
    val borderColor = when (state.variant) {
        GlassToastVariant.Success -> ToastSuccessBorder
        GlassToastVariant.Error -> ToastErrorBorder
        GlassToastVariant.Info -> ToastInfoBorder
    }
    val progressColor = when (state.variant) {
        GlassToastVariant.Success -> ToastSuccessProgress
        GlassToastVariant.Error -> ToastErrorProgress
        GlassToastVariant.Info -> ToastInfoProgress
    }
    val liveRegionMode = when (state.variant) {
        GlassToastVariant.Error -> LiveRegionMode.Assertive
        else -> LiveRegionMode.Polite
    }

    // Depleting progress animation
    val progress = remember { Animatable(1f) }
    LaunchedEffect(state.id) {
        progress.snapTo(1f)
        progress.animateTo(
            targetValue = 0f,
            animationSpec = tween(
                durationMillis = AUTO_DISMISS_MS.toInt(),
                easing = LinearEasing,
            ),
        )
    }

    Column(
        modifier = Modifier
            .widthIn(max = ToastMaxWidth)
            .semantics { liveRegion = liveRegionMode }
            .shadowDepth()
            .clip(shape)
            .background(backgroundColor, shape)
            .border(1.dp, borderColor, shape),
    ) {
        // Message content
        Text(
            text = state.message,
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp),
        )

        // Depleting progress indicator at bottom
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(3.dp)
                .drawBehind {
                    val barWidth = size.width * progress.value
                    drawRoundRect(
                        color = progressColor,
                        topLeft = Offset.Zero,
                        size = Size(barWidth, size.height),
                        cornerRadius = CornerRadius(1.5f, 1.5f),
                    )
                },
        )
    }
}
