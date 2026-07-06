package com.csnexus.app.feature.quizzes.ui

import android.content.Context
import android.graphics.RectF
import android.view.View
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Bolt
import androidx.compose.material.icons.outlined.EditNote
import androidx.compose.material.icons.outlined.MenuBook
import androidx.compose.material.icons.outlined.Timer
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.scale
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.disabled
import androidx.compose.ui.semantics.selected
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.viewmodel.compose.viewModel
import com.caverock.androidsvg.SVG
import com.csnexus.app.core.design.AnimatedNumber
import com.csnexus.app.core.design.CSNexusDesign
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassLarge
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.CSNexusMotion
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.feature.quizzes.data.QuizMode
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import com.csnexus.app.feature.quizzes.data.QuizRepository
import com.csnexus.app.feature.quizzes.data.QuizScope
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

@Composable
fun QuizScreen(
    repository: QuizRepository,
    contentPadding: PaddingValues,
    scope: QuizScope = QuizScope.Subtopic,
    scopeId: Int = 1,
    onOpenLesson: ((Int) -> Unit)? = null,
    onBackToModules: (() -> Unit)? = null,
    viewModel: QuizViewModel = viewModel(factory = QuizViewModelFactory(repository, scope, scopeId)),
) {
    val state by viewModel.uiState.collectAsState()

    when (state.phase) {
        QuizPhase.Loading -> LoadingState(label = state.saveMessage ?: "Assembling your quiz")
        QuizPhase.LessonBlocked -> LessonBlockedState(
            scope = scope,
            scopeId = scopeId,
            contentPadding = contentPadding,
            onOpenLesson = onOpenLesson,
            onBack = viewModel::backToModes,
        )
        QuizPhase.SelectMode -> QuizModeSelection(
            state = state,
            contentPadding = contentPadding,
            onStart = viewModel::startQuiz,
            onBackToModules = onBackToModules,
        )
        QuizPhase.InProgress -> ActiveQuiz(
            state = state,
            contentPadding = contentPadding,
            onAnswer = viewModel::answer,
            onPrevious = viewModel::previousQuestion,
            onNext = viewModel::nextQuestion,
            onJump = viewModel::goToQuestion,
            onSubmit = viewModel::submit,
        )
        QuizPhase.Submitted -> QuizResults(
            state = state,
            contentPadding = contentPadding,
            onTryAgain = viewModel::backToModes,
            onBackToModules = onBackToModules,
        )
    }
}

