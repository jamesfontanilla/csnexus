package com.csnexus.app.feature.tutor.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.GlassToast
import com.csnexus.app.core.design.GlassToastState
import com.csnexus.app.core.design.GlassToastVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun TutorScreen(
    repository: TutorRepositoryContract,
    contentRepository: ContentRepository,
    contentPadding: PaddingValues,
    factory: androidx.lifecycle.ViewModelProvider.Factory? = null,
) {
    val vm: TutorViewModel = if (factory != null) {
        viewModel(factory = factory)
    } else {
        viewModel(factory = TutorViewModelFactory(repository, contentRepository))
    }
    val state by vm.uiState.collectAsState()
    var toastState by remember { mutableStateOf<GlassToastState?>(null) }
    val listState = rememberLazyListState()
    val keyboardController = LocalSoftwareKeyboardController.current

    LaunchedEffect(state.messages.size) {
        if (state.messages.isNotEmpty()) {
            listState.animateScrollToItem(state.messages.lastIndex)
        }
    }

    LaunchedEffect(state.ratingFeedback) {
        val feedback = state.ratingFeedback ?: return@LaunchedEffect
        toastState = GlassToastState(
            message = feedback,
            variant = GlassToastVariant.Success,
        )
        vm.clearRatingFeedback()
    }

    BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
        val compactLayout = maxWidth < 600.dp
        val horizontalPadding = if (compactLayout) 12.dp else 16.dp
        val verticalPadding = if (compactLayout) 12.dp else 16.dp
        val sectionGap = if (compactLayout) 12.dp else 16.dp

        Box(modifier = Modifier.fillMaxSize()) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(contentPadding)
                    .padding(horizontal = horizontalPadding, vertical = verticalPadding),
                verticalArrangement = Arrangement.spacedBy(sectionGap),
            ) {
                TutorHeader(
                    onNewChat = vm::resetConversation,
                    showNewChat = state.selectedSubtopicId != null && state.messages.isNotEmpty(),
                )

                TutorContextCard(
                    state = state,
                    onModuleSelected = vm::onModuleSelected,
                    onTopicSelected = vm::onTopicSelected,
                    onSubtopicSelected = vm::onSubtopicSelected,
                )

                if (!compactLayout) {
                    QuickPromptCard(
                        enabled = state.selectedSubtopicId != null && !state.sending,
                        onPrompt = vm::sendPrompt,
                    )
                }

                PremiumCard(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                ) {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        verticalArrangement = Arrangement.spacedBy(if (compactLayout) 10.dp else 12.dp),
                    ) {
                        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text("Chat", style = MaterialTheme.typography.titleMedium)
                            val title = remember(state) {
                                buildString {
                                    append(state.modules.firstOrNull { it.id == state.selectedModuleId }?.title ?: "Module")
                                    append(" / ")
                                    append(state.topics.firstOrNull { it.id == state.selectedTopicId }?.title ?: "Topic")
                                    append(" / ")
                                    append(state.subtopics.firstOrNull { it.id == state.selectedSubtopicId }?.title ?: "Subtopic")
                                }
                            }
                            Text(
                                text = title,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }

                        if (state.errorMessage != null) {
                            Text(
                                text = state.errorMessage.orEmpty(),
                                color = MaterialTheme.colorScheme.error,
                                style = MaterialTheme.typography.bodySmall,
                            )
                        }

                        if (state.messages.isEmpty()) {
                            CompactTutorPromptStrip(
                                enabled = state.selectedSubtopicId != null && !state.sending,
                                onPrompt = vm::sendPrompt,
                                maxItems = if (compactLayout) 4 else 5,
                            )
                        }

                        LazyColumn(
                            state = listState,
                            modifier = Modifier
                                .fillMaxWidth()
                                .weight(1f),
                            verticalArrangement = Arrangement.spacedBy(10.dp),
                            contentPadding = PaddingValues(vertical = 4.dp),
                        ) {
                            items(state.messages) { message ->
                                TutorBubble(message = message)
                            }
                            if (state.sending) {
                                item {
                                    ChatTypingBubble()
                                }
                            }
                        }

                        if (state.lastInteractionId != null && !state.sending && state.messages.lastOrNull()?.role == TutorChatRole.Assistant && !state.messages.lastOrNull()!!.isError) {
                            RatingRow(
                                onHelpful = { vm.rateInteraction(true) },
                                onNotHelpful = { vm.rateInteraction(false) },
                            )
                        }

                        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            CSNexusTextField(
                                value = state.input,
                                onValueChange = vm::onInputChanged,
                                label = "Message",
                                singleLine = false,
                                supportingText = if (state.selectedSubtopicId == null) "Select a subtopic first." else null,
                                modifier = Modifier.fillMaxWidth(),
                                keyboardOptions = KeyboardOptions.Default,
                                placeholder = "Ask anything about this subtopic",
                            )
                            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                CSNexusButton(
                                    text = "Send",
                                    onClick = {
                                        vm.sendMessage()
                                        keyboardController?.hide()
                                    },
                                    enabled = state.selectedSubtopicId != null && state.input.isNotBlank() && !state.sending,
                                    loading = state.sending,
                                    modifier = Modifier.weight(1f),
                                )
                            }
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
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun TutorContextCard(
    state: TutorUiState,
    onModuleSelected: (String) -> Unit,
    onTopicSelected: (String) -> Unit,
    onSubtopicSelected: (String) -> Unit,
) {
    PremiumCard(modifier = Modifier.fillMaxWidth()) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Context", style = MaterialTheme.typography.titleMedium)
            TutorDropdownField(
                label = "Module",
                value = state.modules.firstOrNull { it.id == state.selectedModuleId }?.title ?: "Choose module",
                options = state.modules.map { SelectionOption(it.id, it.title) },
                enabled = !state.modulesLoading && state.modules.isNotEmpty(),
                onSelected = { onModuleSelected(it.value.toString()) },
            )
            TutorDropdownField(
                label = "Topic",
                value = state.topics.firstOrNull { it.id == state.selectedTopicId }?.title ?: "Choose topic",
                options = state.topics.map { SelectionOption(it.id, it.title) },
                enabled = !state.topicsLoading && state.selectedModuleId != null && state.topics.isNotEmpty(),
                onSelected = { onTopicSelected(it.value.toString()) },
            )
            TutorDropdownField(
                label = "Subtopic",
                value = state.subtopics.firstOrNull { it.id == state.selectedSubtopicId }?.title ?: "Choose subtopic",
                options = state.subtopics.map { SelectionOption(it.id, it.title) },
                enabled = !state.subtopicsLoading && state.selectedTopicId != null && state.subtopics.isNotEmpty(),
                onSelected = { onSubtopicSelected(it.value.toString()) },
            )
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun QuickPromptCard(
    enabled: Boolean,
    onPrompt: (String) -> Unit,
) {
    val prompts = listOf(
        "Summarize this lesson",
        "Explain it simpler",
        "Give me an example",
        "Quiz me on this topic",
        "What should I remember?",
    )

    PremiumCard(modifier = Modifier.fillMaxWidth()) {
        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Quick prompts", style = MaterialTheme.typography.titleMedium)
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                prompts.forEachIndexed { index, prompt ->
                    CSNexusButton(
                        text = prompt,
                        onClick = { onPrompt(prompt) },
                        variant = if (index < 3) CSNexusButtonVariant.Secondary else CSNexusButtonVariant.Ghost,
                        enabled = enabled,
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun CompactTutorPromptStrip(
    enabled: Boolean,
    onPrompt: (String) -> Unit,
    maxItems: Int,
) {
    val prompts = listOf(
        "Summarize this lesson",
        "Explain it simpler",
        "Give me an example",
        "Quiz me on this topic",
        "What should I remember?",
    )

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(
            text = "Ask about the selected subtopic.",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        FlowRow(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            prompts.take(maxItems).forEachIndexed { index, prompt ->
                CSNexusButton(
                    text = prompt,
                    onClick = { onPrompt(prompt) },
                    variant = if (index < 3) CSNexusButtonVariant.Secondary else CSNexusButtonVariant.Ghost,
                    enabled = enabled,
                )
            }
        }
    }
}

@Composable
private fun TutorHeader(
    onNewChat: () -> Unit,
    showNewChat: Boolean,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = "AI Tutor",
            style = MaterialTheme.typography.headlineMedium,
        )
        if (showNewChat) {
            CSNexusButton(
                text = "New chat",
                onClick = onNewChat,
                variant = CSNexusButtonVariant.Ghost,
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun TutorDropdownField(
    label: String,
    value: String,
    options: List<SelectionOption>,
    enabled: Boolean,
    onSelected: (SelectionOption) -> Unit,
) {
    var expanded by remember { mutableStateOf(false) }

    ExposedDropdownMenuBox(
        expanded = expanded,
        onExpandedChange = { if (enabled) expanded = !expanded },
    ) {
        OutlinedTextField(
            value = value,
            onValueChange = {},
            modifier = Modifier
                .fillMaxWidth(),
            readOnly = true,
            enabled = enabled,
            label = { Text(label) },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
        )

        ExposedDropdownMenu(
            expanded = expanded,
            onDismissRequest = { expanded = false },
        ) {
            options.forEach { option ->
                DropdownMenuItem(
                    text = { Text(option.label) },
                    onClick = {
                        expanded = false
                        onSelected(option)
                    },
                )
            }
        }
    }
}

@Composable
private fun TutorBubble(message: TutorChatMessage) {
    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = if (message.role == TutorChatRole.User) Alignment.CenterEnd else Alignment.CenterStart,
    ) {
        PremiumCard(
            modifier = Modifier.widthIn(max = 320.dp),
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = if (message.role == TutorChatRole.User) "You" else "Tutor",
                    style = MaterialTheme.typography.labelMedium,
                    color = if (message.isError) {
                        MaterialTheme.colorScheme.error
                    } else if (message.role == TutorChatRole.User) {
                        MaterialTheme.colorScheme.primary
                    } else {
                        MaterialTheme.colorScheme.secondary
                    },
                )
                Text(
                    text = message.content,
                    style = MaterialTheme.typography.bodyMedium,
                    color = if (message.isError) {
                        MaterialTheme.colorScheme.error
                    } else {
                        MaterialTheme.colorScheme.onSurface
                    },
                )
            }
        }
    }
}

@Composable
private fun ChatTypingBubble() {
    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = Alignment.CenterStart,
    ) {
        PremiumCard(
            modifier = Modifier.widthIn(max = 240.dp),
        ) {
            Text(
                text = "Thinking...",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun RatingRow(
    onHelpful: () -> Unit,
    onNotHelpful: () -> Unit,
) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
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

private data class SelectionOption(
    val value: Int,
    val label: String,
)

internal class TutorViewModelFactory(
    private val repository: TutorRepositoryContract,
    private val contentRepository: ContentRepository,
) : androidx.lifecycle.ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : androidx.lifecycle.ViewModel> create(modelClass: Class<T>): T {
        require(modelClass == TutorViewModel::class.java)
        return TutorViewModel(repository, contentRepository) as T
    }
}
