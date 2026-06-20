package com.csnexus.app.core.design

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import kotlin.math.roundToInt

/**
 * Animated count-up number that transitions from 0 to [target] over [durationMs].
 *
 * Uses decelerate easing (FastOutSlowIn) for a natural "revealing" feel.
 * When reduced motion is active, shows the final value immediately.
 *
 * @param target The final integer value to count up to.
 * @param durationMs Animation duration in milliseconds (default 1000ms).
 * @param style Text style for rendering.
 * @param prefix Optional prefix string (e.g., "$", "+").
 * @param suffix Optional suffix string (e.g., "%", "XP").
 */
@Composable
fun AnimatedNumber(
    target: Int,
    modifier: Modifier = Modifier,
    durationMs: Int = 1000,
    style: TextStyle = MaterialTheme.typography.headlineLarge,
    prefix: String = "",
    suffix: String = "",
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val animatable = remember { Animatable(0f) }
    val finalText = "$prefix$target$suffix"

    LaunchedEffect(target) {
        if (reducedMotion) {
            animatable.snapTo(target.toFloat())
        } else {
            animatable.snapTo(0f)
            animatable.animateTo(
                targetValue = target.toFloat(),
                animationSpec = tween(
                    durationMillis = durationMs,
                    easing = FastOutSlowInEasing,
                ),
            )
        }
    }

    Text(
        text = "$prefix${animatable.value.roundToInt()}$suffix",
        modifier = modifier.semantics {
            contentDescription = finalText
        },
        style = style,
    )
}
