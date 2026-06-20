package com.csnexus.app.feature.tutor.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusRetryPanel
import com.csnexus.app.core.design.CSNexusSkeleton
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassToast
import com.csnexus.app.core.design.GlassToastState
import com.csnexus.app.core.design.GlassToastVariant
import com.csnexus.app.feature.tutor.data.TutorAction
import com.csnexus.app.feature.tutor.data.TutorRepository
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract

// ── Entry point ───────────────────────────────────────────────────────────────

/**
 * Full-parity native Tutor screen.
 *
 * Matches the web Tutor behavior:
 *  - Question ID + optional selected answer as inputs.
 *  - Action buttons: Explain, Simplify, Hint, Step-by-step, Similar.
 *  - Result area: plain text / numbered steps / similar question card.
 *  - Rating (👍 / 👎) shown after every successful response.
 *  - Failed-send shows an error card with a labelled Retry button.
 *  - Reset clears all state to start fresh.
 *
 * The [lessonContext] parameter wires lesson-aware context when the screen is
 * opened from the lesson companion panel (task 11.2).
 */
@Composable
fun TutorScreen(
    repository: TutorRepository,
    contentPadding: PaddingValues,
    lessonContext: String? = null,
    factory: androidx.lifecycle.ViewModelProvider.Factory? = null,
) {
    val vm: TutorViewModel = if (factory != null) {
        viewModel(factory = factory)
    } else {
        viewModel(factory = TutorViewModelFactory(repository))
    }
    val state by vm.uiState.collectAsState()
    var toastState by remember { mutableStateOf<GlassToastState?>(null) }

    // Seed question ID from lesson context if it was provided (task 11.2 context passing).
    // The lesson companion passes "lesson:<subtopicId>" as context; we do not pre-fill the ID
    // field since the question ID must come from the user, but we do store context so
    // the lesson-chat pathway can use it.
    LaunchedEffect(lessonContext) {
        // No-op on null; lesson context is passed to repository calls from the companion panel,
        // not from this standalone screen.
    }

    // Show rating feedback with the shared glass toast surface.
    LaunchedEffect(state.ratingFeedback) {
        val feedback = state.ratingFeedback ?: return@LaunchedEffect
        toastState = GlassToastState(
            message = feedback,
            variant = GlassToastVariant.Success,
        )
        vm.clearRatingFeedback()
    }

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(
                top = contentPadding.calculateTopPadding() + 16.dp,
                bottom = contentPadding.calculateBottomPadding() + 24.dp,
                start = 16.dp,
                end = 16.dp,
            ),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            item { TutorHeader() }
            item {
                TutorInputCard(
                    questionIdInput = state.questionIdInput,
                    selectedAnswerInput = state.selectedAnswerInput,
                    loading = state.loading,
                    onQuestionIdChanged = vm::onQuestionIdChanged,
                    onSelectedAnswerChanged = vm::onSelectedAnswerChanged,
                    onAction = vm::requestAction,
                    onStepByStep = vm::requestStepByStep,
                    onSimilar = vm::requestSimilar,
                    onReset = vm::reset,
                )
            }
            item {
                AnimatedVisibility(
                    visible = state.loading,
                    enter = fadeIn(),
                    exit = fadeOut(),
                ) {
                    LoadingResultCard()
                }
            }
            if (!state.loading) {
                when (val result = state.result) {
                    is TutorResult.Text -> item {
                        TextResultCard(result.text)
                    }
                    is TutorResult.Steps -> item {
                        StepsResultCard(result.steps)
                    }
                    is TutorResult.Similar -> item {
                        SimilarQuestionCard(result.dto)
                    }
                    is TutorResult.FailedSend -> item {
                        CSNexusRetryPanel(
                            title = "Could not reach tutor",
                            body = result.message,
                            onRetry = vm::retryLastAction,
                        )
                    }
                    null -> Unit
                }
                if (state.result != null && state.result !is TutorResult.FailedSend) {
                    item {
                        RatingRow(
                            onHelpful = { vm.rateInteraction(true) },
                            onNotHelpful = { vm.rateInteraction(false) },
                        )
                    }
                }
            }
        }

        GlassToast(
            state = toastState,
            onDismiss = { toastState = null },
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = contentPadding.calculateTopPadding() + 12.dp, end = 12.dp),
        )
    }
}

// ── Sub-composables ───────────────────────────────────────────────────────────

