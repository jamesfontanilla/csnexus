package com.csnexus.app.feature.tutor.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.tutor.data.LessonChatHistoryItemDto
import com.csnexus.app.feature.tutor.data.LessonChatResponseDto
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract
import kotlinx.coroutines.launch
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.intOrNull
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlinx.serialization.json.contentOrNull
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

data class TutorChatMessage(
    val role: TutorChatRole,
    val content: String,
    val isError: Boolean = false,
)

enum class TutorChatRole(val wireValue: String) {
    User("user"),
    Assistant("assistant"),
}

data class TutorUiState(
    val modules: List<LearningModule> = emptyList(),
    val topics: List<LearningTopic> = emptyList(),
    val subtopics: List<LearningSubtopic> = emptyList(),
    val selectedModuleId: Int? = null,
    val selectedTopicId: Int? = null,
    val selectedSubtopicId: Int? = null,
    val modulesLoading: Boolean = true,
    val topicsLoading: Boolean = false,
    val subtopicsLoading: Boolean = false,
    val messages: List<TutorChatMessage> = emptyList(),
    val input: String = "",
    val sending: Boolean = false,
    val chatContext: JsonElement? = null,
    val lastInteractionId: Int? = null,
    val ratingFeedback: String? = null,
    val errorMessage: String? = null,
)

