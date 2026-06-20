package com.csnexus.app.core.design

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

private val ThumbColorIdle = Color(0x40C9A84C)     // gold at 25% alpha
private val ThumbColorActive = Color(0x73C9A84C)   // gold at 45% alpha
private val ThumbWidth = 6.dp
private val ThumbCornerRadius = 3.dp

/**
 * Custom scrollbar modifier for [ScrollState].
 * Draws a gold-tinted scrollbar thumb with 6.dp width and 3.dp border-radius.
 * Thumb alpha increases from 25% to 45% during active scrolling.
 * Track is transparent.
 */
@Composable
fun Modifier.goldScrollbar(scrollState: ScrollState): Modifier {
    val isScrolling = scrollState.isScrollInProgress
    val reducedMotion = rememberCSNexusReducedMotion()

    val thumbAlpha by animateFloatAsState(
        targetValue = if (isScrolling) 0.45f else 0.25f,
        animationSpec = if (reducedMotion) CSNexusMotion.instant() else tween(150),
        label = "scrollbarAlpha",
    )

    val thumbColor = Color(0xFFC9A84C).copy(alpha = thumbAlpha)

    return this.drawWithContent {
        drawContent()

        val maxScroll = scrollState.maxValue.toFloat()
        if (maxScroll <= 0f) return@drawWithContent

        val viewportHeight = size.height
        val contentHeight = viewportHeight + maxScroll
        val thumbHeight = (viewportHeight / contentHeight * viewportHeight).coerceAtLeast(24.dp.toPx())
        val scrollFraction = scrollState.value / maxScroll
        val thumbOffset = scrollFraction * (viewportHeight - thumbHeight)

        drawRoundRect(
            color = thumbColor,
            topLeft = Offset(size.width - ThumbWidth.toPx(), thumbOffset),
            size = Size(ThumbWidth.toPx(), thumbHeight),
            cornerRadius = CornerRadius(ThumbCornerRadius.toPx(), ThumbCornerRadius.toPx()),
        )
    }
}

/**
 * Custom scrollbar modifier for [LazyListState].
 * Same styling as the ScrollState version, for use with LazyColumn/LazyRow.
 */
@Composable
fun Modifier.goldScrollbar(listState: LazyListState): Modifier {
    val isScrolling = listState.isScrollInProgress
    val reducedMotion = rememberCSNexusReducedMotion()

    val thumbAlpha by animateFloatAsState(
        targetValue = if (isScrolling) 0.45f else 0.25f,
        animationSpec = if (reducedMotion) CSNexusMotion.instant() else tween(150),
        label = "lazyScrollbarAlpha",
    )

    val thumbColor = Color(0xFFC9A84C).copy(alpha = thumbAlpha)

    // Approximate scroll position from visible items
    val totalItems by remember { derivedStateOf { listState.layoutInfo.totalItemsCount } }

    return this.drawWithContent {
        drawContent()

        if (totalItems <= 0) return@drawWithContent

        val firstVisible = listState.firstVisibleItemIndex
        val visibleCount = listState.layoutInfo.visibleItemsInfo.size
        if (visibleCount >= totalItems) return@drawWithContent // all visible, no scrollbar

        val viewportHeight = size.height
        val thumbHeight = (visibleCount.toFloat() / totalItems * viewportHeight).coerceAtLeast(24.dp.toPx())
        val scrollFraction = firstVisible.toFloat() / (totalItems - visibleCount).coerceAtLeast(1)
        val thumbOffset = scrollFraction * (viewportHeight - thumbHeight)

        drawRoundRect(
            color = thumbColor,
            topLeft = Offset(size.width - ThumbWidth.toPx(), thumbOffset),
            size = Size(ThumbWidth.toPx(), thumbHeight),
            cornerRadius = CornerRadius(ThumbCornerRadius.toPx(), ThumbCornerRadius.toPx()),
        )
    }
}
