package com.csnexus.app.core.design

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.keyframes
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.AssistChip
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch

enum class CSNexusButtonVariant { Primary, Secondary, Ghost, Danger }

@Composable
fun CSNexusButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    variant: CSNexusButtonVariant = CSNexusButtonVariant.Primary,
    enabled: Boolean = true,
    loading: Boolean = false,
    leadingIcon: (@Composable () -> Unit)? = null,
) {
    val disabled = !enabled || loading
    val indicatorColor = when (variant) {
        CSNexusButtonVariant.Primary -> MaterialTheme.colorScheme.onPrimary
        CSNexusButtonVariant.Danger -> Color.White
        else -> MaterialTheme.colorScheme.onSurface
    }
    val content: @Composable () -> Unit = {
        if (loading) {
            CircularProgressIndicator(
                modifier = Modifier.size(18.dp),
                strokeWidth = 2.dp,
                color = indicatorColor,
            )
        } else {
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                if (leadingIcon != null) leadingIcon()
                Text(text)
            }
        }
    }

    when (variant) {
        CSNexusButtonVariant.Primary -> {
            val reducedMotion = rememberCSNexusReducedMotion()
            val performanceTier = LocalCSNexusPerformanceTier.current
            val scope = rememberCoroutineScope()
            val density = LocalDensity.current
            val shape = RoundedCornerShape(CSNexusDesign.tokens.radius.md)

            // Gold gradient (135deg: accent → metallic)
            val goldGradient = Brush.linearGradient(
                colors = listOf(Color(0xFFC9A84C), Color(0xFFE8C96A)),
                start = Offset(0f, Float.POSITIVE_INFINITY),
                end = Offset(Float.POSITIVE_INFINITY, 0f),
            )
            val goldBorderColor = Color(0x4DC9A84C) // gold 30% alpha
            val textColor = Color(0xFF050505) // ObsidianWarm

            // Press state
            var pressed by remember { mutableStateOf(false) }
            val liftPx = with(density) { 2.dp.toPx() }
            val translationY = remember { Animatable(0f) }

            val shimmerOffset = if (!reducedMotion && pressed) {
                val shimmerTransition = rememberInfiniteTransition(label = "btn_shimmer")
                val shimmerAnimatedOffset by shimmerTransition.animateFloat(
                    initialValue = -1f,
                    targetValue = 2f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(durationMillis = 600, easing = LinearEasing),
                        repeatMode = RepeatMode.Restart,
                    ),
                    label = "btn_shimmer_offset",
                )
                shimmerAnimatedOffset
            } else {
                null
            }

            val inputModifier = if (!disabled) {
                Modifier.pointerInput(onClick) {
                    detectTapGestures(
                        onPress = {
                            pressed = true
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
                            if (released) onClick()
                        },
                    )
                }
            } else {
                Modifier
            }

            // Shadow: resting = gold shadow, pressed = increased glow
            val shadowModifier = if (performanceTier == PerformanceTier.Low) {
                Modifier
            } else {
                if (pressed) {
                    Modifier.drawWithContent {
                        // Increased glow: 0 0 24px rgba(212,165,116,0.3) + 0 4px 16px rgba(212,165,116,0.2)
                        drawCircle(
                            color = Color(0x4DD4A574),
                            radius = 24.dp.toPx(),
                            center = Offset(size.width / 2f, size.height / 2f),
                        )
                        drawContent()
                    }
                } else {
                    Modifier.drawWithContent {
                        // Resting: 0 2px 8px rgba(212,165,116,0.15)
                        drawCircle(
                            color = Color(0x26D4A574),
                            radius = 12.dp.toPx(),
                            center = Offset(size.width / 2f, size.height + 2.dp.toPx()),
                        )
                        drawContent()
                    }
                }
            }

            Box(
                modifier = modifier
                    .csnexusMinimumTouchTarget()
                    .then(shadowModifier)
                    .then(inputModifier)
                    .graphicsLayer {
                        this.translationY = translationY.value
                        if (disabled) alpha = 0.5f
                    }
                    .background(goldGradient, shape)
                    .border(1.dp, goldBorderColor, shape)
                    .semantics { role = Role.Button }
                    .drawWithContent {
                        drawContent()
                        // Shimmer sweep highlight on press
                        if (shimmerOffset != null) {
                            val sweepBrush = Brush.linearGradient(
                                colors = listOf(
                                    Color.Transparent,
                                    Color.White.copy(alpha = 0.25f),
                                    Color.Transparent,
                                ),
                                start = Offset(shimmerOffset * size.width, 0f),
                                end = Offset((shimmerOffset + 0.5f) * size.width, 0f),
                            )
                            drawRect(sweepBrush)
                        }
                    }
                    .padding(horizontal = 20.dp, vertical = 12.dp),
                contentAlignment = Alignment.Center,
            ) {
                if (loading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = textColor,
                    )
                } else {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (leadingIcon != null) leadingIcon()
                        Text(text, color = textColor)
                    }
                }
            }
        }
        CSNexusButtonVariant.Secondary -> {
            val shape = RoundedCornerShape(CSNexusDesign.tokens.radius.md)
            val warmWhite = Color(0xFFF0EBE0)
            val glassSubtle = Color(0x08FFFFFF)
            val glassMedium = Color(0x10FFFFFF)
            val glassBorderMedium = Color(0x1AFFFFFF)

            var pressed by remember { mutableStateOf(false) }
            val bgColor = if (pressed) glassMedium else glassSubtle

            val inputModifier = if (!disabled) {
                Modifier.pointerInput(onClick) {
                    detectTapGestures(
                        onPress = {
                            pressed = true
                            val released = tryAwaitRelease()
                            pressed = false
                            if (released) onClick()
                        },
                    )
                }
            } else {
                Modifier
            }

            Box(
                modifier = modifier
                    .csnexusMinimumTouchTarget()
                    .then(inputModifier)
                    .graphicsLayer { if (disabled) alpha = 0.5f }
                    .background(bgColor, shape)
                    .border(1.dp, glassBorderMedium, shape)
                    .semantics { role = Role.Button }
                    .padding(horizontal = 20.dp, vertical = 12.dp),
                contentAlignment = Alignment.Center,
            ) {
                if (loading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = warmWhite,
                    )
                } else {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (leadingIcon != null) leadingIcon()
                        Text(text, color = warmWhite)
                    }
                }
            }
        }
        CSNexusButtonVariant.Ghost -> {
            val shape = RoundedCornerShape(CSNexusDesign.tokens.radius.md)
            val warmWhite = Color(0xFFF0EBE0)
            val glassSubtle = Color(0x08FFFFFF)

            var pressed by remember { mutableStateOf(false) }
            val bgColor = if (pressed) glassSubtle else Color.Transparent

            val inputModifier = if (!disabled) {
                Modifier.pointerInput(onClick) {
                    detectTapGestures(
                        onPress = {
                            pressed = true
                            val released = tryAwaitRelease()
                            pressed = false
                            if (released) onClick()
                        },
                    )
                }
            } else {
                Modifier
            }

            Box(
                modifier = modifier
                    .csnexusMinimumTouchTarget()
                    .then(inputModifier)
                    .graphicsLayer { if (disabled) alpha = 0.5f }
                    .background(bgColor, shape)
                    .semantics { role = Role.Button }
                    .padding(horizontal = 20.dp, vertical = 12.dp),
                contentAlignment = Alignment.Center,
            ) {
                if (loading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = warmWhite,
                    )
                } else {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (leadingIcon != null) leadingIcon()
                        Text(text, color = warmWhite)
                    }
                }
            }
        }
        CSNexusButtonVariant.Danger -> {
            val shape = RoundedCornerShape(CSNexusDesign.tokens.radius.md)
            val dangerGradient = Brush.linearGradient(
                colors = listOf(Color(0xFFD4645C), Color(0xFFE07070)),
            )
            val dangerBorderColor = Color(0x4DD4645C) // danger 30% alpha

            var pressed by remember { mutableStateOf(false) }

            val inputModifier = if (!disabled) {
                Modifier.pointerInput(onClick) {
                    detectTapGestures(
                        onPress = {
                            pressed = true
                            val released = tryAwaitRelease()
                            pressed = false
                            if (released) onClick()
                        },
                    )
                }
            } else {
                Modifier
            }

            // Red glow shadow on press
            val shadowModifier = if (pressed) {
                Modifier.drawWithContent {
                    drawCircle(
                        color = Color(0x4DD4645C),
                        radius = 20.dp.toPx(),
                        center = Offset(size.width / 2f, size.height / 2f),
                    )
                    drawContent()
                }
            } else {
                Modifier
            }

            Box(
                modifier = modifier
                    .csnexusMinimumTouchTarget()
                    .then(shadowModifier)
                    .then(inputModifier)
                    .graphicsLayer { if (disabled) alpha = 0.5f }
                    .background(dangerGradient, shape)
                    .border(1.dp, dangerBorderColor, shape)
                    .semantics { role = Role.Button }
                    .padding(horizontal = 20.dp, vertical = 12.dp),
                contentAlignment = Alignment.Center,
            ) {
                if (loading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(18.dp),
                        strokeWidth = 2.dp,
                        color = Color.White,
                    )
                } else {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        if (leadingIcon != null) leadingIcon()
                        Text(text, color = Color.White)
                    }
                }
            }
        }
    }
}

