package com.csnexus.app.core.design

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.RoundedCornerShape

private val Obsidian = Color(0xFF080808)
private val ObsidianWarm = Color(0xFF050505)
private val Surface = Color(0xFF1C1C1C)
private val SurfaceRaised = Color(0xFF242424)
private val Gold = Color(0xFFC9A84C)
private val MetallicGold = Color(0xFFE8C96A)
private val WarmWhite = Color(0xFFF0EBE0)
private val TextSecondary = Color(0xFF9A9A9A)
private val TextMuted = Color(0xFF666666)
private val Success = Color(0xFF8FBC8F)
private val Warning = Color(0xFFE8A838)
private val Danger = Color(0xFFD4645C)
private val Info = Color(0xFF7EB8C9)

private val DarkColors: ColorScheme = darkColorScheme(
    primary = Gold,
    onPrimary = ObsidianWarm,
    secondary = MetallicGold,
    onSecondary = ObsidianWarm,
    tertiary = Info,
    onTertiary = ObsidianWarm,
    background = Obsidian,
    onBackground = WarmWhite,
    surface = Surface,
    onSurface = WarmWhite,
    surfaceVariant = SurfaceRaised,
    onSurfaceVariant = TextSecondary,
    outline = Color(0x33FFFFFF),
    outlineVariant = Color(0x1AFFFFFF),
    error = Danger,
    onError = Color.White,
)

@Immutable
data class CSNexusSemanticColors(
    val success: Color,
    val warning: Color,
    val danger: Color,
    val info: Color,
    val textMuted: Color,
    val glassSubtle: Color,
    val glassMedium: Color,
    val glassStrong: Color,
    val glassBorderLight: Color,
    val glassBorderMedium: Color,
    val stateHover: Color,
    val stateActive: Color,
)

@Immutable
data class CSNexusSpacing(
    val none: Dp = 0.dp,
    val xs: Dp = 4.dp,
    val sm: Dp = 8.dp,
    val md: Dp = 12.dp,
    val lg: Dp = 16.dp,
    val xl: Dp = 24.dp,
    val xxl: Dp = 32.dp,
    val section: Dp = 48.dp,
    val page: Dp = 64.dp,
)

@Immutable
data class CSNexusRadius(
    val sm: Dp = 8.dp,
    val md: Dp = 12.dp,
    val lg: Dp = 20.dp,
    val xl: Dp = 28.dp,
)

@Immutable
data class CSNexusElevation(
    val flat: Dp = 0.dp,
    val raised: Dp = 2.dp,
    val floating: Dp = 8.dp,
)

@Immutable
data class CSNexusShadows(
    val subtle: List<Shadow>,
    val diffused: List<Shadow>,
    val depth: List<Shadow>,
    val lifted: List<Shadow>,
    val glow: List<Shadow>,
)

private val DefaultShadows = CSNexusShadows(
    subtle = listOf(
        Shadow(color = Color(0x4D000000), offset = Offset(0f, 2f), blurRadius = 8f),
        Shadow(color = Color(0x33000000), offset = Offset(0f, 1f), blurRadius = 3f),
    ),
    diffused = listOf(
        Shadow(color = Color(0x66000000), offset = Offset(0f, 4f), blurRadius = 16f),
        Shadow(color = Color(0x33000000), offset = Offset(0f, 1f), blurRadius = 4f),
    ),
    depth = listOf(
        Shadow(color = Color(0xB3000000), offset = Offset(0f, 8f), blurRadius = 32f),
        Shadow(color = Color(0x66000000), offset = Offset(0f, 2f), blurRadius = 8f),
    ),
    lifted = listOf(
        Shadow(color = Color(0xCC000000), offset = Offset(0f, 12f), blurRadius = 40f),
        Shadow(color = Color(0x80000000), offset = Offset(0f, 4f), blurRadius = 16f),
    ),
    glow = listOf(
        Shadow(color = Color(0x33C9A84C), offset = Offset(0f, 0f), blurRadius = 20f),
    ),
)

@Immutable
data class CSNexusDesignTokens(
    val semantic: CSNexusSemanticColors,
    val spacing: CSNexusSpacing,
    val radius: CSNexusRadius,
    val elevation: CSNexusElevation,
    val shadows: CSNexusShadows,
)