class TutorViewModel(
    private val tutorRepository: TutorRepositoryContract,
    private val contentRepository: ContentRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(TutorUiState())
    val uiState: StateFlow<TutorUiState> = _uiState.asStateFlow()

    init {
        loadModules()
    }

    fun onModuleSelected(value: String) {
        val moduleId = value.toIntOrNull()
        if (moduleId == null) {
            _uiState.update {
                it.copy(
                    selectedModuleId = null,
                    selectedTopicId = null,
                    selectedSubtopicId = null,
                    topics = emptyList(),
                    subtopics = emptyList(),
                    messages = emptyList(),
                    input = "",
                    chatContext = null,
                    lastInteractionId = null,
                    ratingFeedback = null,
                    errorMessage = null,
                )
            }
            return
        }

        _uiState.update {
            it.copy(
                selectedModuleId = moduleId,
                selectedTopicId = null,
                selectedSubtopicId = null,
                topics = emptyList(),
                subtopics = emptyList(),
                messages = emptyList(),
                input = "",
                chatContext = null,
                lastInteractionId = null,
                ratingFeedback = null,
                errorMessage = null,
            )
        }
        loadTopics(moduleId)
    }

    fun onTopicSelected(value: String) {
        val topicId = value.toIntOrNull()
        if (topicId == null) {
            _uiState.update {
                it.copy(
                    selectedTopicId = null,
                    selectedSubtopicId = null,
                    subtopics = emptyList(),
                    messages = emptyList(),
                    input = "",
                    chatContext = null,
                    lastInteractionId = null,
                    ratingFeedback = null,
                    errorMessage = null,
                )
            }
            return
        }

        _uiState.update {
            it.copy(
                selectedTopicId = topicId,
                selectedSubtopicId = null,
                subtopics = emptyList(),
                messages = emptyList(),
                input = "",
                chatContext = null,
                lastInteractionId = null,
                ratingFeedback = null,
                errorMessage = null,
            )
        }
        loadSubtopics(topicId)
    }

    fun onSubtopicSelected(value: String) {
        val subtopicId = value.toIntOrNull()
        _uiState.update {
            it.copy(
                selectedSubtopicId = subtopicId,
                messages = emptyList(),
                input = "",
                chatContext = null,
                lastInteractionId = null,
                ratingFeedback = null,
                errorMessage = null,
            )
        }
    }

    fun onInputChanged(value: String) {
        _uiState.update { it.copy(input = value, errorMessage = null) }
    }

    fun sendPrompt(prompt: String) {
        sendMessage(prompt)
    }

    fun sendMessage(messageOverride: String? = null) {
        val current = _uiState.value
        val subtopicId = current.selectedSubtopicId ?: run {
            _uiState.update { it.copy(errorMessage = "Select a subtopic first.") }
            return
        }
        if (current.sending) return

        val message = (messageOverride ?: current.input).trim()
        if (message.isBlank()) return

        val nextMessages = current.messages + TutorChatMessage(
            role = TutorChatRole.User,
            content = message,
        )
        val history = current.messages.takeLast(10).map {
            LessonChatHistoryItemDto(role = it.role.wireValue, content = it.content)
        }

        _uiState.update {
            it.copy(
                messages = nextMessages,
                input = if (messageOverride == null) "" else it.input,
                sending = true,
                errorMessage = null,
            )
        }

        viewModelScope.launch {
            when (
                val result = tutorRepository.lessonChat(
                    message = message,
                    contextJson = current.chatContext,
                    subtopicId = subtopicId,
                    activeSectionIndex = null,
                    history = history,
                )
            ) {
                is ApiResult.Success -> {
                    val response = result.value
                    val assistantText = response.resolvedText().ifBlank {
                        "Sorry, I couldn't answer that right now."
                    }
                    _uiState.update {
                        it.copy(
                            messages = it.messages + TutorChatMessage(
                                role = TutorChatRole.Assistant,
                                content = assistantText,
                            ),
                            sending = false,
                            lastInteractionId = response.interactionId.takeIf { id -> id != 0 },
                            chatContext = response.contextJson ?: it.chatContext,
                        )
                    }
                }
                is ApiResult.Failure -> {
                    _uiState.update {
                        it.copy(
                            messages = it.messages + TutorChatMessage(
                                role = TutorChatRole.Assistant,
                                content = result.error.userMessage(),
                                isError = true,
                            ),
                            sending = false,
                            lastInteractionId = null,
                            errorMessage = "Could not reach the tutor.",
                        )
                    }
                }
            }
        }
    }

    fun rateInteraction(helpful: Boolean) {
        val interactionId = _uiState.value.lastInteractionId ?: return
        viewModelScope.launch {
            when (tutorRepository.rateInteraction(interactionId, helpful)) {
                is ApiResult.Success -> {
                    _uiState.update {
                        it.copy(
                            ratingFeedback = if (helpful) "Thanks for the thumbs up." else "Thanks, we will use that feedback.",
                        )
                    }
                }
                is ApiResult.Failure -> Unit
            }
        }
    }

    fun clearRatingFeedback() {
        _uiState.update { it.copy(ratingFeedback = null) }
    }

    fun resetConversation() {
        _uiState.update {
            it.copy(
                messages = emptyList(),
                input = "",
                sending = false,
                chatContext = null,
                lastInteractionId = null,
                ratingFeedback = null,
                errorMessage = null,
            )
        }
    }

    private fun loadModules() {
        viewModelScope.launch {
            when (val result = contentRepository.modules()) {
                is ApiResult.Success -> {
                    val modules = result.value.value
                    _uiState.update {
                        it.copy(
                            modules = modules,
                            modulesLoading = false,
                            errorMessage = null,
                        )
                    }
                    if (modules.isNotEmpty()) {
                        onModuleSelected(modules.first().id.toString())
                    }
                }
                is ApiResult.Failure -> {
                    _uiState.update {
                        it.copy(
                            modulesLoading = false,
                            errorMessage = result.error.userMessage(),
                        )
                    }
                }
            }
        }
    }

    private fun loadTopics(moduleId: Int) {
        _uiState.update { it.copy(topicsLoading = true) }
        viewModelScope.launch {
            when (val result = contentRepository.topics(moduleId)) {
                is ApiResult.Success -> {
                    val topics = result.value.value
                    if (_uiState.value.selectedModuleId != moduleId) return@launch
                    val selectedTopicId = topics.firstOrNull()?.id
                    _uiState.update {
                        it.copy(
                            topics = topics,
                            topicsLoading = false,
                            selectedTopicId = selectedTopicId,
                            errorMessage = null,
                        )
                    }
                    if (selectedTopicId != null) {
                        loadSubtopics(selectedTopicId)
                    }
                }
                is ApiResult.Failure -> {
                    _uiState.update {
                        it.copy(
                            topicsLoading = false,
                            errorMessage = result.error.userMessage(),
                        )
                    }
                }
            }
        }
    }

    private fun loadSubtopics(topicId: Int) {
        _uiState.update { it.copy(subtopicsLoading = true) }
        viewModelScope.launch {
            when (val result = contentRepository.subtopics(topicId)) {
                is ApiResult.Success -> {
                    val subtopics = result.value.value
                    if (_uiState.value.selectedTopicId != topicId) return@launch
                    val selectedSubtopicId = subtopics.firstOrNull()?.id
                    _uiState.update {
                        it.copy(
                            subtopics = subtopics,
                            subtopicsLoading = false,
                            selectedSubtopicId = selectedSubtopicId,
                            messages = emptyList(),
                            input = "",
                            chatContext = null,
                            lastInteractionId = null,
                            ratingFeedback = null,
                            errorMessage = null,
                        )
                    }
                }
                is ApiResult.Failure -> {
                    _uiState.update {
                        it.copy(
                            subtopicsLoading = false,
                            errorMessage = result.error.userMessage(),
                        )
                    }
                }
            }
        }
    }
}