@Composable
fun CSNexusIconButton(
    contentDescription: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    icon: @Composable () -> Unit,
) {
    IconButton(
        onClick = onClick,
        enabled = enabled,
        modifier = modifier
            .csnexusMinimumTouchTarget()
            .csnexusContentDescription(contentDescription),
    ) {
        icon()
    }
}

@Composable
fun CSNexusTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier,
    singleLine: Boolean = true,
    keyboardOptions: KeyboardOptions = KeyboardOptions.Default,
    visualTransformation: VisualTransformation = VisualTransformation.None,
    isError: Boolean = false,
    supportingText: String? = null,
    placeholder: String? = null,
    leadingIcon: (@Composable () -> Unit)? = null,
) {
    var focused by remember { mutableStateOf(false) }
    val shape = RoundedCornerShape(CSNexusDesign.tokens.radius.lg)

    Box(
        modifier = modifier
            .fillMaxWidth()
            .drawBehind {
                if (focused) {
                    // Primary glow ring: 4px at 15% alpha
                    val glowColor = if (isError) Color(0x26D4645C) else Color(0x26C9A84C)
                    drawRoundRect(
                        color = glowColor,
                        cornerRadius = CornerRadius(20.dp.toPx()),
                        topLeft = Offset(-4.dp.toPx(), -4.dp.toPx()),
                        size = Size(size.width + 8.dp.toPx(), size.height + 8.dp.toPx()),
                    )
                    // Secondary wider glow: 20dp at 20% alpha
                    val secondaryGlow = if (isError) Color(0x33D4645C) else Color(0x33C9A84C)
                    drawRoundRect(
                        color = secondaryGlow,
                        cornerRadius = CornerRadius(24.dp.toPx()),
                        topLeft = Offset(-10.dp.toPx(), -10.dp.toPx()),
                        size = Size(size.width + 20.dp.toPx(), size.height + 20.dp.toPx()),
                    )
                }
            },
    ) {
        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            modifier = Modifier
                .fillMaxWidth()
                .onFocusChanged { focused = it.isFocused },
            label = { Text(label) },
            placeholder = placeholder?.let { { Text(it) } },
            leadingIcon = leadingIcon,
            singleLine = singleLine,
            keyboardOptions = keyboardOptions,
            visualTransformation = visualTransformation,
            isError = isError,
            supportingText = supportingText?.let { { Text(it) } },
            shape = shape,
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = CSNexusDesign.tokens.semantic.glassMedium,
                unfocusedContainerColor = CSNexusDesign.tokens.semantic.glassSubtle,
                disabledContainerColor = CSNexusDesign.tokens.semantic.glassSubtle,
                errorContainerColor = CSNexusDesign.tokens.semantic.glassSubtle,
                focusedBorderColor = if (isError) CSNexusDesign.tokens.semantic.danger else Color(0xFFC9A84C),
                unfocusedBorderColor = CSNexusDesign.tokens.semantic.glassBorderMedium,
                disabledBorderColor = CSNexusDesign.tokens.semantic.glassBorderLight,
                errorBorderColor = CSNexusDesign.tokens.semantic.danger,
                focusedTextColor = MaterialTheme.colorScheme.onSurface,
                unfocusedTextColor = MaterialTheme.colorScheme.onSurface,
                cursorColor = MaterialTheme.colorScheme.primary,
                focusedLabelColor = if (isError) CSNexusDesign.tokens.semantic.danger else Color(0xFFC9A84C),
                unfocusedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
                focusedPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant,
                unfocusedPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant,
            ),
        )
    }
}

