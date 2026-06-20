package com.csnexus.app.feature.content.ui

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusOfflineBanner
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.EmptyState
import com.csnexus.app.core.design.ErrorState
import com.csnexus.app.core.design.LessonSkeleton
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.ModuleListSkeleton
import com.csnexus.app.core.design.TopicListSkeleton
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.design.csnexusHeading
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.content.domain.InlineCheck
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.Lesson
import com.csnexus.app.feature.content.domain.LessonSegment
import com.csnexus.app.feature.tutor.data.LessonChatHistoryItemDto
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ModuleListScreen(
    repository: ContentRepository,
    contentPadding: PaddingValues,
    onModuleSelected: (Int) -> Unit,
    onMasterySelected: (() -> Unit)? = null,
    viewModel: ContentViewModel = viewModel(factory = ContentViewModelFactory(repository)),
) {
    val state by viewModel.uiState.collectAsState()

    when {
        state.isLoading -> ModuleListSkeleton(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding),
        )
        state.errorMessage != null -> ErrorState(
            message = state.errorMessage.orEmpty(),
            onRetry = viewModel::loadModules,
        )
        state.modules.isEmpty() -> EmptyState(
            title = "No modules yet",
            body = "Published lessons will appear here.",
        )
        else -> LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding),
            contentPadding = PaddingValues(16.dp),
        ) {
            item {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    MetallicText("Modules")
                    if (onMasterySelected != null) {
                        CSNexusButton(
                            text = "Mastery",
                            onClick = onMasterySelected,
                            variant = CSNexusButtonVariant.Secondary,
                        )
                    }
                }
            }
            if (state.fromCache) {
                item {
                    CSNexusOfflineBanner(
                        modifier = Modifier.padding(bottom = 12.dp),
                        message = "Offline. Showing saved modules.",
                    )
                }
            }
            // 2-column grid using chunked rows
            val chunkedModules = state.modules.chunked(2)
            items(chunkedModules.size, key = { chunkedModules[it].first().id }) { rowIndex ->
                val row = chunkedModules[rowIndex]
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 12.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    row.forEachIndexed { colIndex, module ->
                        val itemIndex = rowIndex * 2 + colIndex
                        StaggeredItem(index = itemIndex, modifier = Modifier.weight(1f)) {
                            ModuleCard(module = module, onClick = { onModuleSelected(module.id) })
                        }
                    }
                    // Fill remaining space if odd number of modules
                    if (row.size < 2) {
                        Spacer(modifier = Modifier.weight(1f))
                    }
                }
            }
        }
    }
}

@Composable
private fun ModuleCard(module: LearningModule, onClick: () -> Unit) {
    PremiumCard(
        modifier = Modifier.fillMaxWidth(),
        onClick = if (module.isPublished) onClick else null,
    ) {
        Row(Modifier.fillMaxWidth()) {
            // Gold left-border gradient (3dp wide)
            Canvas(
                modifier = Modifier
                    .width(3.dp)
                    .fillMaxHeight(),
            ) {
                drawRect(
                    brush = Brush.verticalGradient(
                        colors = listOf(
                            Color(0xFFC9A84C),
                            Color(0xFFE8C96A),
                        ),
                    ),
                )
            }
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Text(text = module.title, style = MaterialTheme.typography.titleMedium)
                CSNexusStatusBadge(text = module.category)
                if (!module.isPublished) {
                    CSNexusStatusBadge(text = "Unavailable")
                }
                LuxuryProgressBar(progress = 0.5f)
            }
        }
    }
}

