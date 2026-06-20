package com.csnexus.app.feature.content.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.Lesson
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class ModuleListUiState(
    val isLoading: Boolean = true,
    val modules: List<LearningModule> = emptyList(),
    val errorMessage: String? = null,
    val fromCache: Boolean = false,
)

class ContentViewModel(
    private val repository: ContentRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(ModuleListUiState())
    val uiState: StateFlow<ModuleListUiState> = _uiState.asStateFlow()

    init {
        loadModules()
    }

    fun loadModules() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null, fromCache = false) }
            when (val result = repository.modules()) {
                is ApiResult.Success -> {
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            modules = result.value.value,
                            fromCache = result.value.fromCache,
                        )
                    }
                }
                is ApiResult.Failure -> {
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            errorMessage = result.error.userMessage(),
                        )
                    }
                }
            }
        }
    }
}

data class TopicListUiState(
    val isLoading: Boolean = true,
    val topics: List<LearningTopic> = emptyList(),
    val errorMessage: String? = null,
    val fromCache: Boolean = false,
)

data class SubtopicListUiState(
    val isLoading: Boolean = true,
    val subtopics: List<LearningSubtopic> = emptyList(),
    val errorMessage: String? = null,
    val fromCache: Boolean = false,
)

data class LessonUiState(
    val isLoading: Boolean = true,
    val lesson: Lesson? = null,
    val errorMessage: String? = null,
    val fromCache: Boolean = false,
    val completed: Boolean = false,
    val isCompleting: Boolean = false,
    val completionMessage: String? = null,
)

class TopicListViewModel(
    private val repository: ContentRepository,
    private val moduleId: Int,
) : ViewModel() {
    private val _uiState = MutableStateFlow(TopicListUiState())
    val uiState: StateFlow<TopicListUiState> = _uiState.asStateFlow()

    init {
        loadTopics()
    }

    fun loadTopics() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null, fromCache = false) }
            when (val result = repository.topics(moduleId)) {
                is ApiResult.Success -> _uiState.update {
                    it.copy(
                        isLoading = false,
                        topics = result.value.value,
                        fromCache = result.value.fromCache,
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(isLoading = false, errorMessage = result.error.userMessage())
                }
            }
        }
    }
}

class SubtopicListViewModel(
    private val repository: ContentRepository,
    private val topicId: Int,
) : ViewModel() {
    private val _uiState = MutableStateFlow(SubtopicListUiState())
    val uiState: StateFlow<SubtopicListUiState> = _uiState.asStateFlow()

    init {
        loadSubtopics()
    }

    fun loadSubtopics() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null, fromCache = false) }
            when (val result = repository.subtopics(topicId)) {
                is ApiResult.Success -> _uiState.update {
                    it.copy(
                        isLoading = false,
                        subtopics = result.value.value,
                        fromCache = result.value.fromCache,
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(isLoading = false, errorMessage = result.error.userMessage())
                }
            }
        }
    }
}

class LessonViewModel(
    private val repository: ContentRepository,
    private val subtopicId: Int,
) : ViewModel() {
    private val _uiState = MutableStateFlow(LessonUiState())
    val uiState: StateFlow<LessonUiState> = _uiState.asStateFlow()

    init {
        loadLesson()
    }

    fun loadLesson() {
        viewModelScope.launch {
            _uiState.update {
                it.copy(
                    isLoading = true,
                    errorMessage = null,
                    fromCache = false,
                    completionMessage = null,
                )
            }
            when (val result = repository.lesson(subtopicId)) {
                is ApiResult.Success -> _uiState.update {
                    it.copy(
                        isLoading = false,
                        lesson = result.value.value,
                        fromCache = result.value.fromCache,
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(isLoading = false, errorMessage = result.error.userMessage())
                }
            }
        }
    }

    fun completeLesson() {
        viewModelScope.launch {
            _uiState.update { it.copy(isCompleting = true, completionMessage = null) }
            when (val result = repository.completeLesson(subtopicId)) {
                is ApiResult.Success -> _uiState.update {
                    it.copy(
                        completed = !result.value.queuedOffline,
                        isCompleting = false,
                        completionMessage = when {
                            result.value.queuedOffline -> "Offline. Lesson completion queued and will be confirmed after sync."
                            result.value.alreadyCompleted -> "Lesson already completed."
                            result.value.awardedXp > 0 -> "Lesson completed (+${result.value.awardedXp} XP)."
                            else -> "Lesson completed."
                        },
                    )
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(
                        isCompleting = false,
                        completionMessage = result.error.userMessage(),
                    )
                }
            }
        }
    }
}

class ContentViewModelFactory(
    private val repository: ContentRepository,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return ContentViewModel(repository) as T
    }
}

class TopicListViewModelFactory(
    private val repository: ContentRepository,
    private val moduleId: Int,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return TopicListViewModel(repository, moduleId) as T
    }
}

class SubtopicListViewModelFactory(
    private val repository: ContentRepository,
    private val topicId: Int,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return SubtopicListViewModel(repository, topicId) as T
    }
}

class LessonViewModelFactory(
    private val repository: ContentRepository,
    private val subtopicId: Int,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return LessonViewModel(repository, subtopicId) as T
    }
}
