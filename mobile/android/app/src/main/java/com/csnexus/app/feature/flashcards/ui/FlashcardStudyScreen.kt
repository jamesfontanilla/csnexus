package com.csnexus.app.feature.flashcards.ui

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
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
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusOfflineBanner
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.ConfidenceLevel
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.FlashcardResponseResult
import com.csnexus.app.feature.flashcards.data.FlashcardStudyMode
import com.csnexus.app.feature.flashcards.data.ResponseType
import com.csnexus.app.feature.flashcards.data.SessionCardDto
import com.csnexus.app.feature.flashcards.data.SessionSummaryDto
import kotlinx.coroutines.launch

private enum class StudyPhase {
    Loading,
    Studying,
    Summary,
    Error,
}

@Composable
fun FlashcardStudyScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
    deckIds: List<Int>,
    initialMode: FlashcardStudyMode?,
    onBack: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var phase by remember { mutableStateOf(StudyPhase.Loading) }
    var sessionId by remember { mutableIntStateOf(0) }
    var cards by remember { mutableStateOf<List<SessionCardDto>>(emptyList()) }
    var currentIndex by remember { mutableIntStateOf(0) }
    var revealed by remember { mutableStateOf(false) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var statusMessage by remember { mutableStateOf<String?>(null) }
    var summary by remember { mutableStateOf<SessionSummaryDto?>(null) }
    var studyMode by remember { mutableStateOf(initialMode ?: FlashcardStudyMode.Swipe) }
    var typedAnswer by remember { mutableStateOf("") }
    var typingResult by remember { mutableStateOf<Pair<Boolean, String>?>(null) }
    var progress by remember { mutableStateOf(StudyProgressSnapshot()) }
    var responding by remember { mutableStateOf(false) }
    var pendingSyncCount by remember { mutableIntStateOf(0) }

    suspend fun startSession(mode: FlashcardStudyMode) {
        phase = StudyPhase.Loading
        errorMessage = null
        statusMessage = null

        if (deckIds.isEmpty()) {
            when (val queueResult = repository.queue()) {
                is ApiResult.Success -> {
                    if (queueResult.value.isEmpty()) {
                        errorMessage = "No cards due for review. You're all caught up."
                        phase = StudyPhase.Error
                        return
                    }
                }
                is ApiResult.Failure -> {
                    // Keep going. The server may still create a queue-backed session.
                }
            }
        }

        when (val sessionResult = repository.createSession(deckIds = deckIds, studyMode = mode)) {
            is ApiResult.Success -> {
                sessionId = sessionResult.value.id
                when (val cardsResult = repository.sessionCards(sessionId)) {
                    is ApiResult.Success -> {
                        if (cardsResult.value.isEmpty()) {
                            errorMessage = "No cards available for this study session."
                            phase = StudyPhase.Error
                        } else {
                            cards = cardsResult.value
                            currentIndex = 0
                            revealed = false
                            typedAnswer = ""
                            typingResult = null
                            progress = StudyProgressSnapshot()
                            phase = StudyPhase.Studying
                        }
                    }
                    is ApiResult.Failure -> {
                        errorMessage = "Could not load session cards."
                        phase = StudyPhase.Error
                    }
                }
            }
            is ApiResult.Failure -> {
                errorMessage = "Failed to start study session."
                phase = StudyPhase.Error
            }
        }
    }

    suspend fun respond(responseType: ResponseType, confidence: ConfidenceLevel) {
        if (responding) return
        val card = cards.getOrNull(currentIndex) ?: return
        responding = true
        when (val result = repository.respondToCard(sessionId, card.cardId, responseType, confidence)) {
            is ApiResult.Success -> {
                progress = progress.afterResponse(responseType)
                statusMessage = when (val syncState = result.value) {
                    FlashcardResponseResult.Synced -> "Response saved."
                    is FlashcardResponseResult.QueuedOffline -> {
                        pendingSyncCount = syncState.pendingCount
                        "Offline. Response queued (${syncState.pendingCount} pending)."
                    }
                }
                val nextIndex = currentIndex + 1
                if (nextIndex >= cards.size) {
                    when (val endResult = repository.endSession(sessionId)) {
                        is ApiResult.Success -> {
                            summary = endResult.value
                            phase = StudyPhase.Summary
                        }
                        is ApiResult.Failure -> {
                            summary = SessionSummaryDto(
                                cardsReviewed = progress.reviewed,
                                cardsCorrect = progress.correct,
                                xpEarned = 0,
                                durationSeconds = progress.reviewed * 20,
                            )
                            statusMessage = "Offline. Session summary is local until the server can finalize it."
                            phase = StudyPhase.Summary
                        }
                    }
                } else {
                    currentIndex = nextIndex
                    revealed = false
                    typedAnswer = ""
                    typingResult = null
                }
            }
            is ApiResult.Failure -> errorMessage = "Could not record your response."
        }
        responding = false
    }

    LaunchedEffect(deckIds, initialMode) {
        studyMode = initialMode ?: FlashcardStudyMode.Swipe
        pendingSyncCount = repository.pendingSyncCount()
        startSession(studyMode)
    }

    when (phase) {
        StudyPhase.Loading -> LoadingState(label = "Starting study session")
        StudyPhase.Error -> {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text(errorMessage ?: "Could not start study session.", color = MaterialTheme.colorScheme.error)
                CSNexusButton(text = "Back to Flashcards", onClick = onBack)
            }
        }
        StudyPhase.Summary -> {
            val sessionSummary = summary
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text("Study Summary", style = MaterialTheme.typography.headlineMedium)
                if (statusMessage != null) {
                    CSNexusOfflineBanner(message = statusMessage!!)
                }
                sessionSummary?.let {
                    PremiumCard {
                        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("${it.cardsReviewed} cards reviewed", style = MaterialTheme.typography.titleLarge)
                            Text("${it.cardsCorrect} correct • ${it.xpEarned} XP", color = MaterialTheme.colorScheme.onSurfaceVariant)
                            Text(
                                "Duration: ${formatFlashcardDuration(it.durationSeconds)}",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
                CSNexusButton(text = "Back to Flashcards", onClick = onBack, modifier = Modifier.fillMaxWidth())
            }
        }
        StudyPhase.Studying -> {
            val card = cards.getOrNull(currentIndex) ?: return
            val total = cards.size.coerceAtLeast(1)
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp),
            ) {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CSNexusStatusBadge(text = studyMode.label)
                CSNexusStatusBadge(text = "${currentIndex + 1}/$total")
                    if (pendingSyncCount > 0) {
                        CSNexusStatusBadge(text = "$pendingSyncCount pending")
                    }
                }
                Text("Card ${currentIndex + 1} of $total", style = MaterialTheme.typography.headlineMedium)
                LuxuryProgressBar(
                    progress = (currentIndex + 1).toFloat() / total.toFloat(),
                    modifier = Modifier.fillMaxWidth(),
                )
                if (statusMessage != null && statusMessage!!.contains("Offline")) {
                    CSNexusOfflineBanner(message = statusMessage!!)
                } else if (statusMessage != null) {
                    Text(statusMessage!!, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                if (errorMessage != null) {
                    Text(errorMessage!!, color = MaterialTheme.colorScheme.error)
                }
                FlashcardFaceCard(
                    front = card.front,
                    back = card.back,
                    revealed = revealed || studyMode == FlashcardStudyMode.Typing,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                )
                if (studyMode == FlashcardStudyMode.Typing) {
                    CSNexusTextField(
                        value = typedAnswer,
                        onValueChange = { typedAnswer = it },
                        label = "Your answer",
                        singleLine = false,
                    )
                    if (typingResult == null) {
                        CSNexusButton(
                            text = "Check Answer",
                            onClick = {
                                val similarity = flashcardSimilarity(typedAnswer, card.back)
                                typingResult = (similarity >= 0.8) to card.back
                            },
                            enabled = typedAnswer.isNotBlank(),
                            modifier = Modifier.fillMaxWidth(),
                        )
                    } else {
                        val isCorrect = typingResult!!.first
                        val similarity = flashcardSimilarity(typedAnswer, card.back)
                        PremiumCard {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text(
                                    if (isCorrect) "Close enough" else "Needs another look",
                                    style = MaterialTheme.typography.titleMedium,
                                    color = if (isCorrect) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
                                )
                                Text("Correct answer: ${typingResult!!.second}")
                                Text("Similarity score: ${(similarity * 100).toInt()}%")
                            }
                        }
                        val choice = confidenceChoiceForSimilarity(similarity, isCorrect)
                        CSNexusButton(
                            text = "Continue",
                            onClick = { scope.launch { respond(choice.responseType, choice.confidence) } },
                            loading = responding,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }
                } else {
                    if (!revealed) {
                        CSNexusButton(
                            text = "Reveal Answer",
                            onClick = { revealed = true },
                            modifier = Modifier.fillMaxWidth(),
                        )
                    } else {
                        ConfidenceButtonGrid(
                            responding = responding,
                            onRespond = { responseType, confidence ->
                                scope.launch { respond(responseType, confidence) }
                            },
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun FlashcardFaceCard(
    front: String,
    back: String,
    revealed: Boolean,
    modifier: Modifier = Modifier,
) {
    val reducedMotion = rememberCSNexusReducedMotion()
    val fadeDuration = if (reducedMotion) 80 else 220
    val crossfadeDuration = if (reducedMotion) 80 else 180
    PremiumCard(modifier = modifier) {
        AnimatedContent(
            targetState = revealed,
            transitionSpec = {
                fadeIn(tween(fadeDuration)) togetherWith fadeOut(tween(crossfadeDuration))
            },
            label = "flashcard-face",
        ) { showingBack ->
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .heightIn(min = 260.dp),
                verticalArrangement = Arrangement.Center,
            ) {
                Text(
                    if (showingBack) "Answer" else "Prompt",
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.SemiBold,
                )
                Crossfade(
                    targetState = showingBack,
                    animationSpec = tween(crossfadeDuration),
                    label = "flashcard-copy",
                ) { showBack ->
                    Text(
                        text = if (showBack) back else front,
                        style = MaterialTheme.typography.headlineSmall,
                        modifier = Modifier.padding(top = 12.dp),
                    )
                }
            }
        }
    }
}

@Composable
private fun ConfidenceButtonGrid(
    responding: Boolean,
    onRespond: (ResponseType, ConfidenceLevel) -> Unit,
) {
    val options = listOf(
        ResponseType.Forgot to ConfidenceLevel.Guessed,
        ResponseType.Remembered to ConfidenceLevel.Unsure,
        ResponseType.Remembered to ConfidenceLevel.Confident,
        ResponseType.Remembered to ConfidenceLevel.Mastered,
    )
    RowWrap {
        options.forEach { (responseType, confidence) ->
            CSNexusButton(
                text = confidence.label,
                onClick = { onRespond(responseType, confidence) },
                loading = responding,
                variant = when (confidence) {
                    ConfidenceLevel.Guessed -> CSNexusButtonVariant.Danger
                    ConfidenceLevel.Unsure -> CSNexusButtonVariant.Secondary
                    ConfidenceLevel.Confident -> CSNexusButtonVariant.Primary
                    ConfidenceLevel.Mastered -> CSNexusButtonVariant.Ghost
                },
            )
        }
    }
}
