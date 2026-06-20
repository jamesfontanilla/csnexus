package com.csnexus.app.core.design

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.LinearGradientShader
import androidx.compose.ui.graphics.ShaderBrush
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.em

private val MetallicGold = Color(0xFFE8C96A)
private val AccentGold = Color(0xFFC9A84C)

@Composable
fun MetallicText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = MaterialTheme.typography.headlineLarge,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val performanceTier = LocalCSNexusPerformanceTier.current

    if (performanceTier == PerformanceTier.Low) {
        Text(
            text = text,
            modifier = modifier.semantics {
                contentDescription = text
            },
            color = MetallicGold,
            style = style.copy(
                fontWeight = FontWeight.SemiBold,
                letterSpacing = 0.02.em,
            ),
        )
        return
    }

    val offset = if (!reducedMotion) {
        val transition = rememberInfiniteTransition(label = "metallic_text")
        val animated by transition.animateFloat(
            initialValue = 0f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(3000, easing = LinearEasing),
                repeatMode = RepeatMode.Restart,
            ),
            label = "metallic_offset",
        )
        animated
    } else {
        0f
    }

    val brush = ShaderBrush(
        LinearGradientShader(
            from = Offset(offset * 1000f, 0f),
            to = Offset(offset * 1000f + 2000f, 0f),
            colors = listOf(
                MetallicGold,
                AccentGold,
                MetallicGold,
                AccentGold,
                MetallicGold,
            ),
            colorStops = listOf(0f, 0.25f, 0.5f, 0.75f, 1f),
        ),
    )

    Text(
        text = text,
        modifier = modifier.semantics {
            contentDescription = text
        },
        style = style.copy(
            brush = brush,
            fontWeight = FontWeight.SemiBold,
            letterSpacing = 0.02.em,
        ),
    )
}
