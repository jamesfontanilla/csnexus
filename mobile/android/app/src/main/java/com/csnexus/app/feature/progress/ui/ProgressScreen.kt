package com.csnexus.app.feature.progress.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.AnimatedNumber
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusConfirmDialog
import com.csnexus.app.core.design.CSNexusOfflineBanner
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTabs
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.CSNexusStatCard
import com.csnexus.app.core.design.ErrorState
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.ProgressRing
import com.csnexus.app.core.design.ReadinessSkeleton
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.progress.data.DailyGoalDto
import com.csnexus.app.feature.progress.data.FreezeCountDto
import com.csnexus.app.feature.progress.data.GoalBundle
import com.csnexus.app.feature.progress.data.GoalDaySummaryDto
import com.csnexus.app.feature.progress.data.MasteryDto
import com.csnexus.app.feature.progress.data.MasteryRecommendationDto
import com.csnexus.app.feature.progress.data.MasteryReviewDueDto
import com.csnexus.app.feature.progress.data.PlannerReadinessDto
import com.csnexus.app.feature.progress.data.ProgressRepository
import com.csnexus.app.feature.progress.data.ProgressSnapshotDto
import com.csnexus.app.feature.progress.data.ReadinessDashboardDto
import com.csnexus.app.feature.progress.data.ReadinessTrendPointDto
import com.csnexus.app.feature.progress.data.SelfAssessmentHistoryItemDto
import com.csnexus.app.feature.progress.data.SelfAssessmentPromptDto
import com.csnexus.app.feature.progress.data.StudyPlanDto
import com.csnexus.app.feature.progress.data.StudyPlanTaskDto
import com.csnexus.app.feature.progress.data.WeeklyGoalDto
import com.csnexus.app.feature.progress.data.XpDto
import java.time.LocalDate
import java.time.OffsetDateTime
import java.time.format.DateTimeParseException
import kotlin.math.roundToInt
import kotlinx.coroutines.launch