private val DarkTokens = CSNexusDesignTokens(
    semantic = CSNexusSemanticColors(
        success = Success,
        warning = Warning,
        danger = Danger,
        info = Info,
        textMuted = TextMuted,
        glassSubtle = Color(0x08FFFFFF),
        glassMedium = Color(0x10FFFFFF),
        glassStrong = Color(0x1AFFFFFF),
        glassBorderLight = Color(0x10FFFFFF),
        glassBorderMedium = Color(0x1AFFFFFF),
        stateHover = Color(0x14D4A574),
        stateActive = Color(0x26D4A574),
    ),
    spacing = CSNexusSpacing(),
    radius = CSNexusRadius(),
    elevation = CSNexusElevation(),
    shadows = DefaultShadows,
)

val LocalCSNexusDesignTokens = staticCompositionLocalOf { DarkTokens }

@Immutable
data class CSNexusUiPreferences(
    val themePreference: String = "system",
    val fontSizePreference: String = "default",
    val reducedMotionPreference: String = "system",
)

val LocalCSNexusUiPreferences = staticCompositionLocalOf { CSNexusUiPreferences() }

object CSNexusDesign {
    val tokens: CSNexusDesignTokens
        @Composable get() = LocalCSNexusDesignTokens.current
}

private val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = CSNexusDisplayFont,
        fontWeight = FontWeight.ExtraBold,
        fontSize = 56.sp,
        lineHeight = 58.sp,
        letterSpacing = (-0.04).em,
    ),
    headlineLarge = TextStyle(
        fontFamily = CSNexusDisplayFont,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 36.sp,
        letterSpacing = (-0.03).em,
    ),
    titleLarge = TextStyle(
        fontFamily = CSNexusDisplayFont,
        fontWeight = FontWeight.SemiBold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = (-0.02).em,
    ),
    titleMedium = TextStyle(
        fontFamily = CSNexusDisplayFont,
        fontWeight = FontWeight.SemiBold,
        fontSize = 16.sp,
        lineHeight = 22.sp,
        letterSpacing = (-0.01).em,
    ),
    bodyLarge = TextStyle(
        fontFamily = CSNexusBodyFont,
        fontWeight = FontWeight.Normal,
        fontSize = 15.sp,
        lineHeight = 24.sp,
    ),
    bodyMedium = TextStyle(
        fontFamily = CSNexusBodyFont,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 22.sp,
    ),
    labelLarge = TextStyle(
        fontFamily = CSNexusDisplayFont,
        fontWeight = FontWeight.SemiBold,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.01.em,
    ),
)

private val AppShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(20.dp),
    extraLarge = RoundedCornerShape(28.dp),
)

@Composable
fun CSNexusTheme(
    darkTheme: Boolean? = null,
    themePreference: String = "system",
    fontSizePreference: String = "default",
    reducedMotionPreference: String = "system",
    content: @Composable () -> Unit,
) {
    // Always dark — matches web's dark-only design.
    val colorScheme = DarkColors
    val tokens = DarkTokens
    val typography = remember(fontSizePreference) {
        AppTypography.scaled(fontScaleMultiplier(fontSizePreference))
    }
    val uiPreferences = remember(themePreference, fontSizePreference, reducedMotionPreference) {
        CSNexusUiPreferences(
            themePreference = themePreference,
            fontSizePreference = fontSizePreference,
            reducedMotionPreference = reducedMotionPreference,
        )
    }

    CompositionLocalProvider(
        LocalCSNexusDesignTokens provides tokens,
        LocalCSNexusUiPreferences provides uiPreferences,
    ) {
        MaterialTheme(
            colorScheme = colorScheme,
            typography = typography,
            shapes = AppShapes,
            content = content,
        )
    }
}

internal fun resolveDarkTheme(themePreference: String, systemIsDark: Boolean): Boolean {
    // Dark mode only — the app always renders dark regardless of system setting.
    // "light" and "system" both resolve to dark to match the web's dark-only design.
    return true
}

internal fun fontScaleMultiplier(fontSizePreference: String): Float {
    return when (fontSizePreference.lowercase()) {
        "compact" -> 0.875f
        "large" -> 1.15f
        else -> 1f
    }
}

private fun Typography.scaled(multiplier: Float): Typography = copy(
    displayLarge = displayLarge.scaleBy(multiplier),
    headlineLarge = headlineLarge.scaleBy(multiplier),
    titleLarge = titleLarge.scaleBy(multiplier),
    titleMedium = titleMedium.scaleBy(multiplier),
    bodyLarge = bodyLarge.scaleBy(multiplier),
    bodyMedium = bodyMedium.scaleBy(multiplier),
    labelLarge = labelLarge.scaleBy(multiplier),
)

private fun TextStyle.scaleBy(multiplier: Float): TextStyle = copy(
    fontSize = fontSize * multiplier,
    lineHeight = lineHeight * multiplier,
)
