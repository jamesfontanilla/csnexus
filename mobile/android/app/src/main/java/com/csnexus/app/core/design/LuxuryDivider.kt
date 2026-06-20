package com.csnexus.app.core.design

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

private val Gold = Color(0xFFC9A84C)
private val GlassBorderMedium = Color(0x1AFFFFFF)
private val GoldGlow = Color(0x33C9A84C) // 20% alpha gold

/**
 * A luxury divider matching the web's `.divider-luxury`:
 * A horizontal gradient line (transparent → border → gold → border → transparent)
 * with a centered 8.dp gold dot + glow effect.
 */
@Composable
fun LuxuryDivider(modifier: Modifier = Modifier) {
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(16.dp), // enough space for the dot + glow
    ) {
        val centerY = size.height / 2f
        val centerX = size.width / 2f

        // Gradient line
        drawLine(
            brush = Brush.horizontalGradient(
                colorStops = arrayOf(
                    0.0f to Color.Transparent,
                    0.2f to GlassBorderMedium,
                    0.5f to Gold,
                    0.8f to GlassBorderMedium,
                    1.0f to Color.Transparent,
                ),
            ),
            start = Offset(0f, centerY),
            end = Offset(size.width, centerY),
            strokeWidth = 1.dp.toPx(),
        )

        // Gold glow behind the dot
        drawCircle(
            color = GoldGlow,
            radius = 12.dp.toPx(),
            center = Offset(centerX, centerY),
        )

        // Centered gold dot (8.dp diameter = 4.dp radius)
        drawCircle(
            color = Gold,
            radius = 4.dp.toPx(),
            center = Offset(centerX, centerY),
        )
    }
}
