package com.csnexus.app.core.design

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.State
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RadialGradientShader
import androidx.compose.ui.graphics.ShaderBrush
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import kotlin.math.sin

// Blob color palette from CSNexusTheme tokens
private val BlobGold = Color(0xFFC9A84C)
private val BlobMetallic = Color(0xFFE8C96A)
private val BlobInfo = Color(0xFF7EB8C9)
private val BlobSurface = Color(0xFF1C1C1C)
private val BackgroundWarm = Color(0xFF080808)

// Vignette edge color: warm-dark from the web's ambient-depth
private val VignetteEdge = Color(0x801A0F0A) // rgba(26,15,10,0.5)

private const val MobileBreakpointDp = 640

/**
 * Immutable definition of a single animated blob.
 * Positions are expressed as fractions of canvas size (0..1).
 */
private data class BlobSpec(
    val centerXBase: Float,
    val centerYBase: Float,
    val radiusFraction: Float,
    val alpha: Float,
    val color: Color,
    val xAmplitude: Float,
    val yAmplitude: Float,
    val periodMs: Int,
    val phaseOffset: Float,
)

private val BlobSpecs = listOf(
    BlobSpec(
        centerXBase = 0.25f, centerYBase = 0.20f,
        radiusFraction = 0.45f, alpha = 0.35f, color = BlobGold,
        xAmplitude = 0.08f, yAmplitude = 0.06f,
        periodMs = 12000, phaseOffset = 0f,
    ),
    BlobSpec(
        centerXBase = 0.75f, centerYBase = 0.35f,
        radiusFraction = 0.40f, alpha = 0.30f, color = BlobMetallic,
        xAmplitude = 0.07f, yAmplitude = 0.09f,
        periodMs = 14000, phaseOffset = 1.2f,
    ),
    BlobSpec(
        centerXBase = 0.50f, centerYBase = 0.70f,
        radiusFraction = 0.50f, alpha = 0.30f, color = BlobInfo,
        xAmplitude = 0.06f, yAmplitude = 0.07f,
        periodMs = 11000, phaseOffset = 2.5f,
    ),
    BlobSpec(
        centerXBase = 0.15f, centerYBase = 0.80f,
        radiusFraction = 0.35f, alpha = 0.32f, color = BlobSurface,
        xAmplitude = 0.05f, yAmplitude = 0.08f,
        periodMs = 15000, phaseOffset = 3.8f,
    ),
    BlobSpec(
        centerXBase = 0.85f, centerYBase = 0.75f,
        radiusFraction = 0.38f, alpha = 0.33f, color = BlobGold,
        xAmplitude = 0.09f, yAmplitude = 0.05f,
        periodMs = 13000, phaseOffset = 5.0f,
    ),
)

private val MobileBlobSpecs = listOf(
    BlobSpec(
        centerXBase = 0.20f, centerYBase = 0.15f,
        radiusFraction = 0.60f, alpha = 0.42f, color = BlobGold,
        xAmplitude = 0.06f, yAmplitude = 0.05f,
        periodMs = 12000, phaseOffset = 0f,
    ),
    BlobSpec(
        centerXBase = 0.82f, centerYBase = 0.38f,
        radiusFraction = 0.52f, alpha = 0.36f, color = BlobMetallic,
        xAmplitude = 0.05f, yAmplitude = 0.07f,
        periodMs = 14000, phaseOffset = 1.2f,
    ),
    BlobSpec(
        centerXBase = 0.48f, centerYBase = 0.80f,
        radiusFraction = 0.58f, alpha = 0.38f, color = BlobInfo,
        xAmplitude = 0.04f, yAmplitude = 0.05f,
        periodMs = 11000, phaseOffset = 2.5f,
    ),
)

/**
 * Full-screen animated ambient background layer.
 *
 * Renders 5 radial-gradient blobs drifting on sinusoidal paths,
 * a subtle noise texture overlay, and a radial vignette.
 * Designed to sit behind the app's navigation scaffold.
 *
 * Performance: Uses [rememberInfiniteTransition] with raw float offsets
 * and a single [Canvas] draw pass — no recomposition per frame.
 */
