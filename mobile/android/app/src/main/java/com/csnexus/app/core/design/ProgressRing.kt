package com.csnexus.app.core.design

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

private val GoldAccent = Color(0xFFC9A84C)
private val GoldMetallic = Color(0xFFE8C96A)
private val TrackColor = Color(0x14FFFFFF) // subtle track
private val GlowColor = Color(0x66C9A84C) // gold glow

/**
 * Circular progress ring with Gold_Gradient stroke matching the web's readiness ring.
 *
 * Animates from 0 to [value] over DurationSlow (400ms) with decelerate easing.
 * Reduced motion: renders at final value immediately.
 * Accessibility: contentDescription includes value and label.
 */
@Composable
fun ProgressRing(
    value: Int,
    modifier: Modifier = Modifier,
    ringSize: Dp = 160.dp,
    strokeWidth: Dp = 12.dp,
    label: String = "Progress",
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val animatedSweep = remember { Animatable(0f) }
    val targetSweep = (value.coerceIn(0, 100) / 100f) * 360f

    LaunchedEffect(value) {
        if (reducedMotion) {
            animatedSweep.snapTo(targetSweep)
        } else {
            animatedSweep.animateTo(
                targetValue = targetSweep,
                animationSpec = tween(
                    durationMillis = CSNexusMotion.DurationSlow,
                    easing = FastOutSlowInEasing,
                ),
            )
        }
    }

    Canvas(
        modifier = modifier
            .size(ringSize)
            .semantics {
                contentDescription = "$value% $label"
            },
    ) {
        val strokePx = strokeWidth.toPx()
        val padding = strokePx / 2f + 4.dp.toPx() // extra for glow
        val arcSize = Size(size.width - padding * 2, size.height - padding * 2)
        val topLeft = Offset(padding, padding)

        // Track circle
        drawArc(
            color = TrackColor,
            startAngle = 0f,
            sweepAngle = 360f,
            useCenter = false,
            topLeft = topLeft,
            size = arcSize,
            style = Stroke(width = strokePx, cap = StrokeCap.Round),
        )

        // Glow behind the progress arc
        if (animatedSweep.value > 0f) {
            drawArc(
                color = GlowColor,
                startAngle = -90f,
                sweepAngle = animatedSweep.value,
                useCenter = false,
                topLeft = topLeft - Offset(2.dp.toPx(), 2.dp.toPx()),
                size = Size(arcSize.width + 4.dp.toPx(), arcSize.height + 4.dp.toPx()),
                style = Stroke(width = strokePx + 4.dp.toPx(), cap = StrokeCap.Round),
            )
        }

        // Progress arc with gradient stroke
        if (animatedSweep.value > 0f) {
            drawArc(
                brush = Brush.sweepGradient(
                    colors = listOf(GoldAccent, GoldMetallic, GoldAccent),
                ),
                startAngle = -90f,
                sweepAngle = animatedSweep.value,
                useCenter = false,
                topLeft = topLeft,
                size = arcSize,
                style = Stroke(width = strokePx, cap = StrokeCap.Round),
            )
        }
    }
}