@Composable
fun CSNexusOtpField(
    value: String,
    onValueChange: (String) -> Unit,
    length: Int = 6,
    modifier: Modifier = Modifier,
) {
    CSNexusTextField(
        value = value,
        onValueChange = { input -> onValueChange(input.filter(Char::isDigit).take(length)) },
        label = "Verification code",
        modifier = modifier,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
        supportingText = "${value.length}/$length digits",
    )
}

@Composable
fun CSNexusSearchField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    placeholder: String = "Search",
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier.fillMaxWidth(),
        placeholder = { Text(placeholder) },
        leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
        singleLine = true,
        shape = RoundedCornerShape(CSNexusDesign.tokens.radius.md),
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = CSNexusDesign.tokens.semantic.glassMedium,
            unfocusedContainerColor = CSNexusDesign.tokens.semantic.glassSubtle,
            disabledContainerColor = CSNexusDesign.tokens.semantic.glassSubtle,
            errorContainerColor = CSNexusDesign.tokens.semantic.glassSubtle,
            focusedBorderColor = MaterialTheme.colorScheme.primary,
            unfocusedBorderColor = CSNexusDesign.tokens.semantic.glassBorderMedium,
            disabledBorderColor = CSNexusDesign.tokens.semantic.glassBorderLight,
            errorBorderColor = CSNexusDesign.tokens.semantic.danger,
            focusedTextColor = MaterialTheme.colorScheme.onSurface,
            unfocusedTextColor = MaterialTheme.colorScheme.onSurface,
            cursorColor = MaterialTheme.colorScheme.primary,
            focusedLabelColor = MaterialTheme.colorScheme.primary,
            unfocusedLabelColor = MaterialTheme.colorScheme.onSurfaceVariant,
            focusedPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant,
            unfocusedPlaceholderColor = MaterialTheme.colorScheme.onSurfaceVariant,
        ),
    )
}