@Composable
fun TopicListScreen(
    repository: ContentRepository,
    moduleId: Int,
    contentPadding: PaddingValues,
    onTopicSelected: (Int) -> Unit,
    onModuleQuizSelected: ((Int) -> Unit)? = null,
    viewModel: TopicListViewModel = viewModel(
        factory = TopicListViewModelFactory(repository, moduleId),
    ),
) {
    val state by viewModel.uiState.collectAsState()
    when {
        state.isLoading -> TopicListSkeleton(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding),
        )
        state.errorMessage != null -> ErrorState(state.errorMessage.orEmpty(), viewModel::loadTopics)
        state.topics.isEmpty() -> EmptyState("No topics yet", "Published topics will appear here.")
        else -> LazyColumn(
            modifier = Modifier.fillMaxSize().padding(contentPadding),
            contentPadding = PaddingValues(16.dp),
        ) {
            item {
                MetallicText(
                    text = "Topics",
                    modifier = Modifier.padding(bottom = 16.dp),
                )
            }
            if (onModuleQuizSelected != null) {
                item {
                    CSNexusButton(
                        text = "Start module quiz",
                        onClick = { onModuleQuizSelected(moduleId) },
                        modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp),
                        variant = CSNexusButtonVariant.Secondary,
                    )
                }
            }
            if (state.fromCache) {
                item {
                    CSNexusOfflineBanner(
                        modifier = Modifier.padding(bottom = 12.dp),
                        message = "Offline. Showing saved topics.",
                    )
                }
            }
            itemsIndexed(state.topics, key = { _, topic -> topic.id }) { index, topic ->
                StaggeredItem(index = index) {
                    TopicCard(topic = topic, onClick = { onTopicSelected(topic.id) })
                }
            }
        }
    }
}

@Composable
private fun TopicCard(topic: LearningTopic, onClick: () -> Unit) {
    PremiumCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 12.dp),
        onClick = if (topic.isPublished) onClick else null,
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(topic.title, style = MaterialTheme.typography.titleMedium)
            Text(
                text = if (topic.isPublished) "Tap to explore" else "Coming soon",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (!topic.isPublished) {
                CSNexusStatusBadge(text = "Unavailable", modifier = Modifier.padding(top = 8.dp))
            }
        }
    }
}

@Composable
fun SubtopicListScreen(
    repository: ContentRepository,
    topicId: Int,
    contentPadding: PaddingValues,
    onSubtopicSelected: (Int) -> Unit,
    onTopicQuizSelected: ((Int) -> Unit)? = null,
    onSubtopicQuizSelected: ((Int) -> Unit)? = null,
    viewModel: SubtopicListViewModel = viewModel(
        factory = SubtopicListViewModelFactory(repository, topicId),
    ),
) {
    val state by viewModel.uiState.collectAsState()
    when {
        state.isLoading -> TopicListSkeleton(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding),
        )
        state.errorMessage != null -> ErrorState(state.errorMessage.orEmpty(), viewModel::loadSubtopics)
        state.subtopics.isEmpty() -> EmptyState("No subtopics yet", "Published lessons will appear here.")
        else -> LazyColumn(
            modifier = Modifier.fillMaxSize().padding(contentPadding),
            contentPadding = PaddingValues(16.dp),
        ) {
            item {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    MetallicText("Subtopics")
                    if (onTopicQuizSelected != null) {
                        CSNexusButton(
                            text = "Topic Quiz",
                            onClick = { onTopicQuizSelected(topicId) },
                        )
                    }
                }
            }
            if (state.fromCache) {
                item {
                    CSNexusOfflineBanner(
                        modifier = Modifier.padding(bottom = 12.dp),
                        message = "Offline. Showing saved subtopics.",
                    )
                }
            }
            itemsIndexed(state.subtopics, key = { _, subtopic -> subtopic.id }) { index, subtopic ->
                StaggeredItem(index = index) {
                    SubtopicCard(
                        subtopic = subtopic,
                        onLessonClick = { onSubtopicSelected(subtopic.id) },
                        onQuizClick = onSubtopicQuizSelected?.let { callback -> { callback(subtopic.id) } },
                    )
                }
            }
        }
    }
}

@Composable
private fun SubtopicCard(
    subtopic: LearningSubtopic,
    onLessonClick: () -> Unit,
    onQuizClick: (() -> Unit)?,
) {
    PremiumCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 12.dp),
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(subtopic.title, style = MaterialTheme.typography.titleMedium)
            if (!subtopic.isPublished) {
                CSNexusStatusBadge(text = "Unavailable", modifier = Modifier.padding(top = 8.dp))
            }
            Row(
                modifier = Modifier.padding(top = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                CSNexusButton(
                    text = "Lesson",
                    onClick = onLessonClick,
                    modifier = Modifier.weight(1f),
                    enabled = subtopic.isPublished,
                    variant = CSNexusButtonVariant.Secondary,
                )
                if (onQuizClick != null) {
                    CSNexusButton(
                        text = "Quiz",
                        onClick = onQuizClick,
                        modifier = Modifier.weight(1f),
                        enabled = subtopic.isPublished,
                    )
                }
            }
        }
    }
}