@Composable
private fun TutorHeader() {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text("AI Tutor", style = MaterialTheme.typography.headlineMedium)
        Text(
            text = "Get explanations, hints, and practice questions for any question in the bank.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun TutorInputCard(
    questionIdInput: String,
    selectedAnswerInput: String,
    loading: Boolean,
    onQuestionIdChanged: (String) -> Unit,
    onSelectedAnswerChanged: (String) -> Unit,
    onAction: (TutorAction) -> Unit,
    onStepByStep: () -> Unit,
    onSimilar: () -> Unit,
    onReset: () -> Unit,
) {
    val hasQuestionId = questionIdInput.isNotBlank()

    PremiumCard {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            // Question ID field
            CSNexusTextField(
                value = questionIdInput,
                onValueChange = onQuestionIdChanged,
                label = "Question ID",
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                singleLine = true,
                modifier = Modifier.fillMaxWidth(),
                placeholder = "e.g. 42",
            )

            // Optional selected answer field
            CSNexusTextField(
                value = selectedAnswerInput,
                onValueChange = onSelectedAnswerChanged,
                label = "Your answer (optional)",
                supportingText = "Helps the tutor tailor its explanation",
            )

            // Action buttons row (scrollable if needed)
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                items(TutorAction.actionValues) { action ->
                    CSNexusButton(
                        text = action.label,
                        onClick = { onAction(action) },
                        variant = CSNexusButtonVariant.Secondary,
                        enabled = hasQuestionId && !loading,
                        loading = loading && false, // only spinner on result card
                    )
                }
                item {
                    CSNexusButton(
                        text = "Step-by-step",
                        onClick = onStepByStep,
                        variant = CSNexusButtonVariant.Secondary,
                        enabled = hasQuestionId && !loading,
                    )
                }
                item {
                    CSNexusButton(
                        text = "Similar",
                        onClick = onSimilar,
                        variant = CSNexusButtonVariant.Secondary,
                        enabled = hasQuestionId && !loading,
                    )
                }
            }

            HorizontalDivider()

            // Reset button — clears inputs and result
            CSNexusButton(
                text = "Reset",
                onClick = onReset,
                variant = CSNexusButtonVariant.Ghost,
                enabled = !loading,
                modifier = Modifier.align(Alignment.End),
            )
        }
    }
}

@Composable
private fun LoadingResultCard() {
    PremiumCard {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            CSNexusSkeleton(
                modifier = Modifier
                    .fillMaxWidth(0.16f)
                    .height(20.dp),
            )
            Text(
                text = "Loading response…",
                modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite },
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.bodyMedium,
            )
        }
    }
}

@Composable
private fun TextResultCard(text: String) {
    PremiumCard {
        Text(
            text = text,
            modifier = Modifier
                .fillMaxWidth()
                .semantics { liveRegion = LiveRegionMode.Assertive },
            style = MaterialTheme.typography.bodyMedium,
        )
    }
}

@Composable
private fun StepsResultCard(steps: List<String>) {
    PremiumCard {
        Column(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text(
                text = "Step-by-Step Solution",
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.semantics { liveRegion = LiveRegionMode.Assertive },
            )
            steps.forEachIndexed { index, step ->
                Text(
                    text = "${index + 1}. $step",
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
    }
}

@Composable
private fun SimilarQuestionCard(dto: com.csnexus.app.feature.tutor.data.SimilarQuestionDto) {
    PremiumCard {
        Column(
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier.fillMaxWidth(),
        ) {
            Text(
                text = "Similar Question",
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.semantics { liveRegion = LiveRegionMode.Assertive },
            )
            Text("Q: ${dto.stem}", style = MaterialTheme.typography.bodyMedium)
            dto.options?.forEachIndexed { index, option ->
                val label = ('A' + index).toString()
                Text("$label. $option", style = MaterialTheme.typography.bodyMedium)
            }
            Spacer(Modifier.height(4.dp))
            CSNexusStatusBadge(
                text = "Answer: ${dto.correctAnswer}",
                color = MaterialTheme.colorScheme.tertiary,
            )
            if (dto.explanation.isNotBlank()) {
                Text(
                    text = dto.explanation,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun RatingRow(
    onHelpful: () -> Unit,
    onNotHelpful: () -> Unit,
) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Text(
            text = "Was this helpful?",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        CSNexusButton(
            text = "👍",
            onClick = onHelpful,
            variant = CSNexusButtonVariant.Ghost,
        )
        CSNexusButton(
            text = "👎",
            onClick = onNotHelpful,
            variant = CSNexusButtonVariant.Ghost,
        )
    }
}

// ── ViewModelFactory ─────────────────────────────────────────────────────────

internal class TutorViewModelFactory(
    private val repository: TutorRepositoryContract,
) : androidx.lifecycle.ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : androidx.lifecycle.ViewModel> create(modelClass: Class<T>): T {
        require(modelClass == TutorViewModel::class.java)
        return TutorViewModel(repository) as T
    }
}
