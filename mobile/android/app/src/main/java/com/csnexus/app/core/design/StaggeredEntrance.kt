package com.csnexus.app.core.design

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay

private const val STAGGER_DELAY_MS = 50L
private const val ENTRANCE_DURATION_MS = 300

/**
 * Wraps [content] in a staggered entrance animation.
 *
 * Each item fades in + translates 8.dp upward, delayed by [index] * 50ms.
 * Under reduced motion, items appear instantly with no animation.
 *
 * Usage in a LazyColumn:
 * ```
 * items(list.size) { index ->
 *     StaggeredItem(index = index) {
 *         PremiumCard { ... }
 *     }
 * }
 * ```
 */
@Composable
fun StaggeredItem(
    index: Int,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val density = LocalDensity.current

    if (reducedMotion) {
        content()
        return
    }

    var visible by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        delay(index * STAGGER_DELAY_MS)
        visible = true
    }

    AnimatedVisibility(
        visible = visible,
        modifier = modifier,
        enter = fadeIn(
            animationSpec = tween(ENTRANCE_DURATION_MS, easing = FastOutSlowInEasing),
        ) + slideInVertically(
            animationSpec = tween(ENTRANCE_DURATION_MS, easing = FastOutSlowInEasing),
            initialOffsetY = { with(density) { 8.dp.roundToPx() } },
        ),
    ) {
        content()
    }
}