@Composable
fun LessonReaderScreen(
    repository: ContentRepository,
    tutorRepository: TutorRepositoryContract? = null,
    subtopicId: Int,
    contentPadding: PaddingValues,
    viewModel: LessonViewModel = viewModel(
        factory = LessonViewModelFactory(repository, subtopicId),
    ),
) {
    val state by viewModel.uiState.collectAsState()
    when {
        state.isLoading -> LessonSkeleton(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding),
        )
        state.errorMessage != null -> ErrorState(state.errorMessage.orEmpty(), viewModel::loadLesson)
        state.lesson == null -> EmptyState("Lesson unavailable", "Try again when you are online.")
        else -> LessonContent(
            lesson = state.lesson,
            contentPadding = contentPadding,
            fromCache = state.fromCache,
            completed = state.completed,
            isCompleting = state.isCompleting,
            completionMessage = state.completionMessage,
            onComplete = viewModel::completeLesson,
            tutorRepository = tutorRepository,
        )
    }
}

@Composable
private fun LessonContent(
    lesson: Lesson?,
    contentPadding: PaddingValues,
    fromCache: Boolean,
    completed: Boolean,
    isCompleting: Boolean,
    completionMessage: String?,
    onComplete: () -> Unit,
    tutorRepository: TutorRepositoryContract?,
) {
    if (lesson == null) return
    if (lesson.isSegmented && lesson.segments.isNotEmpty()) {
        SegmentedLessonContent(
            lesson = lesson,
            contentPadding = contentPadding,
            fromCache = fromCache,
            completed = completed,
            isCompleting = isCompleting,
            completionMessage = completionMessage,
            onComplete = onComplete,
            tutorRepository = tutorRepository,
        )
        return
    }

    // Track scroll progress for the reading progress bar
    val listState = rememberLazyListState()
    val readingProgress by remember {
        derivedStateOf {
            val layoutInfo = listState.layoutInfo
            val totalItems = layoutInfo.totalItemsCount
            if (totalItems == 0) return@derivedStateOf 0f
            val lastVisibleIndex = layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: 0
            ((lastVisibleIndex + 1).toFloat() / totalItems.toFloat()).coerceIn(0f, 1f)
        }
    }

    // XP gain animation state
    var showXpGain by remember { mutableStateOf(false) }
    LaunchedEffect(completed) {
        if (completed) {
            showXpGain = true
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            // Fixed 3dp gold-gradient reading progress bar at top
            ReadingProgressBar(progress = readingProgress)

            // Content with max-width constraint
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                contentAlignment = Alignment.TopCenter,
            ) {
                LazyColumn(
                    state = listState,
                    modifier = Modifier
                        .widthIn(max = 680.dp)
                        .fillMaxSize(),
                    contentPadding = PaddingValues(20.dp),
                ) {
                    if (fromCache) {
                        item {
                            CSNexusOfflineBanner(
                                modifier = Modifier.padding(bottom = 12.dp),
                                message = "Offline. Showing saved lesson.",
                            )
                        }
                    }
                    item {
                        Text(
                            text = lesson.title,
                            modifier = Modifier.csnexusHeading(),
                            style = MaterialTheme.typography.headlineMedium,
                        )
                    }
                    if (lesson.summary.isNotBlank()) {
                        item {
                            Text(
                                text = lesson.summary,
                                modifier = Modifier.padding(top = 16.dp),
                                style = MaterialTheme.typography.bodyLarge.copy(
                                    lineHeight = (MaterialTheme.typography.bodyLarge.fontSize.value * 1.75f).sp,
                                ),
                            )
                        }
                    }
                    items(
                        items = lesson.explanations,
                        key = { explanation -> "explanation:${explanation.heading}:${explanation.body.hashCode()}" },
                        contentType = { "lesson_explanation" },
                    ) { explanation ->
                        Text(
                            text = explanation.heading,
                            modifier = Modifier.padding(top = 24.dp),
                            style = MaterialTheme.typography.titleLarge,
                        )
                        Text(
                            text = explanation.body,
                            modifier = Modifier.padding(top = 8.dp),
                            style = MaterialTheme.typography.bodyLarge.copy(
                                lineHeight = (MaterialTheme.typography.bodyLarge.fontSize.value * 1.75f).sp,
                            ),
                        )
                    }
                    items(
                        items = lesson.workedExamples,
                        key = { example -> "example:${example.title}:${example.body.hashCode()}" },
                        contentType = { "lesson_example" },
                    ) { example ->
                        Text(
                            text = example.title,
                            modifier = Modifier.padding(top = 24.dp),
                            style = MaterialTheme.typography.titleLarge,
                        )
                        Text(
                            text = example.body,
                            modifier = Modifier.padding(top = 8.dp),
                            style = MaterialTheme.typography.bodyLarge.copy(
                                lineHeight = (MaterialTheme.typography.bodyLarge.fontSize.value * 1.75f).sp,
                            ),
                        )
                    }
                    items(
                        items = lesson.sections,
                        key = { section -> "section:${section.title}:${section.blocks.size}" },
                        contentType = { "lesson_section" },
                    ) { section ->
                        Text(
                            text = section.title,
                            modifier = Modifier.padding(top = 24.dp),
                            style = MaterialTheme.typography.titleLarge,
                        )
                        section.blocks.forEach { block ->
                            LessonBlockRenderer(
                                block = block,
                                modifier = Modifier.padding(top = 8.dp),
                            )
                        }
                    }
                    if (lesson.keyTakeaways.isNotEmpty()) {
                        item {
                            Text(
                                text = "Key takeaways",
                                modifier = Modifier.padding(top = 24.dp),
                                style = MaterialTheme.typography.titleLarge,
                            )
                        }
                        items(
                            items = lesson.keyTakeaways,
                            key = { takeaway -> "takeaway:$takeaway" },
                            contentType = { "lesson_takeaway" },
                        ) { takeaway ->
                            Text(
                                text = "- $takeaway",
                                modifier = Modifier.padding(top = 8.dp),
                                style = MaterialTheme.typography.bodyLarge,
                            )
                        }
                    }
                    item {
                        LessonCompanionPanel(
                            lesson = lesson,
                            activeSectionIndex = 0,
                            tutorRepository = tutorRepository,
                            modifier = Modifier.padding(top = 24.dp),
                        )
                    }
                    // Gold gradient overlay fade before completion button
                    item {
                        Box(modifier = Modifier.fillMaxWidth()) {
                            Canvas(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(48.dp),
                            ) {
                                drawRect(
                                    brush = Brush.verticalGradient(
                                        colors = listOf(
                                            Color.Transparent,
                                            Color(0x33C9A84C), // gold at ~20% alpha
                                        ),
                                    ),
                                )
                            }
                        }
                    }
                    item {
                        LessonCompletionFooter(
                            fromCache = fromCache,
                            completed = completed,
                            isCompleting = isCompleting,
                            completionMessage = completionMessage,
                            onComplete = onComplete,
                            modifier = Modifier.padding(top = 8.dp),
                        )
                    }
                }
            }
        }

        // XP gain animation overlay
        XpGainOverlay(
            visible = showXpGain,
            onDismiss = { showXpGain = false },
        )
    }
}

