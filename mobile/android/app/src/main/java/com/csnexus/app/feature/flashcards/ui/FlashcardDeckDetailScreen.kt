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
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusConfirmDialog
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.CardUpdateRequestDto
import com.csnexus.app.feature.flashcards.data.CardCreateRequestDto
import com.csnexus.app.feature.flashcards.data.CardType
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.DeckUpdateRequestDto
import com.csnexus.app.feature.flashcards.data.FlashcardDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.FlashcardStudyMode
import kotlinx.coroutines.launch

@Composable
fun FlashcardDeckDetailScreen(
    repository: FlashcardRepository,
    deckId: Int,
    contentPadding: PaddingValues,
    onStudyDeck: (List<Int>, FlashcardStudyMode?) -> Unit,
) {
    val scope = rememberCoroutineScope()
    var deck by remember { mutableStateOf<DeckDto?>(null) }
    var cards by remember { mutableStateOf<List<FlashcardDto>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var editingDeck by remember { mutableStateOf(false) }
    var addingCard by remember { mutableStateOf(false) }
    var deleteCardId by remember { mutableIntStateOf(0) }

    suspend fun load() {
        loading = true
        errorMessage = null
        val deckResult = repository.deck(deckId)
        val cardsResult = repository.deckCards(deckId)
        when {
            deckResult is ApiResult.Success && cardsResult is ApiResult.Success -> {
                deck = deckResult.value
                cards = cardsResult.value
            }
            deckResult is ApiResult.Failure -> errorMessage = "Could not load this deck."
            cardsResult is ApiResult.Failure -> errorMessage = "Could not load cards for this deck."
        }
        loading = false
    }

    LaunchedEffect(deckId) { load() }

    if (deleteCardId != 0) {
        CSNexusConfirmDialog(
            title = "Delete card?",
            body = "This card will be removed from the deck.",
            confirmText = "Delete",
            onConfirm = {
                val cardId = deleteCardId
                scope.launch {
                    when (repository.deleteCard(deckId, cardId)) {
                        is ApiResult.Success -> cards = cards.filterNot { it.id == cardId }
                        is ApiResult.Failure -> errorMessage = "Could not delete card."
                    }
                    deleteCardId = 0
                }
            },
            onDismiss = { deleteCardId = 0 },
            danger = true,
        )
    }

    if (loading) {
        LoadingState(label = "Loading deck")
        return
    }

    val currentDeck = deck
    if (currentDeck == null) {
        Text("Deck not found", modifier = Modifier.padding(24.dp), color = MaterialTheme.colorScheme.error)
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
            PremiumCard {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text(currentDeck.title, style = MaterialTheme.typography.headlineMedium)
                    if (!currentDeck.description.isNullOrBlank()) {
                        Text(currentDeck.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        CSNexusChip(text = currentDeck.category.label)
                        CSNexusChip(text = currentDeck.visibility.label)
                        CSNexusChip(text = "${cards.size} cards")
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        CSNexusButton(
                            text = "Study",
                            onClick = { onStudyDeck(listOf(deckId), FlashcardStudyMode.Swipe) },
                            modifier = Modifier.weight(1f),
                        )
                        CSNexusButton(
                            text = "Type",
                            onClick = { onStudyDeck(listOf(deckId), FlashcardStudyMode.Typing) },
                            modifier = Modifier.weight(1f),
                            variant = CSNexusButtonVariant.Secondary,
                        )
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        CSNexusButton(
                            text = if (editingDeck) "Hide edit" else "Edit deck",
                            onClick = { editingDeck = !editingDeck },
                            modifier = Modifier.weight(1f),
                            variant = CSNexusButtonVariant.Ghost,
                        )
                        CSNexusButton(
                            text = if (addingCard) "Hide add card" else "Add card",
                            onClick = { addingCard = !addingCard },
                            modifier = Modifier.weight(1f),
                            variant = CSNexusButtonVariant.Secondary,
                        )
                    }
                }
            }
        }

        if (editingDeck) {
            item {
                EditDeckCard(
                    deck = currentDeck,
                    onSave = { title, description ->
                        scope.launch {
                            when (
                                val result = repository.updateDeck(
                                    deckId = deckId,
                                    request = DeckUpdateRequestDto(
                                        title = title,
                                        description = description,
                                    ),
                                )
                            ) {
                                is ApiResult.Success -> {
                                    deck = result.value
                                    editingDeck = false
                                }
                                is ApiResult.Failure -> errorMessage = "Could not update deck."
                            }
                        }
                    },
                )
            }
        }

        if (addingCard) {
            item {
                AddCardCard(
                    onAdd = { front, back, cardType ->
                        scope.launch {
                            when (
                                val result = repository.createCard(
                                    deckId = deckId,
                                    request = CardCreateRequestDto(
                                        front = front,
                                        back = back,
                                        cardType = cardType,
                                    ),
                                )
                            ) {
                                is ApiResult.Success -> {
                                    cards = cards + result.value
                                    addingCard = false
                                }
                                is ApiResult.Failure -> errorMessage = "Could not add card."
                            }
                        }
                    },
                )
            }
        }

        if (errorMessage != null) {
            item {
                Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
            }
        }

        if (cards.isEmpty()) {
            item {
                PremiumCard {
                    Text("No cards yet. Add one to start studying.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        } else {
            items(cards, key = { it.id }) { card ->
                FlashcardItem(
                    card = card,
                    onDelete = { deleteCardId = card.id },
                    onSave = { front, back, type ->
                        scope.launch {
                            when (
                                val result = repository.updateCard(
                                    deckId = deckId,
                                    cardId = card.id,
                                    request = CardUpdateRequestDto(
                                        front = front,
                                        back = back,
                                        cardType = type,
                                    ),
                                )
                            ) {
                                is ApiResult.Success -> cards = cards.map {
                                    if (it.id == card.id) result.value else it
                                }
                                is ApiResult.Failure -> errorMessage = "Could not update card."
                            }
                        }
                    },
                )
            }
        }
    }
}

@Composable
private fun EditDeckCard(
    deck: DeckDto,
    onSave: (String, String?) -> Unit,
) {
    var title by remember(deck.id) { mutableStateOf(deck.title) }
    var description by remember(deck.id) { mutableStateOf(deck.description.orEmpty()) }

    PremiumCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Edit deck", style = MaterialTheme.typography.titleMedium)
            CSNexusTextField(value = title, onValueChange = { title = it }, label = "Title")
            CSNexusTextField(
                value = description,
                onValueChange = { description = it },
                label = "Description",
                singleLine = false,
            )
            CSNexusButton(
                text = "Save changes",
                onClick = { onSave(title.trim(), description.trim().ifBlank { null }) },
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

@Composable
private fun AddCardCard(
    onAdd: (String, String, CardType) -> Unit,
) {
    var front by remember { mutableStateOf("") }
    var back by remember { mutableStateOf("") }
    var type by remember { mutableStateOf(CardType.Basic) }

    PremiumCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Add card", style = MaterialTheme.typography.titleMedium)
            CSNexusTextField(value = front, onValueChange = { front = it }, label = "Front")
            CSNexusTextField(value = back, onValueChange = { back = it }, label = "Back", singleLine = false)
            RowWrap {
                CardType.entries.forEach { option ->
                    CSNexusChip(
                        text = option.label,
                        selected = option == type,
                        onClick = { type = option },
                    )
                }
            }
            CSNexusButton(
                text = "Add card",
                onClick = { onAdd(front.trim(), back.trim(), type) },
                enabled = front.isNotBlank() && back.isNotBlank(),
                modifier = Modifier.fillMaxWidth(),
            )
        }
    }
}

@Composable
private fun FlashcardItem(
    card: FlashcardDto,
    onDelete: () -> Unit,
    onSave: (String, String, CardType) -> Unit,
) {
    var editing by remember(card.id) { mutableStateOf(false) }
    var front by remember(card.id) { mutableStateOf(card.front) }
    var back by remember(card.id) { mutableStateOf(card.back) }
    var type by remember(card.id) { mutableStateOf(card.cardType) }

    PremiumCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            if (editing) {
                CSNexusTextField(value = front, onValueChange = { front = it }, label = "Front")
                CSNexusTextField(value = back, onValueChange = { back = it }, label = "Back", singleLine = false)
                RowWrap {
                    CardType.entries.forEach { option ->
                        CSNexusChip(
                            text = option.label,
                            selected = option == type,
                            onClick = { type = option },
                        )
                    }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    CSNexusButton(
                        text = "Save",
                        onClick = {
                            onSave(front.trim(), back.trim(), type)
                            editing = false
                        },
                        modifier = Modifier.weight(1f),
                    )
                    CSNexusButton(
                        text = "Cancel",
                        onClick = {
                            front = card.front
                            back = card.back
                            type = card.cardType
                            editing = false
                        },
                        modifier = Modifier.weight(1f),
                        variant = CSNexusButtonVariant.Secondary,
                    )
                }
            } else {
                Text(card.front, style = MaterialTheme.typography.titleMedium)
                Text(card.back, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    CSNexusChip(text = card.cardType.label)
                    val tags = card.tags.orEmpty()
                    if (tags.isNotEmpty()) {
                        CSNexusChip(text = "${tags.size} tags")
                    }
                }
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    CSNexusButton(
                        text = "Edit",
                        onClick = { editing = true },
                        modifier = Modifier.weight(1f),
                        variant = CSNexusButtonVariant.Secondary,
                    )
                    CSNexusButton(
                        text = "Delete",
                        onClick = onDelete,
                        modifier = Modifier.weight(1f),
                        variant = CSNexusButtonVariant.Danger,
                    )
                }
            }
        }
    }
}
