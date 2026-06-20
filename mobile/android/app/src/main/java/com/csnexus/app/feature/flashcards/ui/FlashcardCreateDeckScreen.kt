package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.DeckCategory
import com.csnexus.app.feature.flashcards.data.DeckCreateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckVisibility
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import kotlinx.coroutines.launch

@Composable
fun FlashcardCreateDeckScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
    onCreated: (Int) -> Unit,
) {
    val scope = rememberCoroutineScope()
    var title by remember { mutableStateOf("") }
    var description by remember { mutableStateOf("") }
    var category by remember { mutableStateOf(DeckCategory.Verbal) }
    var visibility by remember { mutableStateOf(DeckVisibility.Private) }
    var tagsInput by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var saving by remember { mutableStateOf(false) }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Text("Create New Deck", style = MaterialTheme.typography.headlineMedium)
            Text(
                "Build a personal deck or publish one to the marketplace.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        if (errorMessage != null) {
            item {
                Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
            }
        }
        item {
            PremiumCard {
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    CSNexusTextField(
                        value = title,
                        onValueChange = { title = it.take(255) },
                        label = "Title",
                    )
                    CSNexusTextField(
                        value = description,
                        onValueChange = { description = it },
                        label = "Description",
                        singleLine = false,
                    )
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Category", style = MaterialTheme.typography.titleMedium)
                        RowWrap {
                            DeckCategory.entries.forEach { option ->
                                CSNexusChip(
                                    text = option.label,
                                    selected = category == option,
                                    onClick = { category = option },
                                )
                            }
                        }
                    }
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Visibility", style = MaterialTheme.typography.titleMedium)
                        DeckVisibility.entries.forEach { option ->
                            VisibilityOption(
                                option = option,
                                selected = visibility == option,
                                onClick = { visibility = option },
                            )
                        }
                    }
                    CSNexusTextField(
                        value = tagsInput,
                        onValueChange = { tagsInput = it },
                        label = "Tags",
                        supportingText = "Comma-separated tags for search and organization.",
                    )
                }
            }
        }
        item {
            CSNexusButton(
                text = if (saving) "Creating..." else "Create Deck",
                onClick = {
                    val normalizedTitle = title.trim()
                    if (normalizedTitle.isBlank()) {
                        errorMessage = "Title is required."
                        return@CSNexusButton
                    }
                    val tags = tagsInput
                        .split(",")
                        .map { it.trim() }
                        .filter { it.isNotBlank() }
                    scope.launch {
                        saving = true
                        errorMessage = null
                        when (
                            val result = repository.createDeck(
                                DeckCreateRequestDto(
                                    title = normalizedTitle,
                                    description = description.trim().ifBlank { null },
                                    category = category,
                                    visibility = visibility,
                                    tags = tags.ifEmpty { null },
                                ),
                            )
                        ) {
                            is ApiResult.Success -> onCreated(result.value.id)
                            is ApiResult.Failure -> errorMessage = "Could not create deck."
                        }
                        saving = false
                    }
                },
                loading = saving,
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

@Composable
private fun VisibilityOption(
    option: DeckVisibility,
    selected: Boolean,
    onClick: () -> Unit,
) {
    PremiumCard(onClick = onClick) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(option.label, style = MaterialTheme.typography.titleMedium)
            Text(
                when (option) {
                    DeckVisibility.Private -> "Only you can access this deck."
                    DeckVisibility.Public -> "Visible in the marketplace."
                    DeckVisibility.Unlisted -> "Available by direct link or import only."
                },
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            if (selected) {
                Text("Selected", color = MaterialTheme.colorScheme.primary)
            }
        }
    }
}

