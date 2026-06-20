package com.csnexus.app.feature.motivation.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.motivation.data.DailyQueueDto
import com.csnexus.app.feature.motivation.data.MotivationRepository
import com.csnexus.app.feature.motivation.data.QueueItemDto
import com.csnexus.app.feature.motivation.data.QueuePreferencesDto
import kotlinx.coroutines.launch

@Composable
fun QueueScreen(
    repository: MotivationRepository,
    contentPadding: PaddingValues,
    onOpenLesson: (Int) -> Unit,
    onOpenQuiz: (Int) -> Unit,
    onOpenFlashcards: (List<Int>) -> Unit,
) {
    val scope = rememberCoroutineScope()
    var queue by remember { mutableStateOf<DailyQueueDto?>(null) }
    var preferences by remember { mutableStateOf<QueuePreferencesDto?>(null) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    fun loadAll() {
        loading = true
        errorMessage = null
        scope.launch {
            when (val queueResult = repository.queue()) {
                is ApiResult.Success -> queue = queueResult.value
                is ApiResult.Failure -> errorMessage = queueResult.error.userMessage()
            }
            when (val preferenceResult = repository.queuePreferences()) {
                is ApiResult.Success -> preferences = preferenceResult.value
                is ApiResult.Failure -> if (errorMessage == null) errorMessage = preferenceResult.error.userMessage()
            }
            loading = false
        }
    }

    fun updateTimeBudget(minutes: Int) {
        scope.launch {
            when (val result = repository.updateQueuePreferences(minutes)) {
                is ApiResult.Success -> {
                    preferences = result.value.first
                    queue = result.value.second
                    errorMessage = null
                }
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
        }
    }

    fun completeItem(itemId: Int) {
        scope.launch {
            when (val result = repository.completeQueueItem(itemId)) {
                is ApiResult.Success -> queue = result.value
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
        }
    }

    fun regenerate() {
        scope.launch {
            when (val result = repository.regenerateQueue()) {
                is ApiResult.Success -> queue = result.value
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
        }
    }

    fun startItem(item: QueueItemDto) {
        when (val destination = queueDestination(item)) {
            is QueueDestination.Lesson -> onOpenLesson(destination.subtopicId)
            is QueueDestination.Quiz -> onOpenQuiz(destination.subtopicId)
            is QueueDestination.Flashcards -> onOpenFlashcards(destination.deckIds)
            QueueDestination.Unknown -> errorMessage = "This queue item does not expose a native destination yet."
        }
    }

    LaunchedEffect(Unit) {
        loadAll()
    }

    if (loading) {
        LoadingState(label = "Loading daily queue", modifier = Modifier.fillMaxSize())
        return
    }

    val currentQueue = queue
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            MetallicText("Today's study queue", style = MaterialTheme.typography.headlineMedium)
            CSNexusButton(
                text = "Regenerate",
                onClick = ::regenerate,
                variant = CSNexusButtonVariant.Ghost,
            )
        }

        if (errorMessage != null && currentQueue == null) {
            QueueErrorCard(message = errorMessage!!, onRetry = ::loadAll)
            return@Column
        }

        if (currentQueue == null || currentQueue.items.isEmpty()) {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("All done for today", style = MaterialTheme.typography.titleMedium)
                    Text(
                        "You've completed the current queue. Come back tomorrow for a fresh study stack.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            return@Column
        }

        if (errorMessage != null) {
            QueueErrorCard(message = errorMessage!!, onRetry = ::loadAll)
        }

        val totalItems = currentQueue.itemsCompleted + currentQueue.itemsRemaining
        val progress = if (totalItems == 0) 0f else currentQueue.itemsCompleted.toFloat() / totalItems.toFloat()
        val firstUncompleted = currentQueue.items.firstOrNull { it.completedAt == null }

        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Text("${currentQueue.itemsCompleted} of $totalItems items completed")
                    Text("~${queueDurationLabel(currentQueue.totalEstimatedSeconds)} total")
                }
                LuxuryProgressBar(progress = progress, modifier = Modifier.fillMaxWidth())
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf(15, 30, 60).forEach { minutes ->
                        CSNexusChip(
                            text = "${minutes}m",
                            selected = preferences?.timeBudgetMinutes == minutes,
                            onClick = { updateTimeBudget(minutes) },
                        )
                    }
                }
            }
        }

        if (firstUncompleted != null) {
            CSNexusButton(
                text = "Start Next: ${queueItemLabel(firstUncompleted.itemType)}",
                onClick = { startItem(firstUncompleted) },
                modifier = Modifier.fillMaxWidth(),
            )
        }

        currentQueue.items.forEachIndexed { index, item ->
            StaggeredItem(index = index) {
                QueueItemCard(
                    item = item,
                    onStart = { startItem(item) },
                    onComplete = { completeItem(item.id) },
                )
            }
        }
    }
}

@Composable
private fun QueueItemCard(
    item: QueueItemDto,
    onStart: () -> Unit,
    onComplete: () -> Unit,
) {
    val completed = item.completedAt != null
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    queueItemLabel(item.itemType),
                    style = MaterialTheme.typography.titleMedium,
                    textDecoration = if (completed) TextDecoration.LineThrough else null,
                    color = if (completed) MaterialTheme.colorScheme.onSurfaceVariant else MaterialTheme.colorScheme.onSurface,
                )
                Text(
                    "${queueItemIcon(item.itemType)} · ~${queueDurationLabel(item.estimatedSeconds)}",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            if (completed) {
                Text("✓", color = Color(0xFF4CAF50), fontWeight = FontWeight.SemiBold)
            } else {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    CSNexusButton(
                        text = "Start",
                        onClick = onStart,
                    )
                    CSNexusButton(
                        text = "Skip",
                        onClick = onComplete,
                        variant = CSNexusButtonVariant.Ghost,
                    )
                }
            }
        }
    }
}

@Composable
private fun QueueErrorCard(
    message: String,
    onRetry: () -> Unit,
) {
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Queue unavailable", style = MaterialTheme.typography.titleMedium)
            Text(message, color = MaterialTheme.colorScheme.onSurfaceVariant)
            CSNexusButton(text = "Retry", onClick = onRetry, variant = CSNexusButtonVariant.Secondary)
        }
    }
}
