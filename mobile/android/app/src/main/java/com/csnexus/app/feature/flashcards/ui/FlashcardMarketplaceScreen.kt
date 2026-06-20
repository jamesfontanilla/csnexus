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
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusSearchField
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.DeckCategory
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.MarketplaceDeckDto
import com.csnexus.app.feature.flashcards.data.MarketplaceSort
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@Composable
fun FlashcardMarketplaceScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
) {
    val scope = rememberCoroutineScope()
    var decks by remember { mutableStateOf<List<MarketplaceDeckDto>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var search by remember { mutableStateOf("") }
    var debouncedSearch by remember { mutableStateOf("") }
    var category by remember { mutableStateOf<DeckCategory?>(null) }
    var sort by remember { mutableStateOf(MarketplaceSort.Popular) }
    var commentDeckId by remember { mutableIntStateOf(0) }
    var comments by remember { mutableStateOf(listOf<com.csnexus.app.feature.flashcards.data.DeckCommentDto>()) }
    var newComment by remember { mutableStateOf("") }
    var ratingDeckId by remember { mutableIntStateOf(0) }
    var ratingScore by remember { mutableIntStateOf(5) }
    var bookmarkedDeckIds by remember { mutableStateOf(setOf<Int>()) }

    suspend fun load() {
        loading = true
        errorMessage = null
        when (
            val result = repository.marketplace(
                search = debouncedSearch,
                category = category,
                sort = sort,
            )
        ) {
            is ApiResult.Success -> decks = result.value
            is ApiResult.Failure -> errorMessage = "Could not load the marketplace."
        }
        loading = false
    }

    LaunchedEffect(search) {
        delay(300)
        debouncedSearch = search
    }

    LaunchedEffect(debouncedSearch, category, sort) {
        load()
    }

    if (loading && decks.isEmpty()) {
        LoadingState(label = "Loading marketplace")
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
            Text("Marketplace", style = MaterialTheme.typography.headlineMedium)
            Text("Search, clone, bookmark, rate, and discuss community decks.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        item {
            CSNexusCard {
                Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    CSNexusSearchField(value = search, onValueChange = { search = it }, placeholder = "Search decks")
                    RowWrap {
                        CSNexusChip(text = "All", selected = category == null, onClick = { category = null })
                        DeckCategory.entries.forEach { option ->
                            CSNexusChip(
                                text = option.label,
                                selected = category == option,
                                onClick = { category = option },
                            )
                        }
                    }
                    RowWrap {
                        MarketplaceSort.entries.forEach { option ->
                            CSNexusChip(
                                text = option.label,
                                selected = sort == option,
                                onClick = { sort = option },
                            )
                        }
                    }
                }
            }
        }
        if (errorMessage != null) {
            item {
                Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
            }
        }
        if (decks.isEmpty()) {
            item {
                CSNexusCard {
                    Text("No marketplace decks matched the current filters.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        } else {
            items(decks, key = { it.id }) { deck ->
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(deck.title, style = MaterialTheme.typography.titleMedium)
                        if (!deck.description.isNullOrBlank()) {
                            Text(deck.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        RowWrap {
                            CSNexusChip(text = deck.category.label)
                            CSNexusChip(text = "${deck.cardCount} cards")
                            CSNexusChip(text = "★ ${deck.averageRating.formatOneDecimal()}")
                            CSNexusChip(text = "${deck.cloneCount} clones")
                        }
                        Text("By ${deck.creatorName}", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                            CSNexusButton(
                                text = "Clone",
                                onClick = {
                                    scope.launch {
                                        when (repository.cloneDeck(deck.id)) {
                                            is ApiResult.Success -> errorMessage = "Deck cloned to your library."
                                            is ApiResult.Failure -> errorMessage = "Could not clone this deck."
                                        }
                                    }
                                },
                                modifier = Modifier.weight(1f),
                            )
                            CSNexusButton(
                                text = if (deck.id in bookmarkedDeckIds) "Bookmarked" else "Bookmark",
                                onClick = {
                                    scope.launch {
                                        val result = if (deck.id in bookmarkedDeckIds) {
                                            repository.unbookmarkDeck(deck.id)
                                        } else {
                                            repository.bookmarkDeck(deck.id)
                                        }
                                        when (result) {
                                            is ApiResult.Success -> {
                                                bookmarkedDeckIds = bookmarkedDeckIds.toMutableSet().also { set ->
                                                    if (!set.add(deck.id)) set.remove(deck.id)
                                                }
                                            }
                                            is ApiResult.Failure -> errorMessage = "Could not update bookmark."
                                        }
                                    }
                                },
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Secondary,
                            )
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                            CSNexusButton(
                                text = if (ratingDeckId == deck.id) "Hide rating" else "Rate",
                                onClick = { ratingDeckId = if (ratingDeckId == deck.id) 0 else deck.id },
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Ghost,
                            )
                            CSNexusButton(
                                text = if (commentDeckId == deck.id) "Hide comments" else "Comments",
                                onClick = {
                                    commentDeckId = if (commentDeckId == deck.id) 0 else deck.id
                                    if (commentDeckId == deck.id) {
                                        scope.launch {
                                            when (val result = repository.comments(deck.id)) {
                                                is ApiResult.Success -> comments = result.value
                                                is ApiResult.Failure -> errorMessage = "Could not load comments."
                                            }
                                        }
                                    }
                                },
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Ghost,
                            )
                        }
                        if (ratingDeckId == deck.id) {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text("Rate this deck", style = MaterialTheme.typography.titleSmall)
                                CSNexusSegmentedControl(
                                    options = listOf("1", "2", "3", "4", "5"),
                                    selectedIndex = ratingScore - 1,
                                    onSelected = { ratingScore = it + 1 },
                                )
                                CSNexusButton(
                                    text = "Submit rating",
                                    onClick = {
                                        scope.launch {
                                            when (repository.rateDeck(deck.id, ratingScore)) {
                                                is ApiResult.Success -> ratingDeckId = 0
                                                is ApiResult.Failure -> errorMessage = "Could not submit rating."
                                            }
                                        }
                                    },
                                    modifier = Modifier.fillMaxWidth(),
                                )
                            }
                        }
                        if (commentDeckId == deck.id) {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text("Comments", style = MaterialTheme.typography.titleSmall)
                                comments.forEach { comment ->
                                    CSNexusCard {
                                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                            Text(comment.userName, style = MaterialTheme.typography.titleSmall)
                                            Text(comment.comment)
                                        }
                                    }
                                }
                                CSNexusTextField(
                                    value = newComment,
                                    onValueChange = { newComment = it },
                                    label = "Add a comment",
                                    singleLine = false,
                                )
                                CSNexusButton(
                                    text = "Post comment",
                                    onClick = {
                                        scope.launch {
                                            when (repository.postComment(deck.id, newComment.trim())) {
                                                is ApiResult.Success -> {
                                                    newComment = ""
                                                    when (val result = repository.comments(deck.id)) {
                                                        is ApiResult.Success -> comments = result.value
                                                        is ApiResult.Failure -> errorMessage = "Could not refresh comments."
                                                    }
                                                }
                                                is ApiResult.Failure -> errorMessage = "Could not post comment."
                                            }
                                        }
                                    },
                                    enabled = newComment.isNotBlank(),
                                    modifier = Modifier.fillMaxWidth(),
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

private fun Double.formatOneDecimal(): String = if (this % 1.0 == 0.0) {
    toInt().toString()
} else {
    String.format(java.util.Locale.US, "%.1f", this)
}
