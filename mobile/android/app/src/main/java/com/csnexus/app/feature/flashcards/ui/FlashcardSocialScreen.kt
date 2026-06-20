package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusTabs
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository

@Composable
fun FlashcardSocialScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
) {
    var selectedTab by remember { mutableStateOf(0) }
    var feed by remember { mutableStateOf<List<DeckDto>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(selectedTab) {
        if (selectedTab != 0) return@LaunchedEffect
        loading = true
        when (val result = repository.feed()) {
            is ApiResult.Success -> feed = result.value
            is ApiResult.Failure -> errorMessage = "Could not load the social feed."
        }
        loading = false
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Text("Social", style = MaterialTheme.typography.headlineMedium)
            Text("Creator feed and a placeholder following view, matching the current web shape.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        item {
            CSNexusTabs(
                tabs = listOf("Feed", "Following"),
                selectedIndex = selectedTab,
                onSelected = { selectedTab = it },
            )
        }
        if (selectedTab == 0) {
            when {
                loading -> item { Text("Loading feed...", color = MaterialTheme.colorScheme.onSurfaceVariant) }
                errorMessage != null -> item { Text(errorMessage!!, color = MaterialTheme.colorScheme.error) }
                feed.isEmpty() -> item {
                    CSNexusCard {
                        Text("No decks in your feed yet. Browse marketplace creators to populate this view.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                else -> items(feed, key = { it.id }) { deck ->
                    CSNexusCard {
                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            Text(deck.title, style = MaterialTheme.typography.titleMedium)
                            if (!deck.description.isNullOrBlank()) {
                                Text(deck.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                            Text("${deck.cardCount} cards • ${deck.category.label}", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        } else {
            item {
                CSNexusCard {
                    Text("Following is not wired on the current backend. This matches the web placeholder state.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}