@Composable
fun CSNexusChip(
    text: String,
    modifier: Modifier = Modifier,
    selected: Boolean = false,
    onClick: (() -> Unit)? = null,
) {
    if (onClick == null) {
        AssistChip(
            onClick = {},
            label = { Text(text) },
            modifier = modifier,
        )
    } else {
        FilterChip(
            selected = selected,
            onClick = onClick,
            label = { Text(text) },
            modifier = modifier.csnexusMinimumTouchTarget(),
        )
    }
}

@Composable
fun CSNexusSegmentedControl(
    options: List<String>,
    selectedIndex: Int,
    onSelected: (Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    Row(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        options.forEachIndexed { index, option ->
            FilterChip(
                selected = selectedIndex == index,
                onClick = { onSelected(index) },
                label = { Text(option) },
                modifier = Modifier
                    .weight(1f)
                    .csnexusMinimumTouchTarget(),
            )
        }
    }
}

@Composable
fun CSNexusTabs(
    tabs: List<String>,
    selectedIndex: Int,
    onSelected: (Int) -> Unit,
    modifier: Modifier = Modifier,
) {
    TabRow(selectedTabIndex = selectedIndex, modifier = modifier) {
        tabs.forEachIndexed { index, label ->
            Tab(
                selected = selectedIndex == index,
                onClick = { onSelected(index) },
                text = { Text(label) },
                modifier = Modifier.csnexusMinimumTouchTarget(),
            )
        }
    }
}

@Composable
fun CSNexusCard(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    content: @Composable () -> Unit,
) {
    if (onClick != null) {
        PremiumCard(
            modifier = modifier.fillMaxWidth(),
            onClick = onClick,
        ) {
            Box(modifier = Modifier.padding(CSNexusDesign.tokens.spacing.lg)) {
                content()
            }
        }
    } else {
        GlassMedium(
            modifier = modifier.fillMaxWidth(),
        ) {
            Box(modifier = Modifier.padding(CSNexusDesign.tokens.spacing.lg)) {
                content()
            }
        }
    }
}

@Composable
fun CSNexusListRow(
    title: String,
    modifier: Modifier = Modifier,
    body: String? = null,
    trailing: (@Composable () -> Unit)? = null,
    onClick: (() -> Unit)? = null,
) {
    CSNexusCard(modifier = modifier, onClick = onClick) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleMedium)
                if (body != null) {
                    Text(
                        text = body,
                        modifier = Modifier.padding(top = 4.dp),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            if (trailing != null) trailing()
        }
    }
}

