package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
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
import com.csnexus.app.core.design.CSNexusSkeleton
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.CardCreateRequestDto
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.GeneratedCardDto
import kotlinx.coroutines.launch

@Composable
fun FlashcardGenerateScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
) {
    val scope = rememberCoroutineScope()
    var lessonContent by remember { mutableStateOf("") }
    var requestedCount by remember { mutableIntStateOf(25) }
    var generating by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var generatedCards by remember { mutableStateOf<List<Pair<GeneratedCardDto, Boolean>>>(emptyList()) }
    var termsExtracted by remember { mutableIntStateOf(0) }
    var decks by remember { mutableStateOf<List<DeckDto>>(emptyList()) }
    var selectedDeckId by remember { mutableIntStateOf(0) }
    var addMessage by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        when (val decksResult = repository.decks()) {
            is ApiResult.Success -> decks = decksResult.value
            is ApiResult.Failure -> Unit
        }
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Text("Generate Flashcards", style = MaterialTheme.typography.headlineMedium)
            Text("Native draft generation with explicit queue-gap messaging while the backend stays request/response only.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        if (errorMessage != null) {
            item {
                Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
            }
        }
        if (addMessage != null) {
            item {
                Text(addMessage!!, color = MaterialTheme.colorScheme.primary)
            }
        }
        if (generatedCards.isEmpty()) {
            item {
                CSNexusCard(modifier = Modifier.heightIn(min = 260.dp)) {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        CSNexusTextField(
                            value = lessonContent,
                            onValueChange = { lessonContent = it },
                            label = "Lesson content",
                            singleLine = false,
                            supportingText = "${lessonContent.length} characters",
                        )
                        Text("Cards to generate: $requestedCount", style = MaterialTheme.typography.titleSmall)
                        Slider(
                            value = requestedCount.toFloat(),
                            onValueChange = { requestedCount = it.toInt().coerceIn(10, 50) },
                            valueRange = 10f..50f,
                            steps = 7,
                        )
                        if (generating) {
                            CSNexusSkeleton(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(6.dp),
                            )
                            Text("Waiting for the generator. Background queue progress is a documented backend gap.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        CSNexusButton(
                            text = "Generate Cards",
                            onClick = {
                                scope.launch {
                                    if (lessonContent.trim().length < 50) {
                                        errorMessage = "Lesson content must be at least 50 characters."
                                        return@launch
                                    }
                                    generating = true
                                    errorMessage = null
                                    addMessage = null
                                    when (
                                        val result = repository.generateCards(
                                            lessonContent = lessonContent.trim(),
                                            lessonId = 0,
                                            requestedCardCount = requestedCount,
                                        )
                                    ) {
                                        is ApiResult.Success -> {
                                            generatedCards = result.value.cards.map { it to true }
                                            termsExtracted = result.value.termsExtracted
                                        }
                                        is ApiResult.Failure -> errorMessage = "Could not generate cards from this lesson."
                                    }
                                    generating = false
                                }
                            },
                            loading = generating,
                            enabled = lessonContent.trim().length >= 50,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }
            }
        } else {
            item {
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        Text("$termsExtracted terms extracted • ${generatedCards.count { it.second }} cards selected", style = MaterialTheme.typography.titleMedium)
                        RowWrap {
                            decks.forEach { deck ->
                                CSNexusChip(
                                    text = deck.title,
                                    selected = selectedDeckId == deck.id,
                                    onClick = { selectedDeckId = deck.id },
                                )
                            }
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            CSNexusButton(
                                text = "Select all",
                                onClick = { generatedCards = generatedCards.map { it.first to true } },
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Secondary,
                            )
                            CSNexusButton(
                                text = "Clear",
                                onClick = { generatedCards = emptyList() },
                                modifier = Modifier.weight(1f),
                                variant = CSNexusButtonVariant.Ghost,
                            )
                        }
                        CSNexusButton(
                            text = "Add selected to deck",
                            onClick = {
                                scope.launch {
                                    val targetDeckId = selectedDeckId
                                    if (targetDeckId == 0) {
                                        errorMessage = "Choose a deck first."
                                        return@launch
                                    }
                                    val selected = generatedCards.filter { it.second }
                                    selected.forEach { (card, _) ->
                                        repository.createCard(
                                            targetDeckId,
                                            CardCreateRequestDto(
                                                front = card.front,
                                                back = card.back,
                                                cardType = card.cardType,
                                            ),
                                        )
                                    }
                                    addMessage = "Added ${selected.size} cards to deck."
                                    generatedCards = emptyList()
                                }
                            },
                            enabled = generatedCards.any { it.second },
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                }
            }
            itemsIndexed(generatedCards, key = { index, _ -> index }) { index, entry ->
                val card = entry.first
                val selected = entry.second
                CSNexusCard(onClick = {
                    generatedCards = generatedCards.toMutableList().also {
                        it[index] = card to !selected
                    }
                }) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(card.front, style = MaterialTheme.typography.titleMedium)
                        Text(card.back, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            CSNexusChip(text = card.cardType.label)
                            CSNexusChip(text = card.difficulty.ifBlank { "medium" })
                            if (selected) CSNexusChip(text = "Selected")
                        }
                    }
                }
            }
        }
    }
}