@Composable
fun ProgressScreen(
    repository: ProgressRepository,
    contentPadding: PaddingValues,
    initialSection: ProgressSection = ProgressSection.Analytics,
    onOpenModules: (() -> Unit)? = null,
) {
    val scope = rememberCoroutineScope()
    val goalSyncBannerFlow = repository.goalSyncBanner()
    val goalSyncBanner by (goalSyncBannerFlow?.collectAsState(initial = null) ?: remember { mutableStateOf(null) })
    var selectedSectionIndex by remember(initialSection) { mutableIntStateOf(initialSection.ordinal) }
    var analyticsRangeIndex by remember { mutableIntStateOf(AnalyticsRange.All.ordinal) }

    var xp by remember { mutableStateOf<XpDto?>(null) }
    var snapshot by remember { mutableStateOf<ProgressSnapshotDto?>(null) }
    var readinessDashboard by remember { mutableStateOf<ReadinessDashboardDto?>(null) }
    var mastery by remember { mutableStateOf<List<MasteryDto>>(emptyList()) }
    var weakest by remember { mutableStateOf<List<MasteryDto>>(emptyList()) }
    var dueReviews by remember { mutableStateOf<List<MasteryReviewDueDto>>(emptyList()) }
    var recommendations by remember { mutableStateOf<List<MasteryRecommendationDto>>(emptyList()) }
    var plannerReadiness by remember { mutableStateOf<PlannerReadinessDto?>(null) }
    var readinessTrend by remember { mutableStateOf<List<ReadinessTrendPointDto>>(emptyList()) }
    var selfAssessmentPrompt by remember { mutableStateOf<SelfAssessmentPromptDto?>(null) }
    var selfAssessmentHistory by remember { mutableStateOf<List<SelfAssessmentHistoryItemDto>>(emptyList()) }
    var dailyGoal by remember { mutableStateOf<DailyGoalDto?>(null) }
    var weeklyGoal by remember { mutableStateOf<WeeklyGoalDto?>(null) }
    var freezeCount by remember { mutableStateOf<FreezeCountDto?>(null) }
    var studyPlan by remember { mutableStateOf<StudyPlanDto?>(null) }
    var studyTasks by remember { mutableStateOf<List<StudyPlanTaskDto>>(emptyList()) }

    var analyticsLoading by remember { mutableStateOf(false) }
    var analyticsError by remember { mutableStateOf<String?>(null) }
    var masteryLoading by remember { mutableStateOf(false) }
    var masteryError by remember { mutableStateOf<String?>(null) }
    var goalsLoading by remember { mutableStateOf(false) }
    var goalsError by remember { mutableStateOf<String?>(null) }
    var studyPlanLoading by remember { mutableStateOf(false) }
    var studyPlanError by remember { mutableStateOf<String?>(null) }
    var readinessLoading by remember { mutableStateOf(false) }
    var readinessError by remember { mutableStateOf<String?>(null) }
    var savingGoal by remember { mutableStateOf(false) }
    var creatingPlan by remember { mutableStateOf(false) }
    var deletingPlan by remember { mutableStateOf(false) }
    var submittingAssessment by remember { mutableStateOf(false) }
    var assessmentMessage by remember { mutableStateOf<String?>(null) }
    var showAbandonPlanDialog by remember { mutableStateOf(false) }

    var examDate by remember { mutableStateOf("") }
    var availableHoursPerDay by remember { mutableStateOf("2") }
    var targetScore by remember { mutableStateOf("80") }
    var selfAssessmentScore by remember { mutableStateOf("") }

    fun loadAnalytics(force: Boolean = false) {
        if (analyticsLoading) return
        if (!force && xp != null && snapshot != null && mastery.isNotEmpty() && readinessDashboard != null) return
        analyticsLoading = true
        analyticsError = null
        scope.launch {
            var firstError: String? = null
            when (val result = repository.xp()) {
                is ApiResult.Success -> xp = result.value
                is ApiResult.Failure -> firstError = result.error.userMessage()
            }
            when (val result = repository.snapshot()) {
                is ApiResult.Success -> snapshot = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.readiness()) {
                is ApiResult.Success -> readinessDashboard = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.mastery()) {
                is ApiResult.Success -> mastery = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.weakestMastery()) {
                is ApiResult.Success -> weakest = result.value
                is ApiResult.Failure -> Unit
            }
            analyticsError = firstError
            analyticsLoading = false
        }
    }

    fun loadMastery(force: Boolean = false) {
        if (masteryLoading) return
        if (!force && mastery.isNotEmpty() && dueReviews.isNotEmpty() && recommendations.isNotEmpty()) {
            return
        }
        masteryLoading = true
        masteryError = null
        scope.launch {
            var firstError: String? = null
            if (mastery.isEmpty() || force) {
                when (val result = repository.mastery()) {
                    is ApiResult.Success -> mastery = result.value
                    is ApiResult.Failure -> firstError = result.error.userMessage()
                }
            }
            when (val result = repository.dueReviews()) {
                is ApiResult.Success -> dueReviews = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.recommendations()) {
                is ApiResult.Success -> recommendations = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            if (weakest.isEmpty()) {
                when (val result = repository.weakestMastery()) {
                    is ApiResult.Success -> weakest = result.value
                    is ApiResult.Failure -> Unit
                }
            }
            masteryError = firstError
            masteryLoading = false
        }
    }

    fun loadGoals(force: Boolean = false) {
        if (goalsLoading) return
        if (!force && dailyGoal != null && weeklyGoal != null && freezeCount != null) return
        goalsLoading = true
        goalsError = null
        scope.launch {
            var firstError: String? = null
            when (val result = repository.dailyGoal()) {
                is ApiResult.Success -> dailyGoal = result.value
                is ApiResult.Failure -> firstError = result.error.userMessage()
            }
            when (val result = repository.weeklyGoal()) {
                is ApiResult.Success -> weeklyGoal = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.freezeCount()) {
                is ApiResult.Success -> freezeCount = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            goalsError = firstError
            goalsLoading = false
        }
    }

    fun loadStudyPlan(force: Boolean = false) {
        if (studyPlanLoading) return
        if (!force && studyPlan != null) return
        studyPlanLoading = true
        studyPlanError = null
        scope.launch {
            when (val planResult = repository.studyPlan()) {
                is ApiResult.Success -> {
                    studyPlan = planResult.value
                    if (planResult.value != null) {
                        when (val tasksResult = repository.todayPlanTasks()) {
                            is ApiResult.Success -> studyTasks = tasksResult.value
                            is ApiResult.Failure -> studyPlanError = tasksResult.error.userMessage()
                        }
                    } else {
                        studyTasks = emptyList()
                    }
                }
                is ApiResult.Failure -> studyPlanError = planResult.error.userMessage()
            }
            studyPlanLoading = false
        }
    }

    fun loadReadiness(force: Boolean = false) {
        if (readinessLoading) return
        if (!force && readinessDashboard != null && plannerReadiness != null) return
        readinessLoading = true
        readinessError = null
        scope.launch {
            var firstError: String? = null
            when (val result = repository.readiness()) {
                is ApiResult.Success -> readinessDashboard = result.value
                is ApiResult.Failure -> firstError = result.error.userMessage()
            }
            when (val result = repository.plannerReadiness()) {
                is ApiResult.Success -> plannerReadiness = result.value
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.readinessTrend()) {
                is ApiResult.Success -> readinessTrend = result.value.trend
                is ApiResult.Failure -> if (firstError == null) firstError = result.error.userMessage()
            }
            when (val result = repository.selfAssessmentPrompt()) {
                is ApiResult.Success -> selfAssessmentPrompt = result.value
                is ApiResult.Failure -> Unit
            }
            when (val result = repository.selfAssessmentHistory()) {
                is ApiResult.Success -> selfAssessmentHistory = result.value.records
                is ApiResult.Failure -> Unit
            }
            readinessError = firstError
            readinessLoading = false
        }
    }

    fun updateGoalTarget(target: Int) {
        val previous = dailyGoal
        if (previous == null || savingGoal) return
        savingGoal = true
        goalsError = null
        dailyGoal = previous.copy(targetXp = target)
        scope.launch {
            when (val result = repository.updateGoalTarget(target)) {
                is ApiResult.Success -> applyGoalBundle(
                    bundle = result.value,
                    setGoal = { dailyGoal = it },
                    setWeekly = { weeklyGoal = it },
                    setFreezes = { freezeCount = it },
                )
                is ApiResult.Failure -> {
                    dailyGoal = previous
                    goalsError = result.error.userMessage()
                }
            }
            savingGoal = false
        }
    }

    fun createStudyPlan() {
        val hours = availableHoursPerDay.toDoubleOrNull()
        val score = targetScore.toDoubleOrNull()?.div(100.0)
        if (examDate.isBlank() || hours == null || score == null || creatingPlan) return
        creatingPlan = true
        studyPlanError = null
        scope.launch {
            when (val result = repository.createStudyPlan(examDate, hours, score)) {
                is ApiResult.Success -> {
                    studyPlan = result.value.first
                    studyTasks = result.value.second
                }
                is ApiResult.Failure -> studyPlanError = result.error.userMessage()
            }
            creatingPlan = false
        }
    }

    fun completeTask(taskId: Int) {
        scope.launch {
            when (val result = repository.completeStudyTask(taskId)) {
                is ApiResult.Success -> {
                    studyTasks = studyTasks.map { task ->
                        if (task.id == taskId) task.copy(completed = true) else task
                    }
                }
                is ApiResult.Failure -> studyPlanError = result.error.userMessage()
            }
        }
    }

    fun abandonPlan() {
        if (deletingPlan) return
        deletingPlan = true
        scope.launch {
            when (val result = repository.abandonStudyPlan()) {
                is ApiResult.Success -> {
                    studyPlan = null
                    studyTasks = emptyList()
                    showAbandonPlanDialog = false
                }
                is ApiResult.Failure -> studyPlanError = result.error.userMessage()
            }
            deletingPlan = false
        }
    }

    fun submitAssessment() {
        val score = selfAssessmentScore.toIntOrNull()
        if (score == null || score !in 0..100 || submittingAssessment) return
        submittingAssessment = true
        assessmentMessage = null
        scope.launch {
            when (val result = repository.submitSelfAssessment(score)) {
                is ApiResult.Success -> {
                    assessmentMessage = result.value.message.ifBlank {
                        "Saved self-assessment at $score%."
                    }
                    loadReadiness(force = true)
                }
                is ApiResult.Failure -> assessmentMessage = result.error.userMessage()
            }
            submittingAssessment = false
        }
    }

    LaunchedEffect(selectedSectionIndex) {
        when (ProgressSection.entries[selectedSectionIndex]) {
            ProgressSection.Analytics -> loadAnalytics()
            ProgressSection.Mastery -> loadMastery()
            ProgressSection.Goals -> loadGoals()
            ProgressSection.StudyPlan -> {
                loadStudyPlan()
                if (recommendations.isEmpty()) loadMastery()
            }
            ProgressSection.Readiness -> loadReadiness()
        }
    }

    val analyticsModel = remember(
        analyticsRangeIndex,
        xp,
        mastery,
        weakest,
        snapshot,
        readinessDashboard,
    ) {
        buildAnalyticsModel(
            xpStreak = xp?.streak ?: 0,
            mastery = mastery,
            weakest = weakest,
            snapshot = snapshot,
            readiness = readinessDashboard,
            range = AnalyticsRange.entries[analyticsRangeIndex],
        )
    }

    if (showAbandonPlanDialog) {
        CSNexusConfirmDialog(
            title = "Abandon study plan?",
            body = "This removes the current plan and today's tasks on this device until the server says otherwise.",
            confirmText = if (deletingPlan) "Removing..." else "Abandon",
            onConfirm = ::abandonPlan,
            onDismiss = { showAbandonPlanDialog = false },
            danger = true,
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
    ) {
        CSNexusTabs(
            tabs = ProgressSection.entries.map { it.label },
            selectedIndex = selectedSectionIndex,
            onSelected = { selectedSectionIndex = it },
        )
        when (ProgressSection.entries[selectedSectionIndex]) {
            ProgressSection.Analytics -> AnalyticsSection(
                loading = analyticsLoading,
                error = analyticsError,
                model = analyticsModel,
                selectedRangeIndex = analyticsRangeIndex,
                onSelectRange = { analyticsRangeIndex = it },
                onRetry = { loadAnalytics(force = true) },
            )
            ProgressSection.Mastery -> MasterySection(
                loading = masteryLoading,
                error = masteryError,
                mastery = mastery,
                dueReviews = dueReviews,
                recommendations = recommendations,
                onRetry = { loadMastery(force = true) },
                onOpenModules = onOpenModules,
            )
            ProgressSection.Goals -> GoalsSection(
                loading = goalsLoading,
                error = goalsError,
                dailyGoal = dailyGoal,
                weeklyGoal = weeklyGoal,
                freezeCount = freezeCount,
                savingGoal = savingGoal,
                syncMessage = goalSyncBanner?.message,
                onSelectGoalTarget = ::updateGoalTarget,
                onRetrySync = {
                    scope.launch {
                        when (val result = repository.retryGoalSync()) {
                            is ApiResult.Success -> if (result.value > 0) loadGoals(force = true)
                            is ApiResult.Failure -> goalsError = result.error.userMessage()
                        }
                    }
                },
                onRetry = { loadGoals(force = true) },
            )
            ProgressSection.StudyPlan -> StudyPlanSection(
                loading = studyPlanLoading,
                error = studyPlanError,
                studyPlan = studyPlan,
                tasks = studyTasks,
                recommendations = recommendations,
                examDate = examDate,
                onExamDateChange = { examDate = it },
                availableHoursPerDay = availableHoursPerDay,
                onAvailableHoursChange = { availableHoursPerDay = it },
                targetScore = targetScore,
                onTargetScoreChange = { targetScore = it },
                creating = creatingPlan,
                onCreate = ::createStudyPlan,
                onCompleteTask = ::completeTask,
                onAbandon = { showAbandonPlanDialog = true },
                onRetry = { loadStudyPlan(force = true) },
            )
            ProgressSection.Readiness -> ReadinessSection(
                loading = readinessLoading,
                error = readinessError,
                dashboard = readinessDashboard,
                plannerReadiness = plannerReadiness,
                trend = readinessTrend,
                prompt = selfAssessmentPrompt,
                history = selfAssessmentHistory,
                selfAssessmentScore = selfAssessmentScore,
                onSelfAssessmentScoreChange = { selfAssessmentScore = it.filter(Char::isDigit).take(3) },
                submittingAssessment = submittingAssessment,
                assessmentMessage = assessmentMessage,
                onSubmitAssessment = ::submitAssessment,
                onRetry = { loadReadiness(force = true) },
            )
        }
    }
}

@Composable
private fun AnalyticsSection(
    loading: Boolean,
    error: String?,
    model: AnalyticsModel,
    selectedRangeIndex: Int,
    onSelectRange: (Int) -> Unit,
    onRetry: () -> Unit,
) {
    if (loading) {
        LoadingState(label = "Loading analytics", modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && model.totalSessions == 0 && model.strongest.isEmpty() && model.weakest.isEmpty()) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    var selectedTrendIndex by remember(model.accuracyTrend) { mutableIntStateOf((model.accuracyTrend.size - 1).coerceAtLeast(0)) }
    var selectedHeatmapIndex by remember(model.consistencyHeatmap) { mutableIntStateOf((model.consistencyHeatmap.size - 1).coerceAtLeast(0)) }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                MetallicText(
                    text = "Learner analytics",
                    style = MaterialTheme.typography.headlineMedium,
                )
                Text(
                    model.accessibleSummary,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.semantics { contentDescription = model.accessibleSummary },
                )
                CSNexusSegmentedControl(
                    options = AnalyticsRange.entries.map { it.label },
                    selectedIndex = selectedRangeIndex,
                    onSelected = onSelectRange,
                )
            }
        }
        if (error != null) {
            item {
                InlineErrorCard(message = error, onRetry = onRetry)
            }
        }
        if (model.totalSessions == 0 && model.strongest.isEmpty() && model.weakest.isEmpty()) {
            item {
                EmptyCard(
                    title = "No analytics yet",
                    body = "Complete lessons, quizzes, or flashcard sessions and this screen will start breathing.",
                )
            }
        } else {
            // 4 stat cards grid with icon + title + AnimatedNumber + trend
            item {
                AnalyticsStatGrid(model = model)
            }
            // Mastery distribution donut chart
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Text("Mastery distribution", style = MaterialTheme.typography.titleMedium)
                        if (model.distribution.isEmpty()) {
                            Text("No mastery buckets inside this time range yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        } else {
                            AnalyticsDonutChart(distribution = model.distribution)
                        }
                    }
                }
            }
            // Accuracy trend line chart
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Text("Accuracy trend", style = MaterialTheme.typography.titleMedium)
                        if (model.accuracyTrend.isEmpty()) {
                            Text("Not enough dated practice yet to draw a trend.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        } else {
                            AnalyticsLineChart(points = model.accuracyTrend)
                            Row(
                                modifier = Modifier.horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                model.accuracyTrend.forEachIndexed { index, point ->
                                    CSNexusChip(
                                        text = "${point.label} ${point.accuracyPercent}%",
                                        selected = selectedTrendIndex == index,
                                        onClick = { selectedTrendIndex = index },
                                    )
                                }
                            }
                            val selected = model.accuracyTrend[selectedTrendIndex]
                            Text(
                                "${selected.label}: ${selected.accuracyPercent}% accuracy across ${selected.sessions} attempts.",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }
            // Study consistency heatmap
            item {
                GlassMedium(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        Text("Study consistency", style = MaterialTheme.typography.titleMedium)
                        if (model.consistencyHeatmap.isEmpty()) {
                            Text("No dated study activity in this range yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        } else {
                            AnalyticsHeatmapChart(entries = model.consistencyHeatmap.takeLast(14))
                            Row(
                                modifier = Modifier.horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                model.consistencyHeatmap.takeLast(14).forEachIndexed { index, entry ->
                                    CSNexusChip(
                                        text = "${entry.label} ${entry.count}",
                                        selected = selectedHeatmapIndex == index,
                                        onClick = { selectedHeatmapIndex = index },
                                    )
                                }
                            }
                            val selected = model.consistencyHeatmap.takeLast(14)[selectedHeatmapIndex.coerceAtMost(model.consistencyHeatmap.takeLast(14).lastIndex)]
                            Text(
                                "${selected.label}: ${selected.count} practiced subtopics logged.",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }
            // 2-column strengths/weaknesses with colored LuxuryProgressBars
            item {
                AnalyticsStrengthsWeaknesses(
                    strongest = model.strongest,
                    weakest = model.weakest,
                )
            }
        }
    }
}

@Composable
private fun MasterySection(
    loading: Boolean,
    error: String?,
    mastery: List<MasteryDto>,
    dueReviews: List<MasteryReviewDueDto>,
    recommendations: List<MasteryRecommendationDto>,
    onRetry: () -> Unit,
    onOpenModules: (() -> Unit)?,
) {
    if (loading && mastery.isEmpty() && dueReviews.isEmpty() && recommendations.isEmpty()) {
        LoadingState(label = "Loading mastery", modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && mastery.isEmpty() && dueReviews.isEmpty() && recommendations.isEmpty()) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    val levelCounts = mastery.groupingBy { it.masteryLevel }.eachCount()

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                MetallicText(
                    text = "Mastery dashboard",
                    style = MaterialTheme.typography.headlineMedium,
                )
                if (onOpenModules != null) {
                    CSNexusButton(
                        text = "Open modules",
                        onClick = onOpenModules,
                        variant = CSNexusButtonVariant.Secondary,
                    )
                }
            }
        }
        if (error != null) {
            item { InlineErrorCard(message = error, onRetry = onRetry) }
        }
        // Level-count colored pills row
        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                masteryOrderLabels.forEach { level ->
                    val count = levelCounts[level] ?: 0
                    CSNexusStatusBadge(
                        text = "${level.replaceFirstChar { it.titlecase() }}: $count",
                        color = masteryLevelColor(level),
                    )
                }
            }
        }
        // Due for review list
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    Text("Due for review", style = MaterialTheme.typography.titleMedium)
                    if (dueReviews.isEmpty()) {
                        Text("Nothing is overdue right now.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        dueReviews.forEach { review ->
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                            ) {
                                Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                                    Text(review.subtopicTitle, fontWeight = FontWeight.SemiBold)
                                    Text(
                                        "Every ${review.intervalDays} days",
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        style = MaterialTheme.typography.bodySmall,
                                    )
                                }
                                Text(
                                    "${review.daysOverdue.roundToInt()}d overdue",
                                    color = MaterialTheme.colorScheme.error,
                                )
                            }
                        }
                    }
                }
            }
        }
        // Recommendations card
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    Text("Recommended next", style = MaterialTheme.typography.titleMedium)
                    if (recommendations.isEmpty()) {
                        Text("Recommendations will appear after more progress signals arrive.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        recommendations.forEach { recommendation ->
                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Text(recommendation.subtopicTitle, fontWeight = FontWeight.SemiBold)
                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    CSNexusStatusBadge(text = reasonLabel(recommendation.reason))
                                    CSNexusStatusBadge(text = recommendation.recommendedDifficulty.ifBlank { "standard" })
                                    CSNexusStatusBadge(text = "P${recommendation.priority}")
                                }
                            }
                        }
                    }
                }
            }
        }
        item {
            Text("Subtopic mastery", style = MaterialTheme.typography.titleLarge)
        }
        if (mastery.isEmpty()) {
            item {
                EmptyCard(
                    title = "No mastery data",
                    body = "This section stays quiet until practice attempts come in.",
                )
            }
        } else {
            items(mastery.size) { index ->
                val item = mastery[index]
                val levelColor = masteryLevelColor(item.masteryLevel)
                val glowAlpha = levelColor.copy(alpha = 0.4f)
                StaggeredItem(index = index) {
                    GlassMedium(modifier = Modifier.fillMaxWidth()) {
                        Column(
                            modifier = Modifier.padding(16.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically,
                            ) {
                                Text(
                                    item.subtopicTitle,
                                    style = MaterialTheme.typography.titleMedium,
                                    modifier = Modifier.weight(1f),
                                )
                                CSNexusStatusBadge(
                                    text = item.masteryLevel.replaceFirstChar { it.titlecase() },
                                    color = levelColor,
                                )
                            }
                            LuxuryProgressBar(
                                progress = item.masteryScore.toFloat().coerceIn(0f, 1f),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .semantics {
                                        contentDescription = "${item.subtopicTitle} mastery ${percent(item.masteryScore)}"
                                    },
                                barColorStart = levelColor,
                                barColorEnd = levelColor.copy(alpha = 0.7f),
                                glowColor = glowAlpha,
                            )
                            Text(
                                "${item.correctAttempts}/${item.totalAttempts} correct attempts",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.bodySmall,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun GoalsSection(
    loading: Boolean,
    error: String?,
    dailyGoal: DailyGoalDto?,
    weeklyGoal: WeeklyGoalDto?,
    freezeCount: FreezeCountDto?,
    savingGoal: Boolean,
    syncMessage: String?,
    onSelectGoalTarget: (Int) -> Unit,
    onRetrySync: () -> Unit,
    onRetry: () -> Unit,
) {
    if (loading && dailyGoal == null) {
        LoadingState(label = "Loading goals", modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && dailyGoal == null) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            MetallicText(
                text = "Daily goals",
                style = MaterialTheme.typography.headlineMedium,
            )
        }
        if (syncMessage != null) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    CSNexusOfflineBanner(message = syncMessage)
                    CSNexusButton(
                        text = "Retry sync",
                        onClick = onRetrySync,
                        variant = CSNexusButtonVariant.Ghost,
                    )
                }
            }
        }
        if (error != null) {
            item { InlineErrorCard(message = error, onRetry = onRetry) }
        }
        // Daily XP progress ring (120dp, gold stroke)
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    if (dailyGoal == null) {
                        Text("No daily goal data is available yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        val dailyXpPercent = ((dailyGoal.currentXp.toFloat() / dailyGoal.targetXp.toFloat().coerceAtLeast(1f)) * 100)
                            .roundToInt()
                            .coerceIn(0, 100)
                        ProgressRing(
                            value = dailyXpPercent,
                            ringSize = 120.dp,
                            label = "Daily XP",
                        )
                        Text(
                            "${dailyGoal.currentXp}/${dailyGoal.targetXp} XP",
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.SemiBold,
                        )
                        if (dailyGoal.completed) {
                            CSNexusStatusBadge(text = "Goal complete", color = Color(0xFF4CAF50))
                        }
                    }
                }
            }
        }
        // Target selector: row of glass toggle buttons, active = primary
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    Text("Daily XP target", style = MaterialTheme.typography.titleMedium)
                    val targets = goalTargetOptions(dailyGoal?.targetXp ?: 0)
                    Row(
                        modifier = Modifier.horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        targets.forEach { target ->
                            val isActive = dailyGoal?.targetXp == target
                            CSNexusButton(
                                text = "$target XP",
                                onClick = { onSelectGoalTarget(target) },
                                variant = if (isActive) CSNexusButtonVariant.Primary else CSNexusButtonVariant.Ghost,
                                modifier = Modifier.semantics {
                                    contentDescription = "$target XP target${if (isActive) ", selected" else ""}"
                                },
                            )
                        }
                    }
                    if (savingGoal) {
                        Text("Saving goal target...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
        // Streak freeze indicator
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Row(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Text("🧊", style = MaterialTheme.typography.titleLarge)
                        Text("Streak freezes", style = MaterialTheme.typography.titleMedium)
                    }
                    AnimatedNumber(
                        target = freezeCount?.available ?: 0,
                        style = MaterialTheme.typography.headlineMedium,
                    )
                }
            }
        }
        // Weekly calendar grid (7-col, completed = green circles)
        item {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    val weekly = weeklyGoal
                    Text(
                        if (weekly == null) "This week" else "This week (${weekly.completedCount}/${weekly.totalDays})",
                        style = MaterialTheme.typography.titleMedium,
                    )
                    if (weekly == null || weekly.days.isEmpty()) {
                        Text("Weekly goal history is empty.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        WeeklyCalendarGrid(days = weekly.days)
                    }
                }
            }
        }
    }
}