@Composable
private fun SegmentedLessonContent(
    lesson: Lesson,
    contentPadding: PaddingValues,
    fromCache: Boolean,
    completed: Boolean,
    isCompleting: Boolean,
    completionMessage: String?,
    onComplete: () -> Unit,
    tutorRepository: TutorRepositoryContract?,
) {
    var selectedSegment by remember(lesson.id) { mutableIntStateOf(0) }
    val segment = lesson.segments[selectedSegment.coerceIn(0, lesson.segments.lastIndex)]
    var checksVisible by remember(lesson.id, selectedSegment) { mutableStateOf(false) }
    var revealedChecks by remember(lesson.id, selectedSegment) { mutableStateOf(emptySet<Int>()) }
    val isLastSegment = selectedSegment == lesson.segments.lastIndex
    val canAdvance = segment.checks.isEmpty() || revealedChecks.isNotEmpty()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        if (fromCache) {
            CSNexusOfflineBanner(message = "Offline. Showing saved lesson.")
        }
        Text(lesson.title, style = MaterialTheme.typography.headlineMedium)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            CSNexusStatusBadge(text = "Part ${selectedSegment + 1}/${lesson.segments.size}")
            if (segment.estimatedMinutes > 0) {
                CSNexusStatusBadge(text = "${segment.estimatedMinutes} min")
            }
        }
        LinearProgressIndicator(
            progress = { (selectedSegment + 1).toFloat() / lesson.segments.size.toFloat() },
            modifier = Modifier.fillMaxWidth(),
        )
        if (lesson.summary.isNotBlank() && selectedSegment == 0) {
            Text(lesson.summary, style = MaterialTheme.typography.bodyLarge)
        }

        SegmentBody(segment)

        if (segment.checks.isNotEmpty()) {
            CSNexusButton(
                text = if (checksVisible) "Understanding check open" else "Check understanding",
                onClick = { checksVisible = true },
                enabled = !checksVisible,
                variant = if (checksVisible) CSNexusButtonVariant.Secondary else CSNexusButtonVariant.Primary,
            )
        }

        if (checksVisible) {
            SegmentChecks(
                checks = segment.checks,
                revealedChecks = revealedChecks,
                onReveal = { index -> revealedChecks = revealedChecks + index },
            )
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            if (selectedSegment > 0) {
                CSNexusButton(
                    text = "Previous",
                    onClick = {
                        selectedSegment -= 1
                    },
                    modifier = Modifier.weight(1f),
                    variant = CSNexusButtonVariant.Secondary,
                )
            }
            CSNexusButton(
                text = if (isLastSegment) "Complete lesson" else "Continue",
                onClick = {
                    if (isLastSegment) {
                        onComplete()
                    } else {
                        selectedSegment += 1
                    }
                },
                modifier = Modifier.weight(1f),
                enabled = canAdvance && !fromCache && !completed,
                loading = isLastSegment && isCompleting,
            )
        }

        if (fromCache) {
            Text(
                text = "Reconnect to complete this lesson and update progress.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        if (completionMessage != null) {
            Text(
                text = completionMessage,
                color = if (completed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodyMedium,
            )
        }

        if (isLastSegment) {
            LessonReviewAids(lesson)
        }
        LessonCompanionPanel(
            lesson = lesson,
            activeSectionIndex = selectedSegment,
            tutorRepository = tutorRepository,
        )
    }
}