@Composable
private fun QuizModeSelection(
    state: QuizUiState,
    contentPadding: PaddingValues,
    onStart: (QuizMode) -> Unit,
    onBackToModules: (() -> Unit)?,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        MetallicText("Choose Your Mode")
        Text(
            text = "Questions are drawn from the selected scope and saved as you answer.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        if (state.errorMessage != null) {
            Text(state.errorMessage, color = MaterialTheme.colorScheme.error)
        }
        GlassLarge {
            Column(
                modifier = Modifier.fillMaxWidth().padding(8.dp),
                verticalArrangement = Arrangement.spacedBy(0.dp),
            ) {
                QuizMode.entries.forEach { mode ->
                    val borderColor = mode.quizColor()
                    Surface(
                        onClick = { onStart(mode) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(min = 56.dp)
                            .padding(vertical = 4.dp),
                        shape = RoundedCornerShape(12.dp),
                        color = Color.Transparent,
                        border = BorderStroke(0.dp, Color.Transparent),
                    ) {
                        Row(
                            modifier = Modifier
                                .drawBehind {
                                    // Color-coded left border (3.dp wide)
                                    drawRoundRect(
                                        color = borderColor,
                                        topLeft = Offset.Zero,
                                        size = Size(3.dp.toPx(), size.height),
                                        cornerRadius = CornerRadius(2.dp.toPx()),
                                    )
                                }
                                .padding(start = 12.dp, end = 8.dp, top = 12.dp, bottom = 12.dp),
                            horizontalArrangement = Arrangement.spacedBy(14.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Icon(
                                imageVector = mode.quizIcon(),
                                contentDescription = null,
                                tint = borderColor,
                                modifier = Modifier.size(28.dp),
                            )
                            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text(mode.label, style = MaterialTheme.typography.titleMedium, color = borderColor)
                                Text(mode.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            Text("${mode.timeLimitSeconds / 60}:00", style = MaterialTheme.typography.titleMedium)
                        }
                    }
                }
            }
        }
        if (onBackToModules != null) {
            CSNexusButton(
                text = "Back to Modules",
                onClick = onBackToModules,
                variant = CSNexusButtonVariant.Secondary,
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

@Composable
private fun LessonBlockedState(
    scope: QuizScope,
    scopeId: Int,
    contentPadding: PaddingValues,
    onOpenLesson: ((Int) -> Unit)?,
    onBack: () -> Unit,
) {
    Column(
        modifier = Modifier.fillMaxSize().padding(contentPadding).padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text("Lesson Not Completed", style = MaterialTheme.typography.headlineMedium)
        Text(
            text = "You need to finish reading the lesson before you can take this quiz. Complete the lesson first, then come back here to test your knowledge.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            if (scope == QuizScope.Subtopic && onOpenLesson != null) {
                CSNexusButton(text = "Go to Lesson", onClick = { onOpenLesson(scopeId) })
            }
            CSNexusButton(text = "Back", onClick = onBack, variant = CSNexusButtonVariant.Secondary)
        }
    }
}

@Composable
@OptIn(ExperimentalLayoutApi::class)
private fun ActiveQuiz(
    state: QuizUiState,
    contentPadding: PaddingValues,
    onAnswer: (Int, String) -> Unit,
    onPrevious: () -> Unit,
    onNext: () -> Unit,
    onJump: (Int) -> Unit,
    onSubmit: () -> Unit,
) {
    val attempt = state.attempt
    val question = state.currentQuestion
    if (attempt == null || question == null) {
        Column(Modifier.fillMaxSize().padding(contentPadding).padding(24.dp)) {
            Text("No questions available", style = MaterialTheme.typography.headlineMedium)
        }
        return
    }

    val total = attempt.questions.size.coerceAtLeast(1)
    val modeColor = state.selectedMode?.quizColor() ?: MaterialTheme.colorScheme.primary
    val remainingSeconds = state.remainingSeconds
    val timerExpired = remainingSeconds == 0
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(MaterialTheme.colorScheme.background)
                    .padding(bottom = 10.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Row(
                        modifier = Modifier.padding(12.dp),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = "Question ${state.currentIndex + 1} of $total",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            Text(
                                text = "${state.answeredCount} of $total answered",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.72f),
                            )
                        }
                        if (remainingSeconds != null) {
                            TimerPill(
                                remainingSeconds = remainingSeconds,
                                expired = timerExpired,
                                accent = modeColor,
                            )
                        }
                        state.selectedMode?.let {
                            CSNexusStatusBadge(text = it.label, color = modeColor)
                        }
                    }
                }
                LuxuryProgressBar(
                    progress = (state.currentIndex + 1).toFloat() / total.toFloat(),
                    barColorStart = modeColor,
                    barColorEnd = modeColor.copy(alpha = 0.78f),
                    glowColor = modeColor.copy(alpha = 0.35f),
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                CSNexusStatusBadge(text = "Q ${state.currentIndex + 1}/$total")
                if (question.difficulty.isNotBlank()) {
                    CSNexusStatusBadge(text = question.difficulty.toDisplayLabel(), color = question.difficulty.difficultyColor())
                }
                CSNexusStatusBadge(text = question.qtype)
            }
        }
        item {
            QuestionCard(
                question = question,
                selectedAnswer = question.effectiveSelectedAnswer,
                isSaving = question.id in state.savingQuestionIds,
                isSubmitting = state.isSubmitting,
                onAnswer = { onAnswer(question.id, it) },
            )
        }
        item {
            QuestionJumpGrid(
                questionCount = attempt.questions.size,
                selectedIndex = state.currentIndex,
                statusColor = { index ->
                    if (attempt.questions[index].effectiveSelectedAnswer != null) {
                        modeColor
                    } else {
                        null
                    }
                },
                onSelected = onJump,
            )
        }
        if (state.saveMessage != null) {
            item {
                Text(state.saveMessage, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        if (state.errorMessage != null) {
            item {
                Text(state.errorMessage, color = MaterialTheme.colorScheme.error)
            }
        }
        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                CSNexusButton(
                    text = "Previous",
                    onClick = onPrevious,
                    enabled = state.currentIndex > 0,
                    modifier = Modifier.weight(1f),
                    variant = CSNexusButtonVariant.Secondary,
                )
                CSNexusButton(
                    text = "Next",
                    onClick = onNext,
                    enabled = state.currentIndex < total - 1,
                    modifier = Modifier.weight(1f),
                    variant = CSNexusButtonVariant.Secondary,
                )
            }
        }
        item {
            CSNexusButton(
                text = if (state.isSubmitting) "Submitting..." else "Submit Quiz",
                onClick = onSubmit,
                enabled = state.answeredCount > 0 && !state.isSubmitting,
                loading = state.isSubmitting,
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

@Composable
private fun TimerPill(
    remainingSeconds: Int,
    expired: Boolean,
    accent: Color,
) {
    val color = when {
        expired -> MaterialTheme.colorScheme.error
        remainingSeconds < 30 -> CSNexusDesign.tokens.semantic.danger
        else -> accent
    }
    Surface(
        color = if (expired) MaterialTheme.colorScheme.error.copy(alpha = 0.15f) else CSNexusDesign.tokens.semantic.glassSubtle,
        shape = RoundedCornerShape(999.dp),
        border = BorderStroke(1.dp, color.copy(alpha = 0.45f)),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(
                imageVector = Icons.Outlined.Timer,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(16.dp),
            )
            Text(
                text = if (expired) "Time Expired" else remainingSeconds.formatTimer(),
                color = color,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Monospace,
                style = MaterialTheme.typography.labelLarge,
            )
        }
    }
}

@Composable
private fun QuestionCard(
    question: QuizQuestionDto,
    selectedAnswer: String?,
    isSaving: Boolean,
    isSubmitting: Boolean,
    onAnswer: (String) -> Unit,
) {
    var typedAnswer by remember(question.id) { mutableStateOf(selectedAnswer.orEmpty()) }
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                if (question.difficulty.isNotBlank()) {
                    CSNexusStatusBadge(text = question.difficulty.toDisplayLabel(), color = question.difficulty.difficultyColor())
                }
                CSNexusStatusBadge(text = question.qtype)
            }
            StemContent(question.stem)
            if (question.options.isNullOrEmpty()) {
                CSNexusTextField(
                    value = typedAnswer,
                    onValueChange = { typedAnswer = it },
                    label = "Answer",
                    singleLine = false,
                )
                CSNexusButton(
                    text = if (isSaving) "Saving..." else "Save answer",
                    onClick = { onAnswer(typedAnswer.trim()) },
                    enabled = typedAnswer.isNotBlank() && !isSaving && !isSubmitting,
                    loading = isSaving,
                    modifier = Modifier.fillMaxWidth(),
                )
            } else {
                question.options.forEach { option ->
                    QuizAnswerOption(
                        text = option,
                        selected = selectedAnswer == option,
                        enabled = !isSaving && !isSubmitting,
                        saving = isSaving && selectedAnswer == option,
                        onClick = { onAnswer(option) },
                    )
                }
            }
            AnimatedVisibility(visible = isSaving) {
                Text("Saving answer...", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            if (selectedAnswer != null && !isSaving) {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "Selected:",
                        color = MaterialTheme.colorScheme.primary,
                        style = MaterialTheme.typography.labelLarge,
                    )
                    OptionDisplay(value = selectedAnswer, isCorrect = null)
                }
            }
        }
    }
}

@Composable
private fun QuizAnswerOption(
    text: String,
    selected: Boolean,
    enabled: Boolean,
    saving: Boolean,
    onClick: () -> Unit,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val interactionSource = remember { MutableInteractionSource() }
    val pressed by interactionSource.collectIsPressedAsState()
    val targetScale = when {
        reducedMotion -> 1f
        pressed -> 0.98f
        selected -> 1.02f
        else -> 1f
    }
    val scale by animateFloatAsState(
        targetValue = targetScale,
        animationSpec = if (reducedMotion) CSNexusMotion.instant() else CSNexusMotion.springGentle(),
        label = "answer-scale",
    )
    val borderColor by animateColorAsState(
        targetValue = when {
            selected -> MaterialTheme.colorScheme.primary
            enabled -> MaterialTheme.colorScheme.outline
            else -> MaterialTheme.colorScheme.outlineVariant
        },
        animationSpec = CSNexusMotion.fast(),
        label = "answer-border",
    )
    val containerColor by animateColorAsState(
        targetValue = when {
            selected -> MaterialTheme.colorScheme.primary.copy(alpha = 0.18f)
            enabled -> CSNexusDesign.tokens.semantic.glassSubtle
            else -> MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.38f)
        },
        animationSpec = CSNexusMotion.fast(),
        label = "answer-container",
    )

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 56.dp)
            .scale(scale)
            .selectable(
                selected = selected,
                enabled = enabled,
                role = Role.RadioButton,
                interactionSource = interactionSource,
                indication = null,
                onClick = onClick,
            )
            .semantics {
                this.selected = selected
                stateDescription = when {
                    saving -> "Saving selected answer"
                    selected -> "Selected"
                    !enabled -> "Disabled"
                    else -> "Not selected"
                }
                if (!enabled) disabled()
            },
        color = containerColor,
        shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
        border = BorderStroke(if (selected) 2.dp else 1.dp, borderColor),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Text(
                text = if (selected) "Selected" else "Option",
                color = if (selected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.labelLarge,
            )
            OptionContent(
                value = text,
                modifier = Modifier.weight(1f),
                selected = selected,
            )
            if (saving) {
                Text("Saving", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelLarge)
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun QuestionJumpGrid(
    questionCount: Int,
    selectedIndex: Int?,
    statusColor: (Int) -> Color?,
    onSelected: (Int) -> Unit,
    suffix: (Int) -> String = { "" },
) {
    FlowRow(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(6.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        repeat(questionCount) { index ->
            val active = selectedIndex == index
            val status = statusColor(index)
            val accent = when {
                active -> MaterialTheme.colorScheme.primary
                status != null -> status
                else -> MaterialTheme.colorScheme.outline
            }
            Surface(
                onClick = { onSelected(index) },
                modifier = Modifier.size(34.dp),
                shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
                color = if (status != null) accent.copy(alpha = 0.14f) else CSNexusDesign.tokens.semantic.glassSubtle,
                border = BorderStroke(if (active) 2.dp else 1.dp, accent.copy(alpha = if (active) 0.95f else 0.48f)),
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Text(
                        text = "${index + 1}${suffix(index)}",
                        color = accent,
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                }
            }
        }
    }
}

@Composable
private fun StemContent(text: String) {
    val parsed = remember(text) { parseSvgAware(text) }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        if (parsed.label.isNotBlank()) {
            Text(parsed.label, style = MaterialTheme.typography.titleMedium)
        }
        if (parsed.svg != null) {
            SvgSnippet(
                svg = parsed.svg,
                modifier = Modifier.fillMaxWidth().heightIn(min = 64.dp, max = 180.dp),
            )
        }
    }
}

@Composable
private fun OptionContent(
    value: String,
    selected: Boolean,
    modifier: Modifier = Modifier,
) {
    val parsed = remember(value) { parseSvgAware(value) }
    if (parsed.svg == null) {
        Text(
            text = value,
            modifier = modifier,
            style = MaterialTheme.typography.bodyLarge,
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
        )
    } else {
        Row(
            modifier = modifier,
            horizontalArrangement = Arrangement.spacedBy(10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = parsed.label,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.SemiBold,
            )
            SvgSnippet(
                svg = parsed.svg,
                modifier = Modifier.widthIn(min = 80.dp, max = 220.dp).heightIn(min = 42.dp, max = 96.dp),
            )
        }
    }
}

@Composable
private fun OptionDisplay(
    value: String,
    isCorrect: Boolean?,
) {
    val parsed = remember(value) { parseSvgAware(value) }
    val color = when (isCorrect) {
        true -> CSNexusDesign.tokens.semantic.success
        false -> CSNexusDesign.tokens.semantic.danger
        null -> MaterialTheme.colorScheme.onSurfaceVariant
    }
    if (parsed.svg == null) {
        Text(
            text = value,
            color = color,
            fontFamily = FontFamily.Monospace,
            style = MaterialTheme.typography.bodyMedium,
        )
    } else {
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = parsed.label,
                color = color,
                fontFamily = FontFamily.Monospace,
                fontWeight = FontWeight.SemiBold,
                style = MaterialTheme.typography.bodyMedium,
            )
            SvgSnippet(
                svg = parsed.svg,
                modifier = Modifier.widthIn(min = 64.dp, max = 160.dp).heightIn(min = 36.dp, max = 72.dp),
            )
        }
    }
}

@Composable
private fun SvgSnippet(
    svg: String,
    modifier: Modifier = Modifier,
) {
    AndroidView(
        modifier = modifier,
        factory = { SvgRenderView(it) },
        update = { it.setSvg(svg) },
    )
}

@Composable
private fun QuizResults(
    state: QuizUiState,
    contentPadding: PaddingValues,
    onTryAgain: () -> Unit,
    onBackToModules: (() -> Unit)?,
) {
    val result = state.result
    val fallbackQuestions = state.attempt?.questions.orEmpty()
    val reviewQuestions = result?.questions?.ifEmpty { fallbackQuestions } ?: fallbackQuestions
    val maxScore = result?.maxScore?.takeIf { it > 0 } ?: reviewQuestions.size.coerceAtLeast(1)
    val score = result?.score ?: 0
    val pct = result?.percentage?.takeIf { it <= 1.0 }?.let { (it * 100).toInt() }
        ?: result?.percentage?.toInt()
        ?: ((score.toFloat() / maxScore.toFloat()) * 100).toInt()
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(contentPadding),
        state = listState,
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            ResultSummaryCard(
                score = score,
                maxScore = maxScore,
                percentage = pct,
                awardedXp = result?.awardedXp ?: 0,
            )
        }
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(
                    text = "Jump to Question",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.SemiBold,
                )
                QuestionJumpGrid(
                    questionCount = reviewQuestions.size,
                    selectedIndex = null,
                    statusColor = { index ->
                        when (reviewQuestions[index].isCorrect) {
                            true -> SuccessGreen
                            false -> DangerRed
                            null -> null
                        }
                    },
                    suffix = { index ->
                        when (reviewQuestions[index].isCorrect) {
                            true -> "✓"
                            false -> "x"
                            null -> ""
                        }
                    },
                    onSelected = { index ->
                        scope.launch { listState.animateScrollToItem(index + 2) }
                    },
                )
            }
        }
        itemsIndexed(reviewQuestions, key = { _, question -> question.id }) { index, question ->
            StaggeredItem(index = index) {
                ReviewQuestion(index, question)
            }
        }
        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                CSNexusButton(
                    text = "Try Again",
                    onClick = onTryAgain,
                    modifier = Modifier.weight(1f),
                    variant = CSNexusButtonVariant.Secondary,
                )
                if (onBackToModules != null) {
                    CSNexusButton(
                        text = "Back to Modules",
                        onClick = onBackToModules,
                        modifier = Modifier.weight(1f),
                    )
                }
            }
        }
    }
}

