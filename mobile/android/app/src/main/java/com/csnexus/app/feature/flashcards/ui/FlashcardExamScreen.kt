package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.CSNexusTimerText
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.DeckDto
import com.csnexus.app.feature.flashcards.data.ExamCardDto
import com.csnexus.app.feature.flashcards.data.ExamResultDto
import com.csnexus.app.feature.flashcards.data.ExamSimulationDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

private enum class FlashcardExamPhase {
    Setup,
    Loading,
    Active,
    Results,
    Error,
}

@Composable
fun FlashcardExamScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
) {
    val scope = rememberCoroutineScope()
    var phase by remember { mutableStateOf(FlashcardExamPhase.Loading) }
    var decks by remember { mutableStateOf<List<DeckDto>>(emptyList()) }
    var selectedDeckIds by remember { mutableStateOf(setOf<Int>()) }
    var cardCount by remember { mutableIntStateOf(30) }
    var timeLimitMinutes by remember { mutableIntStateOf(15) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var exam by remember { mutableStateOf<ExamSimulationDto?>(null) }
    var cards by remember { mutableStateOf<List<ExamCardDto>>(emptyList()) }
    var currentIndex by remember { mutableIntStateOf(0) }
    var answer by remember { mutableStateOf("") }
    var result by remember { mutableStateOf<ExamResultDto?>(null) }
    var remainingSeconds by remember { mutableIntStateOf(0) }
    var submitting by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        when (val deckResult = repository.decks()) {
            is ApiResult.Success -> {
                decks = deckResult.value
                phase = FlashcardExamPhase.Setup
            }
            is ApiResult.Failure -> {
                errorMessage = "Could not load decks for exam simulation."
                phase = FlashcardExamPhase.Error
            }
        }
    }

    LaunchedEffect(phase, remainingSeconds) {
        if (phase == FlashcardExamPhase.Active && remainingSeconds > 0) {
            delay(1_000)
            remainingSeconds -= 1
            if (remainingSeconds == 0 && exam != null) {
                when (val complete = repository.completeExam(exam!!.id)) {
                    is ApiResult.Success -> {
                        result = complete.value
                        phase = FlashcardExamPhase.Results
                    }
                    is ApiResult.Failure -> {
                        errorMessage = "Could not finalize the exam when time expired."
                        phase = FlashcardExamPhase.Error
                    }
                }
            }
        }
    }

    when (phase) {
        FlashcardExamPhase.Loading -> LoadingState(label = "Loading exam setup")
        FlashcardExamPhase.Error -> {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text(errorMessage ?: "Something went wrong.", color = MaterialTheme.colorScheme.error)
            }
        }
        FlashcardExamPhase.Setup -> {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding),
                contentPadding = PaddingValues(20.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                item {
                    Text("Exam Simulation", style = MaterialTheme.typography.headlineMedium)
                    Text("Create a timed flashcard test from one or more decks.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                item {
                    CSNexusCard(modifier = Modifier.heightIn(min = 240.dp)) {
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Text("Select Decks", style = MaterialTheme.typography.titleMedium)
                            if (decks.isEmpty()) {
                                Text("No decks available yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                            } else {
                                RowWrap {
                                    decks.forEach { deck ->
                                        CSNexusChip(
                                            text = deck.title,
                                            selected = deck.id in selectedDeckIds,
                                            onClick = {
                                                selectedDeckIds = selectedDeckIds.toMutableSet().also { set ->
                                                    if (!set.add(deck.id)) set.remove(deck.id)
                                                }
                                            },
                                        )
                                    }
                                }
                            }
                            Text("Cards: $cardCount", style = MaterialTheme.typography.titleSmall)
                            Slider(
                                value = cardCount.toFloat(),
                                onValueChange = { cardCount = it.toInt().coerceIn(10, 50) },
                                valueRange = 10f..50f,
                                steps = 7,
                            )
                            Text("Time limit: $timeLimitMinutes minutes", style = MaterialTheme.typography.titleSmall)
                            Slider(
                                value = timeLimitMinutes.toFloat(),
                                onValueChange = { timeLimitMinutes = it.toInt().coerceIn(5, 60) },
                                valueRange = 5f..60f,
                                steps = 10,
                            )
                            CSNexusButton(
                                text = "Start Exam",
                                onClick = {
                                    scope.launch {
                                        phase = FlashcardExamPhase.Loading
                                        when (
                                            val examResult = repository.createExam(
                                                deckIds = selectedDeckIds.toList(),
                                                cardCount = cardCount,
                                                timeLimitMinutes = timeLimitMinutes,
                                            )
                                        ) {
                                            is ApiResult.Success -> {
                                                exam = examResult.value
                                                when (val cardsResult = repository.examCards(examResult.value.id)) {
                                                    is ApiResult.Success -> {
                                                        cards = cardsResult.value
                                                        currentIndex = 0
                                                        answer = ""
                                                        remainingSeconds = timeLimitMinutes * 60
                                                        phase = FlashcardExamPhase.Active
                                                    }
                                                    is ApiResult.Failure -> {
                                                        errorMessage = "Could not load exam cards."
                                                        phase = FlashcardExamPhase.Error
                                                    }
                                                }
                                            }
                                            is ApiResult.Failure -> {
                                                errorMessage = "Could not start exam simulation."
                                                phase = FlashcardExamPhase.Error
                                            }
                                        }
                                    }
                                },
                                enabled = selectedDeckIds.isNotEmpty(),
                                modifier = Modifier.fillMaxWidth(),
                            )
                        }
                    }
                }
            }
        }
        FlashcardExamPhase.Active -> {
            val examCard = cards.getOrNull(currentIndex) ?: return
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp),
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    CSNexusChip(text = "${currentIndex + 1}/${cards.size}")
                    CSNexusChip(text = "${selectedDeckIds.size} decks")
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Text("Exam Card", style = MaterialTheme.typography.headlineMedium)
                    CSNexusTimerText(text = formatExamCountdown(remainingSeconds), urgent = remainingSeconds in 1..299)
                }
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(examCard.front, style = MaterialTheme.typography.titleLarge)
                        Text("Type the answer you would recall under pressure.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                CSNexusTextField(
                    value = answer,
                    onValueChange = { answer = it },
                    label = "Your answer",
                    singleLine = false,
                )
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    CSNexusButton(
                        text = if (currentIndex == cards.lastIndex) "Submit final answer" else "Save and next",
                        onClick = {
                            scope.launch {
                                submitting = true
                                val cardId = examCard.cardId
                                when (repository.answerExamCard(exam!!.id, cardId, answer.trim())) {
                                    is ApiResult.Success -> {
                                        if (currentIndex == cards.lastIndex) {
                                            when (val complete = repository.completeExam(exam!!.id)) {
                                                is ApiResult.Success -> {
                                                    result = complete.value
                                                    phase = FlashcardExamPhase.Results
                                                }
                                                is ApiResult.Failure -> {
                                                    errorMessage = "Could not score this exam."
                                                    phase = FlashcardExamPhase.Error
                                                }
                                            }
                                        } else {
                                            currentIndex += 1
                                            answer = ""
                                        }
                                    }
                                    is ApiResult.Failure -> {
                                        errorMessage = "Could not submit this answer."
                                        phase = FlashcardExamPhase.Error
                                    }
                                }
                                submitting = false
                            }
                        },
                        loading = submitting,
                        enabled = answer.isNotBlank(),
                        modifier = Modifier.weight(1f),
                    )
                    CSNexusButton(
                        text = "Finish now",
                        onClick = {
                            scope.launch {
                                when (val complete = repository.completeExam(exam!!.id)) {
                                    is ApiResult.Success -> {
                                        result = complete.value
                                        phase = FlashcardExamPhase.Results
                                    }
                                    is ApiResult.Failure -> {
                                        errorMessage = "Could not finalize the exam."
                                        phase = FlashcardExamPhase.Error
                                    }
                                }
                            }
                        },
                        modifier = Modifier.weight(1f),
                        variant = CSNexusButtonVariant.Secondary,
                    )
                }
            }
        }
        FlashcardExamPhase.Results -> {
            val examResult = result ?: return
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text("Exam Results", style = MaterialTheme.typography.headlineMedium)
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("${examResult.score}/${examResult.total}", style = MaterialTheme.typography.headlineLarge)
                        Text("${examResult.percentage.toInt()}% • ${examResult.xpEarned} XP", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Text("Time taken: ${formatFlashcardDuration(examResult.timeTakenSeconds)}", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                Text(
                    "The current backend returns a scored summary for exam simulation. Per-card review will deepen when the server exposes it.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

private fun formatExamCountdown(seconds: Int): String {
    val minutes = seconds / 60
    val remainingSeconds = seconds % 60
    return "$minutes:${remainingSeconds.toString().padStart(2, '0')}"
}
