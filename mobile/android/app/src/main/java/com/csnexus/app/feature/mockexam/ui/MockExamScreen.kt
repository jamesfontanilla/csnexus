package com.csnexus.app.feature.mockexam.ui

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.design.AnimatedNumber
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusDesign
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.CSNexusTimerText
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.ProgressRing
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.feature.mockexam.data.MockExamRepository
import com.csnexus.app.feature.mockexam.data.MockRecommendationDto
import com.csnexus.app.feature.mockexam.data.MockSubtopicBreakdownDto
import com.csnexus.app.feature.quizzes.data.QuizQuestionDto
import com.csnexus.app.feature.quizzes.ui.effectiveCorrectAnswer
import com.csnexus.app.feature.quizzes.ui.effectiveSelectedAnswer

@Composable
fun MockExamScreen(
    repository: MockExamRepository,
    contentPadding: PaddingValues,
    viewModel: MockExamViewModel = viewModel(factory = MockExamViewModelFactory(repository)),
) {
    val state by viewModel.uiState.collectAsState()
    var showExitConfirm by remember { mutableStateOf(false) }
    var showSubmitConfirm by remember { mutableStateOf(false) }
    val lifecycleOwner = LocalLifecycleOwner.current

    BackHandler(enabled = state.phase == MockExamPhase.Active) {
        showExitConfirm = true
    }

    DisposableEffect(lifecycleOwner, state.phase, state.attempt?.effectiveAttemptId) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_STOP && state.phase == MockExamPhase.Active) {
                viewModel.reportFocusLoss("app_backgrounded")
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    if (showExitConfirm) {
        AlertDialog(
            onDismissRequest = { showExitConfirm = false },
            title = { Text("Leave mock exam?") },
            text = { Text("Your server timer keeps running. Submit when you are done, or return quickly to continue.") },
            confirmButton = {
                CSNexusButton(
                    text = "Leave",
                    onClick = {
                        viewModel.reportFocusLoss("exit_confirmed")
                        viewModel.abandonLocalAttempt()
                        showExitConfirm = false
                    },
                    variant = CSNexusButtonVariant.Danger,
                )
            },
            dismissButton = {
                CSNexusButton(
                    text = "Stay",
                    onClick = { showExitConfirm = false },
                    variant = CSNexusButtonVariant.Secondary,
                )
            },
        )
    }

    if (showSubmitConfirm) {
        AlertDialog(
            onDismissRequest = { showSubmitConfirm = false },
            title = { Text("Submit mock exam?") },
            text = { Text("Your answers will be finalized and scored by the server.") },
            confirmButton = {
                CSNexusButton(
                    text = "Submit",
                    onClick = {
                        showSubmitConfirm = false
                        viewModel.submitExam()
                    },
                    loading = state.isSubmitting,
                )
            },
            dismissButton = {
                CSNexusButton(
                    text = "Review",
                    onClick = { showSubmitConfirm = false },
                    variant = CSNexusButtonVariant.Secondary,
                )
            },
        )
    }

    when (state.phase) {
        MockExamPhase.Setup -> MockExamSetup(
            contentPadding = contentPadding,
            errorMessage = state.errorMessage,
            onStart = viewModel::startExam,
        )
        MockExamPhase.Loading -> LoadingState(label = state.statusMessage ?: "Starting mock exam")
        MockExamPhase.Active -> MockExamActive(
            state = state,
            contentPadding = contentPadding,
            onAnswer = viewModel::answer,
            onPrevious = viewModel::previousQuestion,
            onNext = viewModel::nextQuestion,
            onJump = viewModel::goToQuestion,
            onSubmit = { showSubmitConfirm = true },
        )
        MockExamPhase.Submitted -> MockExamSubmitted(
            state = state,
            contentPadding = contentPadding,
            onStartOver = viewModel::abandonLocalAttempt,
            onAcceptRecommendation = viewModel::acceptRecommendation,
        )
    }
}

