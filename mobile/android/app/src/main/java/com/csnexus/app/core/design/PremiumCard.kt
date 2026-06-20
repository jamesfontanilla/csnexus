package com.csnexus.app.core.design

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.onClick
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch

private val GoldBorderPress = Color(0x66D4A574) // gold at ~40% opacity
private val GoldGlowPress = Color(0x14C9A84C)  // gold at 8% opacity
private val BorderResting = Color.Transparent

/**
 * Premium card with press-reactive effects matching the web's `.glass-card-premium`.
 *
 * - On press: translate -2dp, shadow lifts, radial gold glow at press point, gold border.
 * - On release: spring back via [CSNexusMotion.springDefault].
 * - Reduced motion: border-color change only, no translate.
 */
@Composable
fun PremiumCard(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    content: @Composable BoxScope.() -> Unit,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val performanceTier = LocalCSNexusPerformanceTier.current
    val scope = rememberCoroutineScope()
    val density = LocalDensity.current

    // Press state
    var pressed by remember { mutableStateOf(false) }
    var pressOffset by remember { mutableStateOf(Offset.Zero) }

    // TranslationY animation (in px)
    val liftPx = with(density) { 2.dp.toPx() }
    val translationY = remember { Animatable(0f) }

    // Animated border color: transparent at rest → gold@40% on press
    val borderColor by animateColorAsState(
        targetValue = if (pressed) GoldBorderPress else BorderResting,
        animationSpec = tween(CSNexusMotion.DurationFast),
        label = "premium_border",
    )

    val inputModifier = Modifier.pointerInput(onClick) {
        detectTapGestures(
            onPress = { offset ->
                pressed = true
                pressOffset = offset
                if (!reducedMotion) {
                    scope.launch {
                        translationY.animateTo(
                            targetValue = -liftPx,
                            animationSpec = tween(CSNexusMotion.DurationFast),
                        )
                    }
                }
                val released = tryAwaitRelease()
                pressed = false
                if (!reducedMotion) {
                    scope.launch {
                        translationY.animateTo(
                            targetValue = 0f,
                            animationSpec = CSNexusMotion.springDefault(),
                        )
                    }
                }
                if (released) {
                    onClick?.invoke()
                }
            },
        )
    }
    val accessibilityModifier = if (onClick != null) {
        Modifier.semantics {
            role = Role.Button
            onClick {
                onClick.invoke()
                true
            }
        }
    } else {
        Modifier
    }

    // Choose shadow modifier based on press state
    val shadowModifier = when {
        performanceTier == PerformanceTier.Low -> Modifier
        pressed -> Modifier.shadowLifted()
        else -> Modifier.shadowSubtle()
    }

    val shape = RoundedCornerShape(CSNexusDesign.tokens.radius.lg)

    GlassMedium(
        modifier = modifier
            .then(shadowModifier)
            .then(inputModifier)
            .then(accessibilityModifier)
            .graphicsLayer {
                this.translationY = translationY.value
            }
            .border(1.dp, borderColor, shape)
            .drawWithContent {
                drawContent()
                // Radial gold glow at press coordinates
                if (pressed) {
                    drawCircle(
                        color = GoldGlowPress,
                        radius = size.maxDimension * 0.6f,
                        center = pressOffset,
                    )
                }
            },
        content = content,
    )
}
