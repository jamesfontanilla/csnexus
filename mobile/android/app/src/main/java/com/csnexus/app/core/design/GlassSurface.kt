package com.csnexus.app.core.design

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

// Glass tier background colors (semi-transparent white on dark)
private val GlassSubtleBg = Color(0x08FFFFFF)   // 3% white
private val GlassMediumBg = Color(0x10FFFFFF)    // 6% white
private val GlassStrongBg = Color(0x1AFFFFFF)    // 10% white

// Glass border colors
private val GlassBorderLight = Color(0x10FFFFFF)  // 6% white
private val GlassBorderMedium = Color(0x1AFFFFFF) // 10% white
private val GlassBorderStrong = Color(0x2EFFFFFF) // ~18% white

// Opaque native fallback. Compose RenderEffect blurs the element itself, not
// the backdrop like CSS backdrop-filter, so glass surfaces use sharp overlays.
private val GlassFallbackBg = Color(0xD9121212)

// Diagonal gradient border overlay colors (135deg: white@12% → transparent → white@6%)
private val GradientOverlayStart = Color(0x1FFFFFFF)  // ~12% white
private val GradientOverlayEnd = Color(0x0FFFFFFF)    // ~6% white

/**
 * Small glass surface tier.
 * - Background: 3% white (glassSubtle)
 * - Border: 6% white (glassBorderLight)
 * - Native fallback keeps child content sharp; no self-blur is applied.
 *
 * Matches web `.glass-sm`.
 */
@Composable
fun GlassSmall(
    modifier: Modifier = Modifier,
    borderRadius: Dp = CSNexusDesign.tokens.radius.lg,
    content: @Composable BoxScope.() -> Unit,
) {
    GlassSurfaceInternal(
        modifier = modifier,
        borderRadius = borderRadius,
        background = GlassSubtleBg,
        borderColor = GlassBorderLight,
        content = content,
    )
}

/**
 * Medium glass surface tier.
 * - Background: 6% white (glassMedium)
 * - Border: 10% white (glassBorderMedium)
 * - Native fallback keeps child content sharp; no self-blur is applied.
 *
 * Matches web `.glass-md`.
 */
@Composable
fun GlassMedium(
    modifier: Modifier = Modifier,
    borderRadius: Dp = CSNexusDesign.tokens.radius.lg,
    content: @Composable BoxScope.() -> Unit,
) {
    GlassSurfaceInternal(
        modifier = modifier,
        borderRadius = borderRadius,
        background = GlassMediumBg,
        borderColor = GlassBorderMedium,
        content = content,
    )
}

/**
 * Large glass surface tier.
 * - Background: 10% white (glassStrong)
 * - Border: 18% white (glassBorderStrong)
 * - Native fallback keeps child content sharp; no self-blur is applied.
 *
 * Matches web `.glass-lg`.
 */
@Composable
fun GlassLarge(
    modifier: Modifier = Modifier,
    borderRadius: Dp = CSNexusDesign.tokens.radius.lg,
    content: @Composable BoxScope.() -> Unit,
) {
    GlassSurfaceInternal(
        modifier = modifier,
        borderRadius = borderRadius,
        background = GlassStrongBg,
        borderColor = GlassBorderStrong,
        content = content,
    )
}

/**
 * Internal shared implementation for all glass tiers.
 *
 * Applies:
 * 1. Clipped rounded shape
 * 2. Semi-transparent background (or solid dark fallback when blur unavailable)
 * 3. 1px border at the tier's border color
 * 4. Diagonal gradient border overlay (135deg white@12% → transparent → white@6%)
 * 5. Native fallback keeps child content sharp; no self-blur is applied.
 */
@Composable
private fun GlassSurfaceInternal(
    modifier: Modifier,
    borderRadius: Dp,
    background: Color,
    borderColor: Color,
    content: @Composable BoxScope.() -> Unit,
) {
    val shape = RoundedCornerShape(borderRadius)
    val performanceTier = LocalCSNexusPerformanceTier.current

    val resolvedBackground = if (performanceTier == PerformanceTier.Low) {
        GlassFallbackBg
    } else {
        background
    }

    Box(
        modifier = modifier
            .clip(shape)
            .background(resolvedBackground, shape)
            .border(1.dp, borderColor, shape)
            .then(
                if (performanceTier == PerformanceTier.Low) {
                    Modifier
                } else {
                    Modifier.diagonalGradientOverlay()
                },
            ),
        content = content,
    )
}

/**
 * Draws a diagonal (135-degree) gradient border overlay on top of content,
 * matching the web's `::before` pseudo-element:
 * linear-gradient(135deg, white@12% → transparent → white@6%).
 *
 * Because the parent Box is already clipped to the rounded shape,
 * this drawRect respects the clip automatically.
 */
private fun Modifier.diagonalGradientOverlay(): Modifier = drawWithContent {
    drawContent()
    val brush = Brush.linearGradient(
        colorStops = arrayOf(
            0.0f to GradientOverlayStart,
            0.5f to Color.Transparent,
            1.0f to GradientOverlayEnd,
        ),
        start = Offset(0f, 0f),
        end = Offset(size.width, size.height),
    )
    drawRect(brush = brush)
}
