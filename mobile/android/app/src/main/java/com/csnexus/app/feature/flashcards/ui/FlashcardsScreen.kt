package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.AutoGraph
import androidx.compose.material.icons.filled.Groups
import androidx.compose.material.icons.filled.LocalLibrary
import androidx.compose.material.icons.filled.Storefront
import androidx.compose.material.icons.filled.Sync
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusConfirmDialog
import com.csnexus.app.core.design.CSNexusListRow
import com.csnexus.app.core.design.CSNexusOfflineBanner
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.csnexusHeading
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.FlashcardStudyMode
import com.csnexus.app.feature.flashcards.data.QueueSummaryDto
import kotlinx.coroutines.launch

@Composable
fun FlashcardsScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
    onOpenCreateDeck: () -> Unit,
    onOpenDeck: (Int) -> Unit,
    onOpenStudy: (List<Int>, FlashcardStudyMode?) -> Unit,
    onOpenMarketplace: () -> Unit,
    onOpenAnalytics: () -> Unit,
    onOpenExam: () -> Unit,
    onOpenSocial: () -> Unit,
    onOpenGenerate: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var decks by remember { mutableStateOf<List<DeckDto>>(emptyList()) }
    var queueSummary by remember { mutableStateOf<QueueSummaryDto?>(null) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var pendingSyncCount by remember { mutableIntStateOf(0) }
    var deleteDeckId by remember { mutableStateOf<Int?>(null) }
    var statusMessage by remember { mutableStateOf<String?>(null) }

    fun load() {
        scope.launch {
            loading = true
            errorMessage = null
            val decksResult = repository.decks()
            val queueResult = repository.queueSummary()
            when {
                decksResult is ApiResult.Success && queueResult is ApiResult.Success -> {
                    decks = decksResult.value
                    queueSummary = queueResult.value
                }
                decksResult is ApiResult.Failure -> {
                    errorMessage = decksResult.error.userMessage()
                }
                queueResult is ApiResult.Failure -> {
                    errorMessage = queueResult.error.userMessage()
                }
            }
            pendingSyncCount = repository.pendingSyncCount()
            loading = false
        }
    }

    LaunchedEffect(Unit) { load() }

    if (deleteDeckId != null) {
        CSNexusConfirmDialog(
            title = "Delete deck?",
            body = "This deck and its cards will be removed from your account.",
            confirmText = "Delete",
            onConfirm = {
                val deckId = deleteDeckId ?: return@CSNexusConfirmDialog
                scope.launch {
                    when (repository.deleteDeck(deckId)) {
                        is ApiResult.Success -> {
                            decks = decks.filterNot { it.id == deckId }
                            statusMessage = "Deck deleted."
                        }
                        is ApiResult.Failure -> errorMessage = "Failed to delete deck."
                    }
                    deleteDeckId = null
                }
            },
            onDismiss = { deleteDeckId = null },
            danger = true,
        )
    }

    if (loading) {
        LoadingState(label = "Loading flashcards")
        return
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(
                        text = "Flashcards",
                        modifier = Modifier.csnexusHeading(),
                        style = MaterialTheme.typography.headlineMedium,
                    )
                    Text(
                        "Decks, review queue, marketplace, analytics, and native study flows.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                CSNexusButton(
                    text = "Create",
                    onClick = onOpenCreateDeck,
                    leadingIcon = { Icon(Icons.Filled.Add, contentDescription = null) },
                )
            }
        }

        if (pendingSyncCount > 0) {
            item {
                PremiumCard {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        CSNexusOfflineBanner(
                            message = "$pendingSyncCount study responses are waiting to sync.",
                        )
                        CSNexusButton(
                            text = "Sync pending responses",
                            onClick = {
                                scope.launch {
                                    when (val result = repository.syncPendingResponses()) {
                                        is ApiResult.Success -> {
                                            pendingSyncCount = repository.pendingSyncCount()
                                            statusMessage = if (result.value > 0) {
                                                "Synced ${result.value} pending responses."
                                            } else {
                                                "Nothing to sync."
                                            }
                                        }
                                        is ApiResult.Failure -> errorMessage = "Could not sync pending responses yet."
                                    }
                                }
                            },
                            variant = CSNexusButtonVariant.Secondary,
                            leadingIcon = { Icon(Icons.Filled.Sync, contentDescription = null) },
                        )
                    }
                }
            }
        }

        if (queueSummary != null && queueSummary!!.dueCount > 0) {
            item {
                PremiumCard(onClick = { onOpenStudy(emptyList(), FlashcardStudyMode.Swipe) }) {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(
                            "${queueSummary!!.dueCount} cards due today",
                            style = MaterialTheme.typography.titleMedium,
                        )
                        Text(
                            "${queueSummary!!.overdueCount} overdue • about ${queueSummary!!.estimatedMinutes} minutes",
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            CSNexusButton(
                                text = "Study Now",
                                onClick = { onOpenStudy(emptyList(), FlashcardStudyMode.Swipe) },
                                modifier = Modifier.weight(1f),
                            )
                            CSNexusButton(
                                text = "Type Mode",
                                onClick = { onOpenStudy(emptyList(), FlashcardStudyMode.Typing) },
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Secondary,
                            )
                        }
                    }
                }
            }
        }

        item {
            FlashcardActionGrid(
                onOpenMarketplace = onOpenMarketplace,
                onOpenAnalytics = onOpenAnalytics,
                onOpenExam = onOpenExam,
                onOpenSocial = onOpenSocial,
                onOpenGenerate = onOpenGenerate,
            )
        }

        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text("Your Decks", style = MaterialTheme.typography.titleLarge)
                if (decks.isNotEmpty()) {
                    CSNexusStatusBadge(text = "${decks.size} decks")
                }
            }
        }

        if (errorMessage != null) {
            item {
                Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
            }
        }

        if (statusMessage != null) {
            item {
                Text(statusMessage!!, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }

        if (decks.isEmpty()) {
            item {
                PremiumCard {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Text("No decks yet", style = MaterialTheme.typography.titleMedium)
                        Text(
                            "Create your first deck or pull one in from the marketplace.",
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            CSNexusButton(
                                text = "Create Deck",
                                onClick = onOpenCreateDeck,
                                modifier = Modifier.weight(1f),
                            )
                            CSNexusButton(
                                text = "Marketplace",
                                onClick = onOpenMarketplace,
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Secondary,
                            )
                        }
                    }
                }
            }
        } else {
            items(decks, key = { it.id }) { deck ->
                DeckRow(
                    deck = deck,
                    onOpen = { onOpenDeck(deck.id) },
                    onStudy = { onOpenStudy(listOf(deck.id), FlashcardStudyMode.Swipe) },
                    onTyping = { onOpenStudy(listOf(deck.id), FlashcardStudyMode.Typing) },
                    onDuplicate = {
                        scope.launch {
                            when (val result = repository.duplicateDeck(deck.id)) {
                                is ApiResult.Success -> {
                                    decks = listOf(result.value) + decks
                                    statusMessage = "Deck duplicated."
                                }
                                is ApiResult.Failure -> errorMessage = "Could not duplicate deck."
                            }
                        }
                    },
                    onDelete = { deleteDeckId = deck.id },
                )
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun FlashcardActionGrid(
    onOpenMarketplace: () -> Unit,
    onOpenAnalytics: () -> Unit,
    onOpenExam: () -> Unit,
    onOpenSocial: () -> Unit,
    onOpenGenerate: () -> Unit,
    ) {
        FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        ActionTile(
            title = "Marketplace",
            body = "Browse and clone public decks.",
            icon = { Icon(Icons.Filled.Storefront, contentDescription = null) },
            modifier = Modifier.fillMaxWidth(0.5f),
            onClick = onOpenMarketplace,
        )
        ActionTile(
            title = "Analytics",
            body = "Retention, readiness, and heatmap.",
            icon = { Icon(Icons.Filled.AutoGraph, contentDescription = null) },
            modifier = Modifier.fillMaxWidth(0.5f),
            onClick = onOpenAnalytics,
        )
        ActionTile(
            title = "Exam Sim",
            body = "Timed flashcard challenge.",
            icon = { Icon(Icons.Filled.LocalLibrary, contentDescription = null) },
            modifier = Modifier.fillMaxWidth(0.5f),
            onClick = onOpenExam,
        )
        ActionTile(
            title = "Social",
            body = "Creator feed and community decks.",
            icon = { Icon(Icons.Filled.Groups, contentDescription = null) },
            modifier = Modifier.fillMaxWidth(0.5f),
            onClick = onOpenSocial,
        )
        ActionTile(
            title = "Generate",
            body = "Turn lesson text into draft cards.",
            icon = { Icon(Icons.Filled.Add, contentDescription = null) },
            modifier = Modifier.fillMaxWidth(0.5f),
            onClick = onOpenGenerate,
        )
    }
}

@Composable
private fun ActionTile(
    title: String,
    body: String,
    icon: @Composable () -> Unit,
    modifier: Modifier = Modifier,
    onClick: () -> Unit,
) {
    PremiumCard(modifier = modifier, onClick = onClick) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .heightIn(min = 132.dp)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Box(modifier = Modifier.size(26.dp)) {
                icon()
            }
            Text(
                title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
            Text(
                body,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.bodyMedium,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

@Composable
private fun DeckRow(
    deck: DeckDto,
    onOpen: () -> Unit,
    onStudy: () -> Unit,
    onTyping: () -> Unit,
    onDuplicate: () -> Unit,
    onDelete: () -> Unit,
) {
    CSNexusListRow(
        title = deck.title,
        body = buildString {
            append("${deck.cardCount} cards • ${deck.category.label} • ${deck.visibility.label}")
            if (!deck.description.isNullOrBlank()) append("\n${deck.description}")
        },
        onClick = onOpen,
        trailing = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                CSNexusButton(
                    text = "Study",
                    onClick = onStudy,
                    variant = CSNexusButtonVariant.Secondary,
                )
                CSNexusButton(
                    text = "Type",
                    onClick = onTyping,
                    variant = CSNexusButtonVariant.Ghost,
                )
            }
        },
    )
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 8.dp, bottom = 4.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        CSNexusButton(
            text = "Open",
            onClick = onOpen,
            modifier = Modifier.weight(1f),
            variant = CSNexusButtonVariant.Secondary,
        )
        CSNexusButton(
            text = "Duplicate",
            onClick = onDuplicate,
            modifier = Modifier.weight(1f),
            variant = CSNexusButtonVariant.Ghost,
        )
        CSNexusButton(
            text = "Delete",
            onClick = onDelete,
            modifier = Modifier.weight(1f),
            variant = CSNexusButtonVariant.Danger,
        )
    }
}
