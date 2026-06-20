package com.csnexus.app.core.design

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.snap
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.windowInsetsPadding
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * A single bottom navigation tab item.
 */
data class GlassBottomNavItem(
    val icon: ImageVector,
    val label: String,
    val selected: Boolean,
    val onClick: () -> Unit,
)

// Colors matching the design spec
private val GoldActive = Color(0xFFC9A84C)
private val TextMutedInactive = Color(0xFF666666)
private val GlassBorderLight = Color(0x10FFFFFF)
private val GlassMediumBg = Color(0x10FFFFFF)
private val GlassFallbackBg = Color(0xD9121212)
private val IndicatorColor = Color(0xFFC9A84C)

private val NavBarHeight = 64.dp
private val IndicatorHeight = 3.dp

/**
 * Glass-styled bottom navigation bar matching the web's `.bottom-nav`.
 *
 * - 64.dp height + system navigation bar inset padding
 * - GlassMedium background (6% white + blur on API 31+)
 * - 1px top border at glassBorderLight
 * - Gold active icon/text, muted inactive
 * - 3.dp tall gold indicator bar that slides between tab positions over 150ms
 * - Reduced motion: instant indicator movement
 */
@Composable
fun GlassBottomNav(
    items: List<GlassBottomNavItem>,
    modifier: Modifier = Modifier,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val performanceTier = LocalCSNexusPerformanceTier.current

    val resolvedBackground = if (performanceTier == PerformanceTier.Low) GlassFallbackBg else GlassMediumBg

    // Animate the indicator position as a fraction (0f = first item center, 1f = last)
    val selectedIndex = items.indexOfFirst { it.selected }.coerceAtLeast(0)
    val targetFraction = if (items.size <= 1) 0f else selectedIndex.toFloat() / (items.size - 1).toFloat()

    val animatedFraction by animateFloatAsState(
        targetValue = targetFraction,
        animationSpec = if (reducedMotion) snap() else tween(CSNexusMotion.DurationFast),
        label = "bottomNavIndicator",
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .background(resolvedBackground)
            .drawWithContent {
                // Draw 1px top border at y=0
                drawLine(
                    color = GlassBorderLight,
                    start = Offset(0f, 0f),
                    end = Offset(size.width, 0f),
                    strokeWidth = 1.dp.toPx(),
                )

                drawContent()

                // Draw the sliding indicator bar at the top
                if (items.isNotEmpty()) {
                    val itemWidth = size.width / items.size
                    val indicatorWidth = itemWidth * 0.5f
                    val indicatorHeightPx = IndicatorHeight.toPx()

                    // Center of the selected item
                    val centerX = if (items.size == 1) {
                        size.width / 2f
                    } else {
                        val firstCenter = itemWidth / 2f
                        val lastCenter = size.width - itemWidth / 2f
                        firstCenter + animatedFraction * (lastCenter - firstCenter)
                    }

                    drawRect(
                        color = IndicatorColor,
                        topLeft = Offset(
                            x = centerX - indicatorWidth / 2f,
                            y = 0f,
                        ),
                        size = Size(indicatorWidth, indicatorHeightPx),
                    )
                }
            }
            .windowInsetsPadding(WindowInsets.navigationBars),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(NavBarHeight),
            horizontalArrangement = Arrangement.SpaceAround,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            items.forEach { item ->
                GlassBottomNavTab(
                    item = item,
                    modifier = Modifier.weight(1f),
                )
            }
        }
    }
}

/**
 * Individual tab composable with icon + label.
 */
@Composable
private fun GlassBottomNavTab(
    item: GlassBottomNavItem,
    modifier: Modifier = Modifier,
) {
    val color = if (item.selected) GoldActive else TextMutedInactive
    val interactionSource = remember { MutableInteractionSource() }

    Column(
        modifier = modifier
            .csnexusMinimumTouchTarget()
            .clickable(
                interactionSource = interactionSource,
                indication = null,
                onClick = item.onClick,
            )
            .padding(vertical = 8.dp)
            .semantics {
                role = Role.Tab
                selected = item.selected
                contentDescription = item.label
            },
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(
            imageVector = item.icon,
            contentDescription = null, // described at parent semantics level
            tint = color,
            modifier = Modifier.size(24.dp),
        )
        Text(
            text = item.label,
            color = color,
            fontSize = 11.sp,
            fontWeight = if (item.selected) FontWeight.Medium else FontWeight.Normal,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.padding(top = 2.dp),
        )
    }
}
