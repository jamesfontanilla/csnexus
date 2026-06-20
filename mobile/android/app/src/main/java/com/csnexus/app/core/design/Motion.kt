package com.csnexus.app.core.design

import android.provider.Settings
import androidx.compose.animation.core.AnimationSpec
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.TweenSpec
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.IntOffset

object CSNexusMotion {
    const val DurationInstant = 80
    const val DurationFast = 150
    const val DurationNormal = 250
    const val DurationSlow = 400
    const val DurationPage = 500

    fun <T> instant(): AnimationSpec<T> = tween(DurationInstant)
    fun <T> fast(): AnimationSpec<T> = tween(DurationFast)
    fun <T> normal(): AnimationSpec<T> = tween(DurationNormal)
    fun <T> slow(): AnimationSpec<T> = tween(DurationSlow)
    fun <T> page(): AnimationSpec<T> = tween(DurationPage)

    fun <T> springDefault(): AnimationSpec<T> = spring(
        dampingRatio = Spring.DampingRatioMediumBouncy,
        stiffness = Spring.StiffnessMedium,
    )

    fun <T> springGentle(): AnimationSpec<T> = spring(
        dampingRatio = Spring.DampingRatioNoBouncy,
        stiffness = Spring.StiffnessLow,
    )

    fun reducedTween(): TweenSpec<Float> = tween(DurationInstant)

    val ForwardOffset = IntOffset(24, 0)
    val BackOffset = IntOffset(-24, 0)
    val VerticalOffset = IntOffset(0, 12)
}

@Composable
fun rememberCSNexusReducedMotion(): Boolean {
    val context = LocalContext.current
    val preference = LocalCSNexusUiPreferences.current.reducedMotionPreference
    val performanceTier = LocalCSNexusPerformanceTier.current
    return remember(context, preference, performanceTier) {
        !performanceTier.animationsEnabled || resolveReducedMotionPreference(
            reducedMotionPreference = preference,
            systemReducedMotion = Settings.Global.getFloat(
                context.contentResolver,
                Settings.Global.ANIMATOR_DURATION_SCALE,
                1f,
            ) == 0f,
        )
    }
}

internal fun resolveReducedMotionPreference(
    reducedMotionPreference: String,
    systemReducedMotion: Boolean,
): Boolean {
    return when (reducedMotionPreference.lowercase()) {
        "on" -> true
        "off" -> false
        else -> systemReducedMotion
    }
}
