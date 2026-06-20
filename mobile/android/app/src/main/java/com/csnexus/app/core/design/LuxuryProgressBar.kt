package com.csnexus.app.core.design

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.snap
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.semantics.progressBarRangeInfo
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp

private val TrackColor = Color(0x08FFFFFF) // glassSubtle
private val GoldAccent = Color(0xFFC9A84C)
private val GoldMetallic = Color(0xFFE8C96A)
private val InsetShadowColor = Color(0x33000000)
private val ShineColor = Color(0x4DFFFFFF) // white at 30% opacity
private val GlowColor = Color(0x66C9A84C) // gold at 0.4 alpha

private val BarHeight = 8.dp

/**
 * A luxury progress bar matching the web's `.progress-luxury` styling.
 *
 * - Track: `glassSubtle` background, full pill radius, inset shadow.
 * - Bar: Gold gradient fill (90deg, accent → metallic), animated shine sweep.
 * - Outer glow: gold shadow at 0.4 alpha behind the filled portion.
 * - Value animation: tween with DurationNormal (250ms).
 * - Reduced motion: no shine sweep, instant width snap.
 *
 * Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7
 */
@Composable
fun LuxuryProgressBar(
    progress: Float,
    modifier: Modifier = Modifier,
    barColorStart: Color = GoldAccent,
    barColorEnd: Color = GoldMetallic,
    glowColor: Color = GlowColor,
) {
    val clampedProgress = progress.coerceIn(0f, 1f)
    val reducedMotion = rememberCSNexusReducedMotion()

    // Animate the progress value change
    val animatedProgress by animateFloatAsState(
        targetValue = clampedProgress,
        animationSpec = if (reducedMotion) snap() else tween(CSNexusMotion.DurationNormal),
        label = "progressAnimation",
    )

    // Shine sweep animation: offset from -0.3 to 1.3 (overshoots to sweep fully across)
    val shineOffset = if (!reducedMotion) {
        val infiniteTransition = rememberInfiniteTransition(label = "shineSweep")
        val offset by infiniteTransition.animateFloat(
            initialValue = -0.3f,
            targetValue = 1.3f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 2000, easing = LinearEasing),
            ),
            label = "shineOffset",
        )
        offset
    } else {
        -1f // off-screen, effectively hidden
    }

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(BarHeight)
            .semantics {
                progressBarRangeInfo = androidx.compose.ui.semantics.ProgressBarRangeInfo(
                    current = clampedProgress,
                    range = 0f..1f,
                )
            },
    ) {
        val barHeight = size.height
        val barWidth = size.width
        val cornerRadius = CornerRadius(barHeight / 2f, barHeight / 2f)

        // Draw gold outer glow behind the filled portion
        val filledWidth = barWidth * animatedProgress
        if (filledWidth > 0f) {
            drawRoundRect(
                color = glowColor,
                topLeft = Offset(-2.dp.toPx(), -2.dp.toPx()),
                size = Size(filledWidth + 4.dp.toPx(), barHeight + 4.dp.toPx()),
                cornerRadius = CornerRadius(
                    (barHeight + 4.dp.toPx()) / 2f,
                    (barHeight + 4.dp.toPx()) / 2f,
                ),
            )
        }

        // Draw track background
        drawRoundRect(
            color = TrackColor,
            topLeft = Offset.Zero,
            size = Size(barWidth, barHeight),
            cornerRadius = cornerRadius,
        )

        // Draw inset shadow on track (top inner shadow)
        drawRoundRect(
            color = InsetShadowColor,
            topLeft = Offset(0f, 0f),
            size = Size(barWidth, barHeight * 0.4f),
            cornerRadius = cornerRadius,
        )

        // Draw the filled bar with gold gradient
        if (filledWidth > 0f) {
            val barPath = Path().apply {
                addRoundRect(
                    RoundRect(
                        rect = Rect(Offset.Zero, Size(filledWidth, barHeight)),
                        topLeft = cornerRadius,
                        topRight = cornerRadius,
                        bottomLeft = cornerRadius,
                        bottomRight = cornerRadius,
                    ),
                )
            }

            clipPath(barPath) {
                // Gold gradient fill (90deg = left to right)
                drawRect(
                    brush = Brush.horizontalGradient(
                        colors = listOf(barColorStart, barColorEnd),
                    ),
                    size = Size(filledWidth, barHeight),
                )

                // Animated shine sweep
                if (!reducedMotion) {
                    drawShineSweep(
                        shineOffset = shineOffset,
                        filledWidth = filledWidth,
                        barHeight = barHeight,
                    )
                }
            }
        }
    }
}

/**
 * Draws a thin white gradient band that sweeps left-to-right across the filled bar.
 */
private fun DrawScope.drawShineSweep(
    shineOffset: Float,
    filledWidth: Float,
    barHeight: Float,
) {
    val shineWidth = filledWidth * 0.3f // shine band is 30% of filled width
    val shineX = shineOffset * filledWidth

    drawRect(
        brush = Brush.horizontalGradient(
            colors = listOf(
                Color.Transparent,
                ShineColor,
                Color.Transparent,
            ),
            startX = shineX - shineWidth / 2f,
            endX = shineX + shineWidth / 2f,
        ),
        topLeft = Offset(0f, 0f),
        size = Size(filledWidth, barHeight),
    )
}