@Composable
fun CSNexusStatCard(
    title: String,
    value: String,
    body: String,
    modifier: Modifier = Modifier,
    valueColor: Color = MaterialTheme.colorScheme.primary,
) {
    CSNexusCard(modifier = modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(
                text = value,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = androidx.compose.ui.text.font.FontWeight.SemiBold,
                color = valueColor,
            )
            Text(body, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
fun CSNexusConfirmDialog(
    title: String,
    body: String,
    confirmText: String,
    onConfirm: () -> Unit,
    onDismiss: () -> Unit,
    danger: Boolean = false,
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(title) },
        text = { Text(body) },
        confirmButton = {
            CSNexusButton(
                text = confirmText,
                onClick = onConfirm,
                variant = if (danger) CSNexusButtonVariant.Danger else CSNexusButtonVariant.Primary,
            )
        },
        dismissButton = {
            CSNexusButton(
                text = "Cancel",
                onClick = onDismiss,
                variant = CSNexusButtonVariant.Ghost,
            )
        },
    )
}

@Composable
fun CSNexusSkeleton(
    modifier: Modifier = Modifier,
) {
    val shimmerBrush = rememberShimmerBrush()
    Box(
        modifier = modifier
            .background(
                brush = shimmerBrush,
                shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
            )
            .border(
                width = 1.dp,
                color = CSNexusDesign.tokens.semantic.glassBorderLight,
                shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
            ),
    )
}

@Composable
fun CSNexusOfflineBanner(
    modifier: Modifier = Modifier,
    message: String = "Offline. Showing saved data where available.",
) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        color = CSNexusDesign.tokens.semantic.warning.copy(alpha = 0.16f),
        shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
        border = BorderStroke(1.dp, CSNexusDesign.tokens.semantic.warning.copy(alpha = 0.35f)),
    ) {
        Text(
            text = message,
            modifier = Modifier
                .padding(12.dp)
                .semantics { liveRegion = LiveRegionMode.Polite },
            color = MaterialTheme.colorScheme.onSurface,
            style = MaterialTheme.typography.bodyMedium,
        )
    }
}

@Composable
fun CSNexusRetryPanel(
    title: String,
    body: String,
    onRetry: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text(title, style = MaterialTheme.typography.titleMedium)
        Text(body, color = MaterialTheme.colorScheme.onSurfaceVariant)
        CSNexusButton(text = "Retry", onClick = onRetry, variant = CSNexusButtonVariant.Secondary)
    }
}

enum class CSNexusStatusBadgeVariant { Default, Accent }

@Composable
fun CSNexusStatusBadge(
    text: String,
    modifier: Modifier = Modifier,
    color: Color = MaterialTheme.colorScheme.primary,
    variant: CSNexusStatusBadgeVariant = CSNexusStatusBadgeVariant.Default,
    showDot: Boolean = false,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val goldGradient = Brush.linearGradient(
        colors = listOf(Color(0xFFC9A84C), Color(0xFFE8C96A)),
    )

    val badgeBackground = when (variant) {
        CSNexusStatusBadgeVariant.Default -> CSNexusDesign.tokens.semantic.glassSubtle
        CSNexusStatusBadgeVariant.Accent -> Color.Transparent
    }
    val badgeBorderColor = when (variant) {
        CSNexusStatusBadgeVariant.Default -> CSNexusDesign.tokens.semantic.glassBorderMedium
        CSNexusStatusBadgeVariant.Accent -> Color(0xFFC9A84C).copy(alpha = 0.5f)
    }
    val textColor = when (variant) {
        CSNexusStatusBadgeVariant.Default -> color
        CSNexusStatusBadgeVariant.Accent -> Color(0xFFE8C96A)
    }

    val backgroundModifier = when (variant) {
        CSNexusStatusBadgeVariant.Default -> Modifier.background(badgeBackground, RoundedCornerShape(999.dp))
        CSNexusStatusBadgeVariant.Accent -> Modifier.background(goldGradient, RoundedCornerShape(999.dp))
    }

    Box(
        modifier = modifier
            .then(backgroundModifier)
            .border(1.dp, badgeBorderColor, RoundedCornerShape(999.dp)),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            if (showDot) {
                BadgePulseDot(color = textColor, reducedMotion = reducedMotion)
                Spacer(modifier = Modifier.width(6.dp))
            }
            Text(
                text = text,
                color = textColor,
                style = MaterialTheme.typography.labelLarge,
            )
        }
    }
}