@Composable
fun AmbientBackground(modifier: Modifier = Modifier) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val performanceTier = LocalCSNexusPerformanceTier.current
    val screenWidthDp = LocalConfiguration.current.screenWidthDp
    val blobSpecs = remember(screenWidthDp) {
        if (screenWidthDp < MobileBreakpointDp) MobileBlobSpecs else BlobSpecs
    }

    val infiniteTransition = rememberInfiniteTransition(label = "ambient_bg")

    // Animate a normalized progress (0→1) per blob for sinusoidal position calculation.
    // Only create animated values when motion is enabled; static 0f otherwise.
    val animateAmbient = !reducedMotion && performanceTier.animationsEnabled

    val blobProgresses: List<State<Float>> = if (animateAmbient) {
        blobSpecs.map { spec ->
            infiniteTransition.animateFloat(
                initialValue = 0f,
                targetValue = 1f,
                animationSpec = infiniteRepeatable(
                    animation = tween(durationMillis = spec.periodMs, easing = LinearEasing),
                    repeatMode = RepeatMode.Restart,
                ),
                label = "blob_${spec.periodMs}",
            )
        }
    } else {
        // Reduced motion: blobs stay at initial position (progress = 0f)
        remember(blobSpecs) { blobSpecs.map { mutableFloatStateOf(0f) } }
    }

    // Step-animated noise offset: cycles through 10 discrete positions over 8 seconds.
    // Skip animation when reduced motion is active.
    val noiseStep by if (animateAmbient) {
        infiniteTransition.animateFloat(
            initialValue = 0f,
            targetValue = 10f,
            animationSpec = infiniteRepeatable(
                animation = tween(durationMillis = 8000, easing = LinearEasing),
                repeatMode = RepeatMode.Restart,
            ),
            label = "noise_step",
        )
    } else {
        remember { mutableFloatStateOf(0f) }
    }

    // Pre-compute density-related values outside draw scope
    val density = LocalDensity.current
    val noiseSpacingPx = with(density) { 4.dp.toPx() }

    Canvas(
        modifier = modifier
            .fillMaxSize()
            .graphicsLayer { /* Isolate this layer for GPU composition */ },
    ) {
        val w = size.width
        val h = size.height

        // 1. Solid dark background fill
        drawRect(color = BackgroundWarm)

        // 2. Draw blobs. Even the low tier keeps a reduced static composition
        // so mobile screens still match the web's ambient depth.
        blobSpecs.forEachIndexed { index, spec ->
            val progress = blobProgresses[index].value
            val angle = (progress * 2f * Math.PI.toFloat()) + spec.phaseOffset

            val cx = (spec.centerXBase + spec.xAmplitude * sin(angle)) * w
            val cy = (spec.centerYBase + spec.yAmplitude * sin(angle * 0.7f + 1.3f)) * h
            val radius = spec.radiusFraction * minOf(w, h)

            drawBlobCircle(
                center = Offset(cx, cy),
                radius = radius,
                color = spec.color,
                alpha = spec.alpha,
            )
        }

        // 3. Noise overlay (dithered dot pattern at 3% alpha)
        drawNoiseOverlay(
            stepOffset = noiseStep.toInt(),
            spacingPx = noiseSpacingPx,
        )

        // 4. Radial vignette: transparent center → dark edges
        drawVignette()
    }
}

/**
 * Draws a single radial-gradient blob using [RadialGradientShader].
 * The gradient fades from [color] at center to fully transparent at edge.
 */
private fun DrawScope.drawBlobCircle(
    center: Offset,
    radius: Float,
    color: Color,
    alpha: Float,
) {
    val shader = RadialGradientShader(
        center = center,
        radius = radius,
        colors = listOf(
            color.copy(alpha = alpha),
            color.copy(alpha = alpha * 0.5f),
            color.copy(alpha = 0f),
        ),
        colorStops = listOf(0f, 0.5f, 1f),
    )
    val brush = ShaderBrush(shader)
    drawCircle(
        brush = brush,
        radius = radius,
        center = center,
    )
}

/**
 * Draws a simple dithered noise pattern as small dots across the canvas.
 * The [stepOffset] shifts the pattern position to create a grain-shift effect
 * matching the web's step-animated noise overlay.
 */
private fun DrawScope.drawNoiseOverlay(
    stepOffset: Int,
    spacingPx: Float,
) {
    val noiseColor = Color.White.copy(alpha = 0.03f)
    val dotRadius = 0.5f
    val offsetShift = stepOffset * spacingPx * 0.3f

    var x = offsetShift % spacingPx
    while (x < size.width) {
        var y = offsetShift % spacingPx
        while (y < size.height) {
            // Simple pseudo-random skip to create noise-like pattern
            val hash = ((x * 7f + y * 13f + stepOffset * 31f).toInt() and 3)
            if (hash == 0) {
                drawCircle(
                    color = noiseColor,
                    radius = dotRadius,
                    center = Offset(x, y),
                )
            }
            y += spacingPx
        }
        x += spacingPx
    }
}

/**
 * Draws a radial vignette: transparent at center, darkening toward the edges.
 * Matches the web's `.ambient-depth` overlay.
 */
private fun DrawScope.drawVignette() {
    val vignetteBrush = Brush.radialGradient(
        0f to Color.Transparent,
        0.4f to Color.Transparent,
        1f to VignetteEdge,
        center = Offset(size.width * 0.5f, size.height * 0.5f),
        radius = maxOf(size.width, size.height) * 0.7f,
    )
    drawRect(brush = vignetteBrush)
}
