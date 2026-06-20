package com.csnexus.app.core.design

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor

private val Gold = Color(0xFFC9A84C)

/**
 * Creates a shimmer brush that sweeps left-to-right over a 2-second cycle.
 * 
 * The gradient uses glassSubtle → gold at 8% opacity → glassSubtle, matching
 * the web's `shimmer-glow` keyframe with `rgba(212, 165, 116, 0.08)` peak tint.
 * 
 * When reduced motion is active, returns a static [SolidColor] with the
 * glassSubtle token color.
 * 
 * Performance: Uses [rememberInfiniteTransition] with shader-based gradient
 * to avoid recomposition on each frame.
 */
@Composable
fun rememberShimmerBrush(): Brush {
    val reducedMotion = rememberCSNexusReducedMotion()
    val glassSubtle = CSNexusDesign.tokens.semantic.glassSubtle

    if (reducedMotion) {
        return SolidColor(glassSubtle)
    }

    val transition = rememberInfiniteTransition(label = "shimmer")
    val offset by transition.animateFloat(
        initialValue = -1f,
        targetValue = 2f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 2000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart,
        ),
        label = "shimmer_offset",
    )

    return Brush.linearGradient(
        colors = listOf(
            glassSubtle,
            Gold.copy(alpha = 0.08f),
            glassSubtle,
        ),
        start = Offset(offset * 1000f, 0f),
        end = Offset((offset + 1f) * 1000f, 0f),
    )
}