@Composable
private fun MockExamSetup(
    contentPadding: PaddingValues,
    errorMessage: String?,
    onStart: () -> Unit,
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(contentPadding),
        contentPadding = PaddingValues(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            MetallicText("Mock Exam")
            Text(
                text = "50 questions. 3 hours. 80 percent to pass.",
                modifier = Modifier.padding(top = 6.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        item {
            GlassMedium {
                Column(
                    modifier = Modifier.padding(20.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Text("Before you start", style = MaterialTheme.typography.titleMedium)
                    Text("Once started, other protected learning content may be blocked until the exam is submitted.")
                    Text("Keep the app open. Leaving the exam records a focus-loss event with the backend.")
                    Text("Some exams may use a no-revisit policy after an answer is finalized.")
                }
            }
        }
        if (errorMessage != null) {
            item {
                Text(errorMessage, color = MaterialTheme.colorScheme.error)
            }
        }
        item {
            CSNexusButton(
                text = "Start Mock Exam",
                onClick = onStart,
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

@Composable
private fun MockExamActive(
    state: MockExamUiState,
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
        EmptyMockExam(contentPadding)
        return
    }

    val total = attempt.questions.size.coerceAtLeast(1)
    val progress = (state.currentIndex + 1).toFloat() / total.toFloat()
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        CSNexusStatusBadge(text = "Attempt #${attempt.effectiveAttemptId}")
                        CSNexusStatusBadge(text = attempt.navPolicy)
                        CSNexusStatusBadge(text = "${state.answeredCount}/$total answered")
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(top = 12.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Text("Question ${state.currentIndex + 1} of $total", style = MaterialTheme.typography.headlineMedium)
                        CSNexusTimerText(
                            text = formatDuration(state.remainingSeconds),
                            urgent = state.remainingSeconds in 1..299,
                        )
                    }
                }
            }
            LuxuryProgressBar(
                progress = progress,
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
            )
        }
        item {
            MockQuestionCard(
                question = question,
                isSaving = question.id in state.savingQuestionIds,
                disabled = state.isSubmitting || (state.isLinearNoRevisit && question.finalizedAt != null),
                onAnswer = { onAnswer(question.id, it) },
            )
        }
        item {
            MockQuestionNavigator(
                questions = attempt.questions,
                selectedIndex = state.currentIndex,
                linearNoRevisit = state.isLinearNoRevisit,
                onJump = onJump,
            )
        }
        if (state.statusMessage != null) {
            item {
                Text(state.statusMessage, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        if (state.errorMessage != null) {
            item {
                Text(state.errorMessage, color = MaterialTheme.colorScheme.error)
            }
        }
        item {
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                if (!state.isLinearNoRevisit) {
                    CSNexusButton(
                        text = "Previous",
                        onClick = onPrevious,
                        enabled = state.currentIndex > 0,
                        modifier = Modifier.weight(1f),
                        variant = CSNexusButtonVariant.Secondary,
                    )
                }
                if (state.currentIndex < total - 1) {
                    CSNexusButton(
                        text = "Next",
                        onClick = onNext,
                        modifier = Modifier.weight(1f),
                    )
                } else {
                    CSNexusButton(
                        text = if (state.isSubmitting) "Submitting..." else "Submit Exam",
                        onClick = onSubmit,
                        loading = state.isSubmitting,
                        modifier = Modifier.weight(1f),
                    )
                }
            }
        }
    }
}

@Composable
private fun MockQuestionCard(
    question: QuizQuestionDto,
    isSaving: Boolean,
    disabled: Boolean,
    onAnswer: (String) -> Unit,
) {
    var typedAnswer by remember(question.id) { mutableStateOf(question.effectiveSelectedAnswer.orEmpty()) }
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CSNexusStatusBadge(text = question.qtype)
                if (question.finalizedAt != null) {
                    CSNexusStatusBadge(text = "Finalized")
                }
            }
            Text(question.stem, style = MaterialTheme.typography.titleMedium)
            if (question.options.isNullOrEmpty()) {
                CSNexusTextField(
                    value = typedAnswer,
                    onValueChange = { typedAnswer = it },
                    label = "Your answer",
                    singleLine = false,
                )
                CSNexusButton(
                    text = if (isSaving) "Saving..." else "Save answer",
                    onClick = { onAnswer(typedAnswer.trim()) },
                    enabled = typedAnswer.isNotBlank() && !disabled && !isSaving,
                    loading = isSaving,
                    modifier = Modifier.fillMaxWidth(),
                )
            } else {
                question.options.forEach { option ->
                    MockAnswerOption(
                        text = option,
                        selected = question.effectiveSelectedAnswer == option,
                        disabled = disabled || isSaving,
                        onClick = { onAnswer(option) },
                    )
                }
            }
            if (disabled && question.finalizedAt != null) {
                Text(
                    text = "This answer is finalized for the current navigation policy.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            if (isSaving) {
                Text("Saving answer...", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun MockAnswerOption(
    text: String,
    selected: Boolean,
    disabled: Boolean,
    onClick: () -> Unit,
) {
    val borderColor = when {
        selected -> Color(0xFFC9A84C) // gold accent for selected
        else -> MaterialTheme.colorScheme.outline
    }
    Surface(
        onClick = onClick,
        enabled = !disabled,
        modifier = Modifier.fillMaxWidth().heightIn(min = 56.dp),
        color = if (selected) Color(0xFFC9A84C).copy(alpha = 0.12f) else CSNexusDesign.tokens.semantic.glassSubtle,
        shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
        border = BorderStroke(
            width = if (selected) 2.dp else 1.dp,
            color = borderColor,
        ),
    ) {
        Text(
            text = text,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 14.dp),
            fontWeight = if (selected) FontWeight.SemiBold else FontWeight.Normal,
        )
    }
}

@Composable
private fun MockQuestionNavigator(
    questions: List<QuizQuestionDto>,
    selectedIndex: Int,
    linearNoRevisit: Boolean,
    onJump: (Int) -> Unit,
) {
    LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        itemsIndexed(questions, key = { _, question -> question.id }) { index, question ->
            val answered = question.effectiveSelectedAnswer != null
            val locked = linearNoRevisit && question.finalizedAt != null && index != selectedIndex
            CSNexusButton(
                text = "${index + 1}${if (answered) "*" else ""}",
                onClick = { onJump(index) },
                enabled = !locked,
                variant = if (index == selectedIndex) CSNexusButtonVariant.Primary else CSNexusButtonVariant.Secondary,
            )
        }
    }
}

@Composable
private fun MockExamSubmitted(
    state: MockExamUiState,
    contentPadding: PaddingValues,
    onStartOver: () -> Unit,
    onAcceptRecommendation: () -> Unit,
) {
    val result = state.result
    val review = state.review
    val diagnostic = review?.diagnostic
    val recommendations = review?.recommendations?.recommendations.orEmpty()
    val prediction = review?.prediction
    val reviewQuestions = result?.questions?.ifEmpty { state.attempt?.questions.orEmpty() }
        ?: state.attempt?.questions.orEmpty()
    val maxScore = result?.maxScore?.takeIf { it > 0 } ?: 1
    val score = result?.score ?: 0
    val pct = result?.percentage?.takeIf { it <= 1.0 }?.let { (it * 100).toInt() }
        ?: result?.percentage?.toInt()
        ?: ((score.toFloat() / maxScore.toFloat()) * 100).toInt()

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(contentPadding),
        contentPadding = PaddingValues(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        MetallicText("Mock Exam Results")
                        if (review?.fromCache == true) {
                            CSNexusStatusBadge(text = "Cached")
                        }
                    }
                    ProgressRing(
                        value = pct,
                        modifier = Modifier.size(160.dp),
                        label = "Score",
                    )
                    AnimatedNumber(
                        target = pct,
                        durationMs = 1200,
                        style = MaterialTheme.typography.displayLarge,
                        suffix = "%",
                    )
                    Text(
                        text = "$score/$maxScore",
                        style = MaterialTheme.typography.headlineSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    if (result?.passed != null) {
                        CSNexusStatusBadge(
                            text = if (result.passed) "PASSED" else "NOT PASSED",
                            color = if (result.passed) CSNexusDesign.tokens.semantic.success else CSNexusDesign.tokens.semantic.danger,
                        )
                    }
                    if ((result?.awardedXp ?: 0) > 0) {
                        Text("XP awarded: ${result?.awardedXp}", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (state.isLoadingReview) {
                        Text("Loading diagnostic review...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (state.statusMessage != null) {
                        Text(state.statusMessage, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    if (state.errorMessage != null) {
                        Text(state.errorMessage, color = MaterialTheme.colorScheme.error)
                    }
                }
            }
        }

        if (prediction != null) {
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text("Predicted Score Range", style = MaterialTheme.typography.titleMedium)
                        if (prediction.midpoint != null) {
                            Text(
                                "${prediction.lowerBound?.formatPercent() ?: "-"} - ${prediction.upperBound?.formatPercent() ?: "-"}",
                                style = MaterialTheme.typography.titleLarge,
                            )
                            Text("Midpoint: ${prediction.midpoint.formatPercent()}")
                            if (!prediction.confidenceLevel.isNullOrBlank()) {
                                Text("Confidence: ${prediction.confidenceLevel}", color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        } else if (!prediction.message.isNullOrBlank()) {
                            Text(prediction.message, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }

        if (diagnostic?.highestImpactAreas?.isNotEmpty() == true) {
            item {
                BreakdownSection(
                    title = "Highest Impact Areas",
                    items = diagnostic.highestImpactAreas,
                    highlight = true,
                )
            }
        }

        if (diagnostic?.regressionAlerts?.isNotEmpty() == true) {
            item {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = CSNexusDesign.tokens.semantic.glassMedium,
                    shape = RoundedCornerShape(CSNexusDesign.tokens.radius.lg),
                    border = BorderStroke(2.dp, Color(0xFFE8A838)), // warning amber border
                ) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text("⚠️ Regression Alerts", style = MaterialTheme.typography.titleMedium, color = Color(0xFFE8A838))
                        diagnostic.regressionAlerts.forEach { alert ->
                            Text(
                                "Subtopic #${alert.subtopicId} declined by ${alert.declinePercentagePoints.formatPercent()}",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }
        }

        if (diagnostic != null) {
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text("Performance by Difficulty", style = MaterialTheme.typography.titleMedium)
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            DifficultyCell("Easy", diagnostic.difficultyPerformance.easy, Color(0xFF4CAF50), Modifier.weight(1f))
                            DifficultyCell("Medium", diagnostic.difficultyPerformance.medium, Color(0xFFC9A84C), Modifier.weight(1f))
                            DifficultyCell("Hard", diagnostic.difficultyPerformance.hard, Color(0xFFE57373), Modifier.weight(1f))
                        }
                    }
                }
            }
        }

        if (diagnostic?.subtopicBreakdowns?.isNotEmpty() == true) {
            item {
                BreakdownSection(
                    title = "Full Breakdown",
                    items = diagnostic.subtopicBreakdowns,
                    highlight = false,
                )
            }
        }

        if (result?.perModuleBreakdown?.isNotEmpty() == true || result?.weaknessSummary?.isNotEmpty() == true) {
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text("Module Breakdown", style = MaterialTheme.typography.titleMedium)
                        result.perModuleBreakdown.forEach { item ->
                            Text(
                                "${item.moduleTitle.ifBlank { item.title.ifBlank { "Module #${item.moduleId}" } }}: ${item.score}/${item.max} (${item.pct.formatPercent()})",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                        if (result.weaknessSummary.isNotEmpty()) {
                            Text("Weak Areas", style = MaterialTheme.typography.titleMedium)
                            result.weaknessSummary.forEach { weakness ->
                                Text(
                                    "${weakness.moduleTitle.ifBlank { "Module #${weakness.moduleId}" }}: ${(weakness.percentage.takeIf { it > 0 } ?: weakness.pct).formatPercent()}",
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                )
                            }
                        }
                    }
                }
            }
        }

        if (recommendations.isNotEmpty()) {
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(20.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        Text("Recommendations", style = MaterialTheme.typography.titleMedium)
                        recommendations.forEachIndexed { index, recommendation ->
                            StaggeredItem(index = index) {
                                RecommendationRow(recommendation, onAcceptRecommendation)
                            }
                        }
                    }
                }
            }
        }

        if (reviewQuestions.isNotEmpty()) {
            item {
                MetallicText("Question Review", style = MaterialTheme.typography.titleLarge)
            }
            itemsIndexed(reviewQuestions, key = { _, question -> question.id }) { index, question ->
                StaggeredItem(index = index) {
                    MockReviewQuestion(index, question)
                }
            }
        }

        item {
            CSNexusButton(text = "Back to setup", onClick = onStartOver, modifier = Modifier.fillMaxWidth())
        }
    }
}

@Composable
private fun BreakdownSection(
    title: String,
    items: List<MockSubtopicBreakdownDto>,
    highlight: Boolean,
) {
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            items.forEach { item ->
                BreakdownRow(item = item, highlight = highlight)
            }
        }
    }
}

@Composable
private fun BreakdownRow(item: MockSubtopicBreakdownDto, highlight: Boolean) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = if (highlight) MaterialTheme.colorScheme.error.copy(alpha = 0.08f) else Color.Transparent,
        shape = RoundedCornerShape(CSNexusDesign.tokens.radius.sm),
    ) {
        Row(
            modifier = Modifier.padding(10.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(item.subtopicName.ifBlank { "Subtopic #${item.subtopicId}" }, style = MaterialTheme.typography.titleMedium)
                Text(
                    "${item.questionsCorrect}/${item.questionsAttempted} correct",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Column {
                Text(
                    item.accuracyPercentage.formatPercent(),
                    color = if (item.accuracyPercentage >= 80.0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                    fontWeight = FontWeight.SemiBold,
                )
                if (item.pointsLost > 0) {
                    Text("-${item.pointsLost} pts", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

@Composable
private fun DifficultyCell(label: String, value: Double?, labelColor: Color, modifier: Modifier = Modifier) {
    GlassMedium(modifier = modifier) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(value?.formatPercent() ?: "-", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(label, color = labelColor, fontWeight = FontWeight.Medium)
        }
    }
}

@Composable
private fun RecommendationRow(
    recommendation: MockRecommendationDto,
    onAccept: () -> Unit,
) {
    PremiumCard(
        modifier = Modifier.fillMaxWidth(),
        onClick = if (recommendation.acceptedAt == null) onAccept else null,
    ) {
        Row(
            modifier = Modifier.padding(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    recommendation.formattedString.ifBlank {
                        "${recommendation.subtopicName}: gain +${recommendation.estimatedPointGain.formatOne()} points"
                    },
                    style = MaterialTheme.typography.titleMedium,
                )
                Text(
                    "${recommendation.currentAccuracy.formatPercent()} → ${recommendation.targetAccuracy.formatPercent()} | ${recommendation.recommendedAction}",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            if (recommendation.acceptedAt == null) {
                CSNexusButton(
                    text = "+ Queue",
                    onClick = onAccept,
                    variant = CSNexusButtonVariant.Secondary,
                )
            } else {
                CSNexusStatusBadge(text = "Added", color = CSNexusDesign.tokens.semantic.success)
            }
        }
    }
}

@Composable
private fun MockReviewQuestion(index: Int, question: QuizQuestionDto) {
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
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CSNexusStatusBadge(text = "${index + 1}")
                if (isCorrect != null) {
                    CSNexusStatusBadge(
                        text = if (isCorrect) "Correct" else "Incorrect",
                        color = accent,
                    )
                }
            }
            Text(question.stem, style = MaterialTheme.typography.titleMedium)
            Text("Your answer: ${question.effectiveSelectedAnswer ?: "(none)"}")
            if (isCorrect == false && question.effectiveCorrectAnswer != null) {
                Text("Correct: ${question.effectiveCorrectAnswer}", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            if (!question.explanation.isNullOrBlank()) {
                Text(question.explanation, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun EmptyMockExam(contentPadding: PaddingValues) {
    Column(Modifier.fillMaxSize().padding(contentPadding).padding(24.dp)) {
        MetallicText("No mock exam questions available")
    }
}

private fun formatDuration(seconds: Int): String {
    val h = seconds / 3600
    val m = (seconds % 3600) / 60
    val s = seconds % 60
    return "$h:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}"
}

private fun Double.formatPercent(): String = "${formatOne()}%"

private fun Double.formatOne(): String = if (this % 1.0 == 0.0) {
    toInt().toString()
} else {
    String.format(java.util.Locale.US, "%.1f", this)
}