@Composable
private fun StudyPlanSection(
    loading: Boolean,
    error: String?,
    studyPlan: StudyPlanDto?,
    tasks: List<StudyPlanTaskDto>,
    recommendations: List<MasteryRecommendationDto>,
    examDate: String,
    onExamDateChange: (String) -> Unit,
    availableHoursPerDay: String,
    onAvailableHoursChange: (String) -> Unit,
    targetScore: String,
    onTargetScoreChange: (String) -> Unit,
    creating: Boolean,
    onCreate: () -> Unit,
    onCompleteTask: (Int) -> Unit,
    onAbandon: () -> Unit,
    onRetry: () -> Unit,
) {
    if (loading && studyPlan == null) {
        LoadingState(label = "Loading study plan", modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && studyPlan == null) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item { Text("Study plan", style = MaterialTheme.typography.headlineMedium) }
        if (error != null) {
            item { InlineErrorCard(message = error, onRetry = onRetry) }
        }
        if (studyPlan == null) {
            item {
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Text("Create a study plan", style = MaterialTheme.typography.titleMedium)
                        CSNexusTextField(
                            value = examDate,
                            onValueChange = onExamDateChange,
                            label = "Target exam date (YYYY-MM-DD)",
                        )
                        CSNexusTextField(
                            value = availableHoursPerDay,
                            onValueChange = { onAvailableHoursChange(it.filter { char -> char.isDigit() || char == '.' }) },
                            label = "Hours per day",
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                        )
                        CSNexusTextField(
                            value = targetScore,
                            onValueChange = { onTargetScoreChange(it.filter(Char::isDigit).take(3)) },
                            label = "Target score (%)",
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        )
                        CSNexusButton(
                            text = if (creating) "Creating..." else "Create plan",
                            onClick = onCreate,
                            loading = creating,
                            enabled = examDate.isNotBlank(),
                        )
                    }
                }
            }
            if (recommendations.isNotEmpty()) {
                item {
                    CSNexusCard {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("Start here", style = MaterialTheme.typography.titleMedium)
                            recommendations.take(3).forEach { recommendation ->
                                Text("${recommendation.subtopicTitle} - ${reasonLabel(recommendation.reason)}")
                            }
                        }
                    }
                }
            }
        } else {
            item {
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text("Plan overview", style = MaterialTheme.typography.titleMedium)
                        Text("Exam: ${studyPlan.targetExamDate}")
                        Text("${studyPlan.daysRemaining} days remaining - ${studyPlan.availableHoursPerDay}h/day")
                        LinearProgressIndicator(
                            progress = { (studyPlan.completionPercentage / 100.0).toFloat().coerceIn(0f, 1f) },
                            modifier = Modifier.fillMaxWidth(),
                        )
                        Text("${studyPlan.completionPercentage.roundToInt()}% complete", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        CSNexusButton(
                            text = "Abandon plan",
                            onClick = onAbandon,
                            variant = CSNexusButtonVariant.Danger,
                        )
                    }
                }
            }
            item {
                Text("Today's tasks", style = MaterialTheme.typography.titleLarge)
            }
            if (tasks.isEmpty()) {
                item {
                    EmptyCard(
                        title = "No tasks today",
                        body = "The current plan has nothing scheduled for today.",
                    )
                }
            } else {
                items(tasks, key = { it.id }) { task ->
                    CSNexusCard {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text(task.subtopicTitle, style = MaterialTheme.typography.titleMedium)
                            Text(
                                "${task.activityType} - ${task.estimatedMinutes} min",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                            CSNexusButton(
                                text = if (task.completed) "Completed" else "Mark complete",
                                onClick = { onCompleteTask(task.id) },
                                enabled = !task.completed,
                                variant = if (task.completed) CSNexusButtonVariant.Secondary else CSNexusButtonVariant.Primary,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ReadinessSection(
    loading: Boolean,
    error: String?,
    dashboard: ReadinessDashboardDto?,
    plannerReadiness: PlannerReadinessDto?,
    trend: List<ReadinessTrendPointDto>,
    prompt: SelfAssessmentPromptDto?,
    history: List<SelfAssessmentHistoryItemDto>,
    selfAssessmentScore: String,
    onSelfAssessmentScoreChange: (String) -> Unit,
    submittingAssessment: Boolean,
    assessmentMessage: String?,
    onSubmitAssessment: () -> Unit,
    onRetry: () -> Unit,
) {
    if (loading && dashboard == null && plannerReadiness == null) {
        ReadinessSkeleton(modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && dashboard == null && plannerReadiness == null) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    val readinessScore = plannerReadiness?.readinessPercentage ?: dashboard?.score?.roundToInt() ?: 0
    val confidenceLevel = plannerReadiness?.confidenceLevel ?: dashboard?.readinessLevel.orEmpty()
    val readinessSummary = readinessAccessibleSummary(
        readinessScore = readinessScore,
        confidenceLevel = confidenceLevel,
        passingProbability = plannerReadiness?.passingProbability ?: 0.0,
        predictedScore = plannerReadiness?.predictedScore ?: 0.0,
    )
    var selectedTrendIndex by remember(trend) { mutableIntStateOf((trend.size - 1).coerceAtLeast(0)) }

    // Confidence-based border color
    val confidenceColor = when {
        confidenceLevel.contains("high", ignoreCase = true) -> Color(0xFF4CAF50)
        confidenceLevel.contains("medium", ignoreCase = true) -> Color(0xFFC9A84C)
        confidenceLevel.contains("low", ignoreCase = true) -> Color(0xFFE57373)
        else -> Color(0xFFC9A84C)
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Column(
                verticalArrangement = Arrangement.spacedBy(8.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.fillMaxWidth(),
            ) {
                MetallicText(
                    text = "Exam readiness",
                    style = MaterialTheme.typography.headlineMedium,
                )
                Text(
                    readinessSummary,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.semantics { contentDescription = readinessSummary },
                )
            }
        }
        if (error != null) {
            item { InlineErrorCard(message = error, onRetry = onRetry) }
        }
        if (dashboard == null && plannerReadiness == null) {
            item {
                EmptyCard(
                    title = "No readiness data",
                    body = "Complete more lessons and quizzes to unlock a readiness forecast.",
                )
            }
        } else {
            // Center GlassMedium card with ProgressRing + AnimatedNumber + Ready label + badge
            item {
                GlassMedium(
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(
                        modifier = Modifier.padding(24.dp).fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        ProgressRing(
                            value = readinessScore,
                            ringSize = 160.dp,
                            label = "Readiness",
                        )
                        AnimatedNumber(
                            target = readinessScore,
                            style = MaterialTheme.typography.headlineLarge,
                            suffix = "%",
                            durationMs = 1000,
                        )
                        Text(
                            text = "Ready",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        if (confidenceLevel.isNotBlank()) {
                            CSNexusStatusBadge(
                                text = confidenceLevel.replace('_', ' '),
                                color = confidenceColor,
                            )
                        }
                    }
                }
            }
            // Stats grid (3-col): Passing Probability, Predicted Score, Recommended Hours
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    // Passing Probability
                    GlassMedium(modifier = Modifier.weight(1f)) {
                        Column(
                            modifier = Modifier.padding(12.dp).fillMaxWidth(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            AnimatedNumber(
                                target = ((plannerReadiness?.passingProbability ?: 0.0) * 100).roundToInt(),
                                style = MaterialTheme.typography.titleLarge,
                                suffix = "%",
                                durationMs = 1000,
                            )
                            MetallicText(
                                text = "Passing",
                                style = MaterialTheme.typography.labelSmall,
                            )
                        }
                    }
                    // Predicted Score
                    GlassMedium(modifier = Modifier.weight(1f)) {
                        Column(
                            modifier = Modifier.padding(12.dp).fillMaxWidth(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            AnimatedNumber(
                                target = ((plannerReadiness?.predictedScore ?: 0.0) * 100).roundToInt(),
                                style = MaterialTheme.typography.titleLarge,
                                suffix = "%",
                                durationMs = 1000,
                            )
                            MetallicText(
                                text = "Predicted",
                                style = MaterialTheme.typography.labelSmall,
                            )
                        }
                    }
                    // Recommended Hours
                    GlassMedium(modifier = Modifier.weight(1f)) {
                        Column(
                            modifier = Modifier.padding(12.dp).fillMaxWidth(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(4.dp),
                        ) {
                            AnimatedNumber(
                                target = plannerReadiness?.recommendedHoursRemaining?.roundToInt() ?: 0,
                                style = MaterialTheme.typography.titleLarge,
                                suffix = "h",
                                durationMs = 1000,
                            )
                            MetallicText(
                                text = "Hours Left",
                                style = MaterialTheme.typography.labelSmall,
                            )
                        }
                    }
                }
            }
            dashboard?.let { ready ->
                item {
                    CSNexusCard {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("Component breakdown", style = MaterialTheme.typography.titleMedium)
                            ReadinessComponentRow("Mastery", ready.components.masteryComponent)
                            ReadinessComponentRow("Retention", ready.components.retentionComponent)
                            ReadinessComponentRow("Mock exams", ready.components.mockComponent)
                            ReadinessComponentRow("Coverage", ready.components.coverageComponent)
                        }
                    }
                }
                if (ready.topImpactSubtopics.isNotEmpty()) {
                    item {
                        CSNexusCard {
                            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                                Text("Highest-impact subtopics", style = MaterialTheme.typography.titleMedium)
                                ready.topImpactSubtopics.forEach { item ->
                                    Text("${item.subtopicName}: ${item.pointImpact.roundToInt()} point impact")
                                }
                            }
                        }
                    }
                }
                ready.scoreChangeSummary?.let { summary ->
                    item {
                        CSNexusCard {
                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                Text("Score change summary", style = MaterialTheme.typography.titleMedium)
                                Text("${summary.primaryComponent} moved ${summary.componentDirection} by ${summary.componentMagnitude.roundToInt()} points.")
                                Text("Overall delta ${summary.overallDelta.roundToInt()} points.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }
            // 2-column strengths/weaknesses GlassMedium cards
            if (plannerReadiness != null) {
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        GlassMedium(modifier = Modifier.weight(1f)) {
                            Column(
                                modifier = Modifier.padding(16.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                Text(
                                    "Strengths",
                                    style = MaterialTheme.typography.titleMedium,
                                    color = Color(0xFF4CAF50),
                                    fontWeight = FontWeight.SemiBold,
                                )
                                if (plannerReadiness.strengths.isEmpty()) {
                                    Text("Keep studying to build strengths.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                                } else {
                                    plannerReadiness.strengths.forEach { Text(it) }
                                }
                            }
                        }
                        GlassMedium(modifier = Modifier.weight(1f)) {
                            Column(
                                modifier = Modifier.padding(16.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                Text(
                                    "Needs work",
                                    style = MaterialTheme.typography.titleMedium,
                                    color = Color(0xFFE57373),
                                    fontWeight = FontWeight.SemiBold,
                                )
                                if (plannerReadiness.weaknesses.isEmpty()) {
                                    Text("No weak areas detected yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                                } else {
                                    plannerReadiness.weaknesses.forEach { Text(it) }
                                }
                            }
                        }
                    }
                }
            }
            if (trend.isNotEmpty()) {
                item {
                    CSNexusCard {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("Trend", style = MaterialTheme.typography.titleMedium)
                            Row(
                                modifier = Modifier.horizontalScroll(rememberScrollState()),
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                trend.forEachIndexed { index, point ->
                                    CSNexusChip(
                                        text = "${point.date.takeLast(5)} ${point.score.roundToInt()}",
                                        selected = selectedTrendIndex == index,
                                        onClick = { selectedTrendIndex = index },
                                    )
                                }
                            }
                            val selected = trend[selectedTrendIndex]
                            Text(
                                "${selected.date.takeLast(5)}: ${selected.score.roundToInt()} readiness score.",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }
            item {
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text("Self-assessment", style = MaterialTheme.typography.titleMedium)
                        if (prompt?.isDue == true) {
                            Text("A new self-assessment is due.", color = MaterialTheme.colorScheme.primary)
                        } else if (prompt?.lastAssessedAt != null) {
                            Text("Last assessed ${formatFriendlyDate(prompt.lastAssessedAt)}.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        CSNexusTextField(
                            value = selfAssessmentScore,
                            onValueChange = onSelfAssessmentScoreChange,
                            label = "How ready do you feel? (0-100)",
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        )
                        CSNexusButton(
                            text = if (submittingAssessment) "Submitting..." else "Submit self-assessment",
                            onClick = onSubmitAssessment,
                            loading = submittingAssessment,
                            enabled = selfAssessmentScore.toIntOrNull() in 0..100,
                        )
                        assessmentMessage?.let {
                            Text(it, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
            if (history.isNotEmpty()) {
                item {
                    CSNexusCard {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("Assessment history", style = MaterialTheme.typography.titleMedium)
                            history.take(5).forEach { item ->
                                Text(
                                    "${formatFriendlyDate(item.assessedAt)} - self ${item.selfAssessedScore}% - computed ${(item.computedScore * 100).roundToInt()}%",
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SummaryGrid(items: List<Pair<String, String>>) {
    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        items.chunked(2).forEach { rowItems ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                rowItems.forEach { (label, value) ->
                    val valueColor = when (label.lowercase()) {
                        "avg accuracy" -> MaterialTheme.colorScheme.primary
                        "day streak" -> MaterialTheme.colorScheme.tertiary
                        "readiness" -> MaterialTheme.colorScheme.secondary
                        else -> MaterialTheme.colorScheme.primary
                    }
                    CSNexusStatCard(
                        title = label,
                        value = value,
                        body = "Current snapshot",
                        modifier = Modifier.weight(1f),
                        valueColor = valueColor,
                    )
                }
                if (rowItems.size == 1) {
                    Column(modifier = Modifier.weight(1f)) {}
                }
            }
        }
    }
}

@Composable
private fun BreakdownCard(
    title: String,
    items: List<MasteryDto>,
    emptyBody: String,
) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            if (items.isEmpty()) {
                Text(emptyBody, color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                items.forEach { item ->
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                        ) {
                            Text(item.subtopicTitle, modifier = Modifier.weight(1f))
                            Text(percent(item.masteryScore))
                        }
                        LinearProgressIndicator(
                            progress = { item.masteryScore.toFloat().coerceIn(0f, 1f) },
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun InlineErrorCard(
    message: String,
    onRetry: () -> Unit,
) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Something needs another try", style = MaterialTheme.typography.titleMedium)
            Text(message, color = MaterialTheme.colorScheme.onSurfaceVariant)
            CSNexusButton(
                text = "Retry",
                onClick = onRetry,
                variant = CSNexusButtonVariant.Secondary,
            )
        }
    }
}

@Composable
private fun EmptyCard(
    title: String,
    body: String,
) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(body, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun GoalDayRow(day: GoalDaySummaryDto) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
            Text(formatFriendlyDate(day.goalDate), fontWeight = FontWeight.SemiBold)
            Text("${day.currentXp}/${day.targetXp} XP", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Text(if (day.completed) "Done" else "In progress")
    }
}

/**
 * Weekly calendar grid: 7 columns with green circles for completed days,
 * gray outline for incomplete days, matching the web's goal calendar.
 */
@Composable
private fun WeeklyCalendarGrid(days: List<GoalDaySummaryDto>) {
    val dayLabels = listOf("M", "T", "W", "T", "F", "S", "S")
    val completedColor = Color(0xFF4CAF50) // green for completed
    val incompleteColor = Color(0x40FFFFFF) // subtle outline for incomplete
    val circleSize = 36.dp

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Day of week header row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly,
        ) {
            dayLabels.forEach { label ->
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.size(circleSize),
                    textAlign = TextAlign.Center,
                )
            }
        }
        // Day circles row
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly,
        ) {
            days.take(7).forEachIndexed { index, day ->
                Canvas(
                    modifier = Modifier
                        .size(circleSize)
                        .semantics {
                            contentDescription = "${dayLabels.getOrElse(index) { "" }}: ${if (day.completed) "completed" else "in progress"}"
                        },
                ) {
                    val radius = size.minDimension / 2f - 2.dp.toPx()
                    if (day.completed) {
                        drawCircle(
                            color = completedColor,
                            radius = radius,
                        )
                    } else {
                        drawCircle(
                            color = incompleteColor,
                            radius = radius,
                            style = Stroke(width = 2.dp.toPx()),
                        )
                    }
                }
            }
            // Fill remaining slots if fewer than 7 days
            repeat((7 - days.take(7).size).coerceAtLeast(0)) {
                Canvas(
                    modifier = Modifier.size(circleSize),
                ) {
                    val radius = size.minDimension / 2f - 2.dp.toPx()
                    drawCircle(
                        color = incompleteColor,
                        radius = radius,
                        style = Stroke(width = 2.dp.toPx()),
                    )
                }
            }
        }
    }
}

@Composable
private fun ReadinessComponentRow(label: String, score: Double) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Text(label)
            Text("${score.roundToInt()}%")
        }
        LinearProgressIndicator(progress = { (score / 100.0).toFloat().coerceIn(0f, 1f) }, modifier = Modifier.fillMaxWidth())
    }
}

private fun applyGoalBundle(
    bundle: GoalBundle,
    setGoal: (DailyGoalDto) -> Unit,
    setWeekly: (WeeklyGoalDto) -> Unit,
    setFreezes: (FreezeCountDto) -> Unit,
) {
    setGoal(bundle.goal)
    setWeekly(bundle.weekly)
    setFreezes(bundle.freezes)
}

private fun percent(value: Double): String = "${(value * 100).roundToInt()}%"

private fun reasonLabel(reason: String): String {
    return when (reason.lowercase()) {
        "weak_area" -> "Needs practice"
        "due_for_review" -> "Due for review"
        "next_in_sequence" -> "Next up"
        "challenge" -> "Challenge"
        else -> reason.replace('_', ' ').ifBlank { "Recommended" }
    }
}

private fun formatFriendlyDate(raw: String): String {
    return try {
        OffsetDateTime.parse(raw).toLocalDate().toString()
    } catch (_: DateTimeParseException) {
        runCatching { LocalDate.parse(raw.take(10)).toString() }.getOrElse { raw.take(10) }
    }
}

private val masteryOrderLabels = listOf("BEGINNER", "FAMILIAR", "PROFICIENT", "ADVANCED", "MASTERED")

private fun masteryLevelColor(level: String): Color = when (level.uppercase()) {
    "BEGINNER" -> Color(0xFF9CA3AF) // gray
    "FAMILIAR" -> Color(0xFF60A5FA) // blue/info
    "PROFICIENT" -> Color(0xFFC9A84C) // gold/accent
    "ADVANCED" -> Color(0xFF4ADE80) // green/success
    "MASTERED" -> Color(0xFFA78BFA) // purple
    else -> Color(0xFF9CA3AF)
}

// -- Analytics premium composables --

private val GoldAccent = Color(0xFFC9A84C)
private val GoldMetallic = Color(0xFFE8C96A)
private val StrengthGreen = Color(0xFF4ADE80)
private val StrengthGreenEnd = Color(0xFF22C55E)
private val WeaknessRed = Color(0xFFEF4444)
private val WeaknessRedEnd = Color(0xFFF87171)

/**
 * 4-stat card grid: 2×2 layout, each card is GlassMedium with icon + title + AnimatedNumber + trend.
 */
@Composable
private fun AnalyticsStatGrid(model: AnalyticsModel) {
    data class StatItem(
        val icon: String,
        val title: String,
        val value: Int,
        val suffix: String,
        val trendPositive: Boolean?,
    )

    val stats = listOf(
        StatItem("📚", "Study Sessions", model.totalSessions, "", null),
        StatItem("🎯", "Avg Accuracy", model.averageAccuracy, "%", model.averageAccuracy >= 70),
        StatItem("🔥", "Day Streak", model.streak, "", model.streak > 0),
        StatItem("⚡", "Readiness", model.readinessPercent, "%", model.readinessPercent >= 60),
    )

    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        stats.chunked(2).forEach { rowItems ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                rowItems.forEach { stat ->
                    GlassMedium(modifier = Modifier.weight(1f)) {
                        Column(
                            modifier = Modifier.padding(14.dp),
                            verticalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(6.dp),
                            ) {
                                Text(stat.icon, style = MaterialTheme.typography.titleMedium)
                                Text(
                                    stat.title,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                )
                            }
                            AnimatedNumber(
                                target = stat.value,
                                style = MaterialTheme.typography.headlineSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = GoldMetallic,
                                ),
                                suffix = stat.suffix,
                            )
                            // Trend indicator
                            when (stat.trendPositive) {
                                true -> Text(
                                    "▲",
                                    color = StrengthGreen,
                                    style = MaterialTheme.typography.bodySmall,
                                )
                                false -> Text(
                                    "▼",
                                    color = WeaknessRed,
                                    style = MaterialTheme.typography.bodySmall,
                                )
                                null -> Spacer(modifier = Modifier.height(16.dp))
                            }
                        }
                    }
                }
                if (rowItems.size == 1) {
                    Spacer(modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

/**
 * Canvas-based donut chart for mastery distribution with gold accent.
 */
@Composable
private fun AnalyticsDonutChart(distribution: List<MasteryLevelCountUi>) {
    val total = distribution.sumOf { it.count }.coerceAtLeast(1)
    val colors = distribution.map { masteryLevelColor(it.level) }

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Canvas(
            modifier = Modifier
                .size(120.dp)
                .semantics {
                    contentDescription = distribution.joinToString(", ") {
                        "${it.level} ${it.count}"
                    }
                },
        ) {
            val strokeWidth = 20.dp.toPx()
            val radius = (size.minDimension - strokeWidth) / 2f
            val center = Offset(size.width / 2f, size.height / 2f)
            var startAngle = -90f

            distribution.forEachIndexed { index, bucket ->
                val sweepAngle = (bucket.count.toFloat() / total) * 360f
                drawArc(
                    color = colors[index],
                    startAngle = startAngle,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = Offset(center.x - radius, center.y - radius),
                    size = Size(radius * 2, radius * 2),
                    style = Stroke(width = strokeWidth, cap = StrokeCap.Round),
                )
                startAngle += sweepAngle
            }

            // Gold center dot accent
            drawCircle(
                color = GoldAccent,
                radius = 4.dp.toPx(),
                center = center,
            )
        }
        // Legend
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            distribution.forEachIndexed { index, bucket ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                ) {
                    Canvas(modifier = Modifier.size(10.dp)) {
                        drawCircle(color = colors[index])
                    }
                    Text(
                        "${bucket.level.replaceFirstChar { it.titlecase() }}: ${bucket.count}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

/**
 * Canvas-based line chart for accuracy trend with gold gradient line.
 */
@Composable
private fun AnalyticsLineChart(points: List<AnalyticsTrendPointUi>) {
    if (points.size < 2) return

    Canvas(
        modifier = Modifier
            .fillMaxWidth()
            .height(100.dp)
            .semantics {
                contentDescription = "Accuracy trend chart with ${points.size} data points"
            },
    ) {
        val maxVal = points.maxOf { it.accuracyPercent }.coerceAtLeast(1).toFloat()
        val stepX = size.width / (points.size - 1).coerceAtLeast(1)
        val goldBrush = Brush.horizontalGradient(listOf(GoldAccent, GoldMetallic))

        // Draw connecting lines
        for (i in 0 until points.size - 1) {
            val x1 = i * stepX
            val y1 = size.height - (points[i].accuracyPercent / maxVal) * size.height * 0.85f
            val x2 = (i + 1) * stepX
            val y2 = size.height - (points[i + 1].accuracyPercent / maxVal) * size.height * 0.85f
            drawLine(
                brush = goldBrush,
                start = Offset(x1, y1),
                end = Offset(x2, y2),
                strokeWidth = 2.dp.toPx(),
                cap = StrokeCap.Round,
            )
        }

        // Draw dots at each point
        points.forEachIndexed { index, point ->
            val x = index * stepX
            val y = size.height - (point.accuracyPercent / maxVal) * size.height * 0.85f
            drawCircle(
                color = GoldMetallic,
                radius = 4.dp.toPx(),
                center = Offset(x, y),
            )
        }
    }
}

/**
 * Canvas-based heatmap showing study consistency with gold accent cells.
 */
@Composable
private fun AnalyticsHeatmapChart(entries: List<AnalyticsHeatmapEntryUi>) {
    if (entries.isEmpty()) return
    val maxCount = entries.maxOf { it.count }.coerceAtLeast(1)

    Canvas(
        modifier = Modifier
            .fillMaxWidth()
            .height(40.dp)
            .semantics {
                contentDescription = "Study consistency heatmap with ${entries.size} days"
            },
    ) {
        val cellWidth = size.width / entries.size.coerceAtLeast(1)
        val cellHeight = size.height
        val cornerPx = 3.dp.toPx()

        entries.forEachIndexed { index, entry ->
            val intensity = (entry.count.toFloat() / maxCount).coerceIn(0.1f, 1f)
            val cellColor = GoldAccent.copy(alpha = intensity)
            drawRoundRect(
                color = cellColor,
                topLeft = Offset(index * cellWidth + 1.dp.toPx(), 0f),
                size = Size(cellWidth - 2.dp.toPx(), cellHeight),
                cornerRadius = CornerRadius(cornerPx, cornerPx),
            )
        }
    }
}

/**
 * 2-column strengths/weaknesses layout with colored LuxuryProgressBars.
 * Green for strengths, red for weaknesses.
 */
@Composable
private fun AnalyticsStrengthsWeaknesses(
    strongest: List<MasteryDto>,
    weakest: List<MasteryDto>,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        // Strengths column
        GlassMedium(modifier = Modifier.weight(1f)) {
            Column(
                modifier = Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                Text(
                    "Strengths",
                    style = MaterialTheme.typography.titleMedium,
                    color = StrengthGreen,
                )
                if (strongest.isEmpty()) {
                    Text(
                        "No strengths yet.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        style = MaterialTheme.typography.bodySmall,
                    )
                } else {
                    strongest.forEach { item ->
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text(
                                item.subtopicTitle,
                                style = MaterialTheme.typography.bodySmall,
                                maxLines = 1,
                            )
                            LuxuryProgressBar(
                                progress = item.masteryScore.toFloat().coerceIn(0f, 1f),
                                modifier = Modifier.fillMaxWidth(),
                                barColorStart = StrengthGreen,
                                barColorEnd = StrengthGreenEnd,
                                glowColor = StrengthGreen.copy(alpha = 0.4f),
                            )
                        }
                    }
                }
            }
        }
        // Weaknesses column
        GlassMedium(modifier = Modifier.weight(1f)) {
            Column(
                modifier = Modifier.padding(14.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                Text(
                    "Needs work",
                    style = MaterialTheme.typography.titleMedium,
                    color = WeaknessRed,
                )
                if (weakest.isEmpty()) {
                    Text(
                        "No weak areas yet.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        style = MaterialTheme.typography.bodySmall,
                    )
                } else {
                    weakest.forEach { item ->
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text(
                                item.subtopicTitle,
                                style = MaterialTheme.typography.bodySmall,
                                maxLines = 1,
                            )
                            LuxuryProgressBar(
                                progress = item.masteryScore.toFloat().coerceIn(0f, 1f),
                                modifier = Modifier.fillMaxWidth(),
                                barColorStart = WeaknessRed,
                                barColorEnd = WeaknessRedEnd,
                                glowColor = WeaknessRed.copy(alpha = 0.4f),
                            )
                        }
                    }
                }
            }
        }
    }
}