@Composable
private fun BadgePulseDot(
    color: Color,
    reducedMotion: Boolean,
    modifier: Modifier = Modifier,
) {
    if (reducedMotion) {
        Box(
            modifier = modifier
                .size(8.dp)
                .background(color, CircleShape),
        )
    } else {
        val infiniteTransition = rememberInfiniteTransition(label = "badge-pulse")
        val scale by infiniteTransition.animateFloat(
            initialValue = 1f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = keyframes {
                    durationMillis = 1500
                    1f at 0 using LinearEasing
                    1.4f at 750 using LinearEasing
                    1f at 1500 using LinearEasing
                },
                repeatMode = RepeatMode.Restart,
            ),
            label = "badge-pulse-scale",
        )
        val alpha by infiniteTransition.animateFloat(
            initialValue = 1f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = keyframes {
                    durationMillis = 1500
                    1f at 0 using LinearEasing
                    0.6f at 750 using LinearEasing
                    1f at 1500 using LinearEasing
                },
                repeatMode = RepeatMode.Restart,
            ),
            label = "badge-pulse-alpha",
        )
        Box(
            modifier = modifier
                .size(8.dp)
                .graphicsLayer {
                    scaleX = scale
                    scaleY = scale
                    this.alpha = alpha
                }
                .background(color, CircleShape),
        )
    }
}

@Composable
fun CSNexusTimerText(
    text: String,
    modifier: Modifier = Modifier,
    urgent: Boolean = false,
) {
    Text(
        text = text,
        modifier = modifier.semantics { liveRegion = LiveRegionMode.Polite },
        color = if (urgent) CSNexusDesign.tokens.semantic.warning else MaterialTheme.colorScheme.onSurface,
        style = MaterialTheme.typography.headlineLarge,
    )
}

@OptIn(ExperimentalMaterial3Api::class)
@Preview(name = "Component states", showBackground = true, backgroundColor = 0xFF080808)
@Composable
private fun CSNexusComponentsPreview() {
    CSNexusTheme(darkTheme = true) {
        var selected by remember { mutableStateOf(0) }
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            CSNexusButton(text = "Continue", onClick = {})
            CSNexusButton(text = "Retry", onClick = {}, variant = CSNexusButtonVariant.Secondary)
            CSNexusButton(text = "Delete", onClick = {}, variant = CSNexusButtonVariant.Danger)
            CSNexusSearchField(value = "", onValueChange = {}, placeholder = "Search lessons")
            CSNexusOtpField(value = "123", onValueChange = {})
            CSNexusSegmentedControl(
                options = listOf("Learn", "Practice", "Review"),
                selectedIndex = selected,
                onSelected = { selected = it },
            )
            CSNexusOfflineBanner()
            CSNexusListRow(title = "Lesson renderer", body = "Tables, formulas, code, checks")
            CSNexusStatusBadge(text = "Syncing")
        }
    }
}

@Preview(name = "Large font", showBackground = true, backgroundColor = 0xFF080808, fontScale = 1.5f)
@Composable
private fun CSNexusLargeFontPreview() {
    CSNexusTheme(darkTheme = true) {
        CSNexusRetryPanel(
            title = "Connection paused",
            body = "Your progress will sync when the device reconnects.",
            onRetry = {},
        )
    }
}
