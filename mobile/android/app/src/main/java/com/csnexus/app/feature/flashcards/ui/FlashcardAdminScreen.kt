package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusConfirmDialog
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.FlashcardAdminAnalyticsDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import kotlinx.coroutines.launch

@Composable
fun FlashcardAdminScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
    isAdmin: Boolean,
) {
    if (!isAdmin) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding)
                .padding(24.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Text("Admin access required", style = MaterialTheme.typography.headlineMedium)
            Text("This route is hidden for non-admin accounts and guarded again here in native code.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        return
    }

    val scope = rememberCoroutineScope()
    var analytics by remember { mutableStateOf<FlashcardAdminAnalyticsDto?>(null) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var moderationDeckId by remember { mutableIntStateOf(0) }
    var moderationAction by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        when (val result = repository.adminAnalytics()) {
            is ApiResult.Success -> analytics = result.value
            is ApiResult.Failure -> errorMessage = "Could not load flashcard admin analytics."
        }
        loading = false
    }

    if (moderationAction != null && moderationDeckId != 0) {
        val action = moderationAction!!
        CSNexusConfirmDialog(
            title = if (action == "flag") "Flag deck?" else "Toggle featured?",
            body = "Deck #$moderationDeckId will be sent to the available moderation endpoint.",
            confirmText = if (action == "flag") "Flag deck" else "Toggle featured",
            onConfirm = {
                scope.launch {
                    when (
                        if (action == "flag") {
                            repository.flagDeck(moderationDeckId)
                        } else {
                            repository.featureDeck(moderationDeckId)
                        }
                    ) {
                        is ApiResult.Success -> errorMessage = "Action completed."
                        is ApiResult.Failure -> errorMessage = "Moderation action failed."
                    }
                    moderationAction = null
                    moderationDeckId = 0
                }
            },
            onDismiss = {
                moderationAction = null
                moderationDeckId = 0
            },
            danger = action == "flag",
        )
    }

    if (loading) {
        LoadingState(label = "Loading flashcard admin")
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
            Text("Flashcard Admin", style = MaterialTheme.typography.headlineMedium)
            Text("Available moderation endpoints are implemented. Richer workflow states remain tracked as a backend gap.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        if (errorMessage != null) {
            item {
                Text(errorMessage!!, color = if (errorMessage!!.contains("completed")) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error)
            }
        }
        item {
            PremiumCard {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Active reviewers (7 days)", style = MaterialTheme.typography.titleMedium)
                    Text("${analytics?.activeReviewers7d ?: 0}", style = MaterialTheme.typography.headlineLarge)
                }
            }
        }
        item {
            ModerationActionCard(
                onFlag = { deckId ->
                    moderationDeckId = deckId
                    moderationAction = "flag"
                },
                onFeature = { deckId ->
                    moderationDeckId = deckId
                    moderationAction = "feature"
                },
            )
        }
        item {
            Text("Top Failed Cards", style = MaterialTheme.typography.titleLarge)
        }
        if (analytics?.topFailedCards.isNullOrEmpty()) {
            item {
                PremiumCard {
                    Text("No failure data yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        } else {
            items(analytics!!.topFailedCards, key = { it.cardId }) { card ->
                PremiumCard {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Text("Card #${card.cardId}")
                        Text("${card.failCount} failures", color = MaterialTheme.colorScheme.error)
                    }
                }
            }
        }
    }
}

@Composable
private fun ModerationActionCard(
    onFlag: (Int) -> Unit,
    onFeature: (Int) -> Unit,
) {
    var deckIdInput by remember { mutableStateOf("") }
    PremiumCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Moderation Actions", style = MaterialTheme.typography.titleMedium)
            CSNexusTextField(
                value = deckIdInput,
                onValueChange = { deckIdInput = it.filter(Char::isDigit) },
                label = "Deck ID",
            )
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                CSNexusButton(
                    text = "Flag for removal",
                    onClick = { deckIdInput.toIntOrNull()?.let(onFlag) },
                    enabled = deckIdInput.isNotBlank(),
                    modifier = Modifier.weight(1f),
                    variant = CSNexusButtonVariant.Danger,
                )
                CSNexusButton(
                    text = "Toggle featured",
                    onClick = { deckIdInput.toIntOrNull()?.let(onFeature) },
                    enabled = deckIdInput.isNotBlank(),
                    modifier = Modifier.weight(1f),
                    variant = CSNexusButtonVariant.Secondary,
                )
            }
        }
    }
}