@Composable
private fun SegmentBody(segment: LessonSegment) {
    segment.sections.forEach { section ->
        Text(
            text = section.title,
            modifier = Modifier.padding(top = 8.dp),
            style = MaterialTheme.typography.titleLarge,
        )
        section.blocks.forEach { block ->
            LessonBlockRenderer(
                block = block,
                modifier = Modifier.padding(top = 8.dp),
            )
        }
    }
}

@Composable
private fun SegmentChecks(
    checks: List<InlineCheck>,
    revealedChecks: Set<Int>,
    onReveal: (Int) -> Unit,
) {
    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        checks.forEachIndexed { index, check ->
            CSNexusCard {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = check.question,
                        style = MaterialTheme.typography.titleMedium,
                    )
                    if (index in revealedChecks) {
                        Text(check.answer, style = MaterialTheme.typography.bodyLarge)
                        if (check.rationale.isNotBlank()) {
                            Text(
                                text = check.rationale,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.bodyMedium,
                            )
                        }
                    } else {
                        CSNexusButton(
                            text = "Reveal answer",
                            onClick = { onReveal(index) },
                            variant = CSNexusButtonVariant.Secondary,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun LessonReviewAids(lesson: Lesson) {
    if (lesson.keyTakeaways.isEmpty() && lesson.memoryAids.isEmpty() && lesson.examStrategies.isEmpty()) return

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("Review", style = MaterialTheme.typography.titleLarge)
        lesson.keyTakeaways.forEach { takeaway ->
            Text("- $takeaway", style = MaterialTheme.typography.bodyLarge)
        }
        lesson.memoryAids.forEach { aid ->
            Text("- $aid", style = MaterialTheme.typography.bodyLarge)
        }
        lesson.examStrategies.forEach { strategy ->
            Text("- $strategy", style = MaterialTheme.typography.bodyLarge)
        }
    }
}

@Composable
private fun LessonCompletionFooter(
    fromCache: Boolean,
    completed: Boolean,
    isCompleting: Boolean,
    completionMessage: String?,
    onComplete: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(8.dp)) {
        CSNexusButton(
            text = if (completed) "Completed" else "Complete lesson",
            onClick = onComplete,
            enabled = !fromCache && !completed,
            loading = isCompleting,
            modifier = Modifier.fillMaxWidth(),
        )
        if (fromCache) {
            Text(
                text = "Reconnect to complete this lesson and update progress.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.bodyMedium,
            )
        }
        if (completionMessage != null) {
            Text(
                text = completionMessage,
                color = if (completed) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodyMedium,
            )
        }
    }
}

@Composable
private fun LessonCompanionPanel(
    lesson: Lesson,
    activeSectionIndex: Int,
    tutorRepository: TutorRepositoryContract?,
    modifier: Modifier = Modifier,
) {
    val tabs = listOf("Practice", "Aids", "Tutor")
    var selectedTab by remember(lesson.id) { mutableIntStateOf(0) }

    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(12.dp)) {
        HorizontalDivider()
        Text("Companion", style = MaterialTheme.typography.titleLarge)
        CSNexusSegmentedControl(
            options = tabs,
            selectedIndex = selectedTab,
            onSelected = { selectedTab = it },
        )
        when (selectedTab) {
            0 -> PracticePanel(lesson)
            1 -> StudyAidsPanel(lesson)
            2 -> TutorPanel(lesson, activeSectionIndex, tutorRepository)
        }
    }
}

@Composable
private fun PracticePanel(lesson: Lesson) {
    var revealedProblems by remember(lesson.id) { mutableStateOf(emptySet<Int>()) }

    if (lesson.practiceProblems.isEmpty()) {
        Text("No practice problems are attached to this lesson yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        return
    }

    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        lesson.practiceProblems.forEachIndexed { index, problem ->
            CSNexusCard {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(
                            text = "Problem ${problem.number.takeIf { it > 0 } ?: index + 1}",
                            style = MaterialTheme.typography.titleMedium,
                        )
                        if (problem.difficulty.isNotBlank()) {
                            CSNexusStatusBadge(text = problem.difficulty)
                        }
                    }
                    Text(problem.question, style = MaterialTheme.typography.bodyLarge)
                    if (index in revealedProblems) {
                        Text(problem.answer, style = MaterialTheme.typography.bodyLarge)
                        if (problem.explanation.isNotBlank()) {
                            Text(
                                problem.explanation,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.bodyMedium,
                            )
                        }
                    } else {
                        CSNexusButton(
                            text = "Show solution",
                            onClick = { revealedProblems = revealedProblems + index },
                            variant = CSNexusButtonVariant.Secondary,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun StudyAidsPanel(lesson: Lesson) {
    val hasAids = lesson.memoryAids.isNotEmpty() || lesson.examStrategies.isNotEmpty() || lesson.keyTakeaways.isNotEmpty()
    if (!hasAids) {
        Text("Study aids will appear here when the lesson provides them.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        return
    }

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        lesson.keyTakeaways.forEach { Text("- $it", style = MaterialTheme.typography.bodyLarge) }
        lesson.memoryAids.forEach { Text("- $it", style = MaterialTheme.typography.bodyLarge) }
        lesson.examStrategies.forEach { Text("- $it", style = MaterialTheme.typography.bodyLarge) }
    }
}

/**
 * Lesson-aware tutor panel embedded in the lesson companion tabs (task 11.2).
 *
 * Uses [TutorRepository.lessonChat] so the backend receives the lesson context
 * alongside every message, matching the web app's `/v1/tutor/lesson-chat` behavior.
 *
 * Offline draft preservation: if [tutorRepository] is null (offline or build gate),
 * the unsent message is preserved in state so the user does not lose their question.
 */
@Composable
private fun TutorPanel(
    lesson: Lesson,
    activeSectionIndex: Int,
    tutorRepository: TutorRepositoryContract?,
) {
    val scope = rememberCoroutineScope()
    var message by remember(lesson.id) { mutableStateOf("") }
    var messages by remember(lesson.id) { mutableStateOf(emptyList<LessonTutorMessage>()) }
    var loading by remember(lesson.id) { mutableStateOf(false) }
    var lastInteractionId by remember(lesson.id) { mutableStateOf<Int?>(null) }
    var draftNotice by remember(lesson.id) { mutableStateOf<String?>(null) }

    LaunchedEffect(lesson.id) {
        message = ""
        messages = emptyList()
        loading = false
        lastInteractionId = null
        draftNotice = null
    }

    fun sendMessage(rawMessage: String) {
        val currentMessage = rawMessage.trim()
        if (currentMessage.isBlank() || loading) return
        if (tutorRepository == null) {
            draftNotice = "Tutor is not available offline. Your question has been saved in the field."
            return
        }
        val nextMessages = messages + LessonTutorMessage(
            role = LessonTutorRole.User,
            content = currentMessage,
        )
        val history = nextMessages
            .dropLast(1)
            .takeLast(10)
            .map { LessonChatHistoryItemDto(role = it.role.wireValue, content = it.content) }
        val context = "Lesson: ${lesson.title}; subtopicId: ${lesson.subtopicId}"
        messages = nextMessages
        message = ""
        draftNotice = null
        loading = true
        lastInteractionId = null
        scope.launch {
            when (
                val result = tutorRepository.lessonChat(
                    message = currentMessage,
                    context = context,
                    subtopicId = lesson.subtopicId,
                    activeSectionIndex = activeSectionIndex,
                    history = history,
                )
            ) {
                is ApiResult.Success -> {
                    val assistantText = result.value.resolvedText()
                        .ifBlank { "Sorry, I couldn't process that. Try again in a moment!" }
                    messages = nextMessages + LessonTutorMessage(
                        role = LessonTutorRole.Assistant,
                        content = assistantText,
                    )
                    lastInteractionId = result.value.interactionId.takeIf { it != 0 }
                }
                is ApiResult.Failure -> {
                    messages = nextMessages + LessonTutorMessage(
                        role = LessonTutorRole.Assistant,
                        content = "Sorry, I couldn't process that. Try again in a moment!",
                        isError = true,
                    )
                    message = currentMessage
                    draftNotice = "Could not reach tutor. Your question is still in the field."
                }
            }
            loading = false
        }
    }

    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text(
            text = "Study Buddy",
            style = MaterialTheme.typography.titleMedium,
        )
        Text(
            text = "Ask about ${lesson.title}.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

        if (messages.isEmpty()) {
            CSNexusCard {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("Hi! I'm your study buddy.", style = MaterialTheme.typography.titleMedium)
                    Text(
                        "Ask me to summarize, quiz you, give an example, or share exam tips for this lesson.",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    LessonTutorQuickActions(
                        onAction = { quickAction -> sendMessage(quickAction.message) },
                    )
                }
            }
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                messages.forEach { chatMessage ->
                    LessonTutorBubble(chatMessage)
                }
                if (loading) {
                    CSNexusCard {
                        Text(
                            text = "Study buddy is thinking...",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
                if (lastInteractionId != null && messages.lastOrNull()?.isError == false && !loading) {
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        CSNexusButton(
                            text = "Helpful",
                            onClick = {
                                lastInteractionId?.let { interactionId ->
                                    scope.launch { tutorRepository?.rateInteraction(interactionId, true) }
                                }
                            },
                            variant = CSNexusButtonVariant.Ghost,
                        )
                        CSNexusButton(
                            text = "Not helpful",
                            onClick = {
                                lastInteractionId?.let { interactionId ->
                                    scope.launch { tutorRepository?.rateInteraction(interactionId, false) }
                                }
                            },
                            variant = CSNexusButtonVariant.Ghost,
                        )
                    }
                }
            }
        }

        CSNexusTextField(
            value = message,
            onValueChange = {
                message = it
                draftNotice = null
            },
            label = "Ask about this lesson",
            singleLine = false,
            supportingText = draftNotice,
        )

        LessonTutorQuickActions(
            onAction = { quickAction -> sendMessage(quickAction.message) },
        )

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp), modifier = Modifier.fillMaxWidth()) {
            CSNexusButton(
                text = "Send",
                onClick = { sendMessage(message) },
                enabled = message.isNotBlank() && !loading,
                loading = loading,
                modifier = Modifier.weight(1f),
            )
        }

        if (tutorRepository == null) {
            Text(
                text = "Tutor is unavailable offline. Your draft will stay in the field until you reconnect.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.bodySmall,
            )
        }
    }
}

private enum class LessonTutorRole(val wireValue: String) {
    User("user"),
    Assistant("assistant"),
}

private data class LessonTutorMessage(
    val role: LessonTutorRole,
    val content: String,
    val isError: Boolean = false,
)

private data class LessonTutorQuickAction(
    val label: String,
    val message: String,
)

private val lessonTutorQuickActions = listOf(
    LessonTutorQuickAction(label = "Summarize", message = "Summarize this section"),
    LessonTutorQuickAction(label = "Quiz me", message = "Quiz me"),
    LessonTutorQuickAction(label = "Example", message = "Give me an example"),
    LessonTutorQuickAction(label = "Memory tips", message = "Help me remember this"),
    LessonTutorQuickAction(label = "Exam tips", message = "How is this tested in the CSE?"),
)

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun LessonTutorQuickActions(
    onAction: (LessonTutorQuickAction) -> Unit,
) {
    FlowRow(
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        lessonTutorQuickActions.forEach { quickAction ->
            CSNexusButton(
                text = quickAction.label,
                onClick = { onAction(quickAction) },
                variant = CSNexusButtonVariant.Secondary,
            )
        }
    }
}

@Composable
private fun LessonTutorBubble(
    message: LessonTutorMessage,
) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                text = if (message.role == LessonTutorRole.User) "You" else "Study buddy",
                style = MaterialTheme.typography.labelMedium,
                color = if (message.role == LessonTutorRole.User) {
                    MaterialTheme.colorScheme.primary
                } else if (message.isError) {
                    MaterialTheme.colorScheme.error
                } else {
                    MaterialTheme.colorScheme.secondary
                },
            )
            Text(
                text = message.content,
                style = MaterialTheme.typography.bodyMedium,
                color = if (message.isError) {
                    MaterialTheme.colorScheme.error
                } else {
                    MaterialTheme.colorScheme.onSurface
                },
            )
        }
    }
}

/**
 * Fixed 3dp gold-gradient reading progress bar drawn at the viewport top.
 * Uses Canvas to draw a horizontal gold gradient bar based on scroll progress.
 */
@Composable
private fun ReadingProgressBar(
    progress: Float,
    modifier: Modifier = Modifier,
) {
    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(3.dp),
    ) {
        val barWidth = size.width * progress.coerceIn(0f, 1f)
        if (barWidth > 0f) {
            drawRect(
                brush = Brush.horizontalGradient(
                    colors = listOf(
                        Color(0xFFC9A84C), // GoldAccent
                        Color(0xFFE8C96A), // GoldMetallic
                    ),
                    endX = size.width,
                ),
                size = Size(barWidth, size.height),
            )
        }
    }
}

