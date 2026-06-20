package com.csnexus.app.core.design

import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Paint
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

private val Gold = Color(0xFFC9A84C)

/**
 * Draws a gold radial glow behind the content.
 * Matches the web's gold glow effect applied to buttons, progress bars, and inputs.
 */
fun Modifier.goldGlow(
    radius: Dp = 20.dp,
    alpha: Float = 0.20f,
): Modifier = drawBehind {
    drawCircle(
        color = Gold.copy(alpha = alpha),
        radius = radius.toPx(),
        center = Offset(size.width / 2f, size.height / 2f),
    )
}

/**
 * Subtle shadow: 0 2px 8px rgba(0,0,0,0.3), 0 1px 3px rgba(0,0,0,0.2)
 */
fun Modifier.shadowSubtle(): Modifier = drawBehind {
    drawIntoCanvas { canvas ->
        val paint = Paint().asFrameworkPaint().apply {
            color = Color.Transparent.toArgb()
            setShadowLayer(8.dp.toPx(), 0f, 2.dp.toPx(), Color(0x4D000000).toArgb())
        }
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
        paint.setShadowLayer(3.dp.toPx(), 0f, 1.dp.toPx(), Color(0x33000000).toArgb())
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
    }
}

/**
 * Diffused shadow: 0 4px 16px rgba(0,0,0,0.4), 0 1px 4px rgba(0,0,0,0.2)
 */
fun Modifier.shadowDiffused(): Modifier = drawBehind {
    drawIntoCanvas { canvas ->
        val paint = Paint().asFrameworkPaint().apply {
            color = Color.Transparent.toArgb()
            setShadowLayer(16.dp.toPx(), 0f, 4.dp.toPx(), Color(0x66000000).toArgb())
        }
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
        paint.setShadowLayer(4.dp.toPx(), 0f, 1.dp.toPx(), Color(0x33000000).toArgb())
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
    }
}

/**
 * Deep shadow: 0 8px 32px rgba(0,0,0,0.7), 0 2px 8px rgba(0,0,0,0.4)
 */
fun Modifier.shadowDepth(): Modifier = drawBehind {
    drawIntoCanvas { canvas ->
        val paint = Paint().asFrameworkPaint().apply {
            color = Color.Transparent.toArgb()
            setShadowLayer(32.dp.toPx(), 0f, 8.dp.toPx(), Color(0xB3000000).toArgb())
        }
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
        paint.setShadowLayer(8.dp.toPx(), 0f, 2.dp.toPx(), Color(0x66000000).toArgb())
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
    }
}

/**
 * Lifted shadow: 0 12px 40px rgba(0,0,0,0.8), 0 4px 16px rgba(0,0,0,0.5)
 */
fun Modifier.shadowLifted(): Modifier = drawBehind {
    drawIntoCanvas { canvas ->
        val paint = Paint().asFrameworkPaint().apply {
            color = Color.Transparent.toArgb()
            setShadowLayer(40.dp.toPx(), 0f, 12.dp.toPx(), Color(0xCC000000).toArgb())
        }
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
        paint.setShadowLayer(16.dp.toPx(), 0f, 4.dp.toPx(), Color(0x80000000).toArgb())
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
    }
}

/**
 * Gold outer glow shadow: 0 0 20px rgba(201,168,76,0.20)
 * Matches web's `--shadow-glow` token.
 */
fun Modifier.shadowGlow(): Modifier = drawBehind {
    drawIntoCanvas { canvas ->
        val paint = Paint().asFrameworkPaint().apply {
            color = Color.Transparent.toArgb()
            setShadowLayer(20.dp.toPx(), 0f, 0f, Color(0x33C9A84C).toArgb())
        }
        canvas.nativeCanvas.drawRect(0f, 0f, size.width, size.height, paint)
    }
}