@Composable
private fun ResultSummaryCard(
    score: Int,
    maxScore: Int,
    percentage: Int,
    awardedXp: Int,
) {
    val passed = percentage >= 80
    val scoreScale by animateFloatAsState(
        targetValue = 1f,
        animationSpec = CSNexusMotion.springDefault(),
        label = "result-scale",
    )
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            MetallicText("Quiz Results")
            AnimatedNumber(
                target = percentage,
                durationMs = 1200,
                style = MaterialTheme.typography.displayLarge,
                suffix = "%",
                modifier = Modifier.scale(scoreScale),
            )
            Text(
                text = "$score/$maxScore",
                style = MaterialTheme.typography.headlineSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            CSNexusStatusBadge(
                text = if (passed) "Passing" else "Below passing",
                color = if (passed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
            )
            if (awardedXp > 0) {
                Text("XP awarded: $awardedXp", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun ReviewQuestion(index: Int, question: QuizQuestionDto) {
    val isCorrect = question.isCorrect
    val accent = when (isCorrect) {
        true -> MaterialTheme.colorScheme.primary
        false -> MaterialTheme.colorScheme.error
        null -> MaterialTheme.colorScheme.outline
    }
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = CSNexusDesign.tokens.semantic.glassMedium,
        shape = RoundedCornerShape(CSNexusDesign.tokens.radius.md),
        border = BorderStroke(1.dp, accent.copy(alpha = 0.6f)),
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    CSNexusStatusBadge(text = "${index + 1}")
                    if (isCorrect != null) {
                        CSNexusStatusBadge(
                            text = if (isCorrect) "Correct" else "Incorrect",
                            color = accent,
                        )
                    }
                    if (question.difficulty.isNotBlank()) {
                        val difficultyColor = when (question.difficulty.lowercase()) {
                            "easy" -> CSNexusDesign.tokens.semantic.success
                            "medium" -> Color(0xFFC9A84C)
                            "hard" -> CSNexusDesign.tokens.semantic.danger
                            else -> MaterialTheme.colorScheme.onSurfaceVariant
                        }
                        CSNexusStatusBadge(
                            text = question.difficulty.replaceFirstChar { it.uppercase() },
                            color = difficultyColor,
                        )
                    }
                }
                StemContent(question.stem)
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("Your answer:", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    OptionDisplay(
                        value = question.effectiveSelectedAnswer ?: "(no answer)",
                        isCorrect = isCorrect,
                    )
                }
                val correctAnswer = question.effectiveCorrectAnswer
                if (isCorrect == false && correctAnswer != null) {
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text("Correct:", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        OptionDisplay(value = correctAnswer, isCorrect = true)
                    }
                }
                if (!question.explanation.isNullOrBlank()) {
                    Text(question.explanation, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

private data class SvgAwareText(
    val label: String,
    val svg: String?,
)

private val SuccessGreen = Color(0xFF52B788)
private val GoldAccent = Color(0xFFC9A84C)
private val DangerRed = Color(0xFFD4645C)

private fun parseSvgAware(value: String): SvgAwareText {
    val svgStart = value.indexOf("<svg", ignoreCase = true)
    if (svgStart == -1) return SvgAwareText(label = value, svg = null)
    val label = value.take(svgStart).trim().removeSuffix(":").trim()
    return SvgAwareText(
        label = label,
        svg = sanitizeSvg(value.drop(svgStart).trim()),
    )
}

private fun sanitizeSvg(value: String): String {
    return value
        .replace(Regex("<script[\\s\\S]*?</script>", RegexOption.IGNORE_CASE), "")
        .replace(Regex("<foreignObject[\\s\\S]*?</foreignObject>", RegexOption.IGNORE_CASE), "")
        .replace(Regex("\\son[a-zA-Z]+\\s*=\\s*(['\"]).*?\\1"), "")
        .takeIf { it.startsWith("<svg", ignoreCase = true) && it.contains("</svg>", ignoreCase = true) }
        ?: ""
}

private class SvgRenderView(context: Context) : View(context) {
    private var rawSvg: String = ""
    private var parsedSvg: SVG? = null

    fun setSvg(svg: String) {
        if (rawSvg == svg) return
        rawSvg = svg
        parsedSvg = runCatching { SVG.getFromString(svg) }.getOrNull()
        requestLayout()
        invalidate()
    }

    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        val width = MeasureSpec.getSize(widthMeasureSpec).takeIf { it > 0 } ?: 240
        val documentWidth = parsedSvg?.documentWidth?.takeIf { it > 0f } ?: width.toFloat()
        val documentHeight = parsedSvg?.documentHeight?.takeIf { it > 0f } ?: 96f
        val desiredHeight = (width * (documentHeight / documentWidth))
            .roundToInt()
            .coerceIn(36, 180)
        setMeasuredDimension(width, resolveSize(desiredHeight, heightMeasureSpec))
    }

    override fun onDraw(canvas: android.graphics.Canvas) {
        super.onDraw(canvas)
        val svg = parsedSvg ?: return
        svg.renderToCanvas(canvas, RectF(0f, 0f, width.toFloat(), height.toFloat()))
    }
}

private fun QuizMode.quizColor(): Color = when (this) {
    QuizMode.Practice -> SuccessGreen
    QuizMode.Exam -> GoldAccent
    QuizMode.Sprint -> DangerRed
}

private fun QuizMode.quizIcon(): ImageVector = when (this) {
    QuizMode.Practice -> Icons.Outlined.MenuBook
    QuizMode.Exam -> Icons.Outlined.EditNote
    QuizMode.Sprint -> Icons.Outlined.Bolt
}

@Composable
private fun String.difficultyColor(): Color = when (lowercase()) {
    "easy" -> SuccessGreen
    "medium" -> GoldAccent
    "hard" -> DangerRed
    else -> MaterialTheme.colorScheme.onSurfaceVariant
}

private fun String.toDisplayLabel(): String =
    replaceFirstChar { if (it.isLowerCase()) it.titlecase() else it.toString() }

private fun Int.formatTimer(): String {
    val minutes = this / 60
    val seconds = this % 60
    return "${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}"
}