/**
 * XP gain animation overlay shown on lesson completion.
 * Displays a centered "+XP" text with fade-in/out and scale animation.
 */
@Composable
private fun XpGainOverlay(
    visible: Boolean,
    onDismiss: () -> Unit,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val alpha = remember { Animatable(0f) }
    val scale = remember { Animatable(0.6f) }
    val scope = rememberCoroutineScope()

    LaunchedEffect(visible) {
        if (visible) {
            if (reducedMotion) {
                alpha.snapTo(1f)
                scale.snapTo(1f)
            } else {
                alpha.animateTo(1f, animationSpec = tween(300))
                scale.animateTo(1.2f, animationSpec = tween(300))
            }
            delay(1200)
            if (reducedMotion) {
                alpha.snapTo(0f)
            } else {
                alpha.animateTo(0f, animationSpec = tween(400))
            }
            onDismiss()
        } else {
            alpha.snapTo(0f)
            scale.snapTo(0.6f)
        }
    }

    if (alpha.value > 0f) {
        Box(
            modifier = Modifier
                .fillMaxSize(),
            contentAlignment = Alignment.Center,
        ) {
            // Semi-transparent dark scrim
            Canvas(modifier = Modifier.fillMaxSize()) {
                drawRect(
                    color = Color.Black.copy(alpha = 0.5f * alpha.value),
                )
            }
            // XP text with gold gradient
            Text(
                text = "+25 XP",
                style = MaterialTheme.typography.displayLarge.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = (48 * scale.value).sp,
                ),
                color = Color(0xFFE8C96A).copy(alpha = alpha.value),
                textAlign = TextAlign.Center,
            )
        }
    }
}
