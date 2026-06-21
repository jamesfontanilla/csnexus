package com.csnexus.app.feature.tutor.ui

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.content.data.ContentApi
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.content.data.CachedContent
import com.csnexus.app.feature.content.data.LessonCache
import com.csnexus.app.feature.content.data.LessonCompleteRequestDto
import com.csnexus.app.feature.content.data.LessonCompletionDto
import com.csnexus.app.feature.content.data.LessonDto
import com.csnexus.app.feature.content.data.ModuleDto
import com.csnexus.app.feature.content.data.PaginatedResponseDto
import com.csnexus.app.feature.content.data.SubtopicDto
import com.csnexus.app.feature.content.data.TopicDto
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.Lesson
import com.csnexus.app.feature.content.domain.LessonCompletion
import com.csnexus.app.feature.tutor.data.LessonChatHistoryItemDto
import com.csnexus.app.feature.tutor.data.LessonChatResponseDto
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.After
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class TutorViewModelTest {

    private val dispatcher = StandardTestDispatcher()

    @Before
    fun setUp() {
        Dispatchers.setMain(dispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun initializesByLoadingModulesAndAutoSelectingTheFirstContext() = runTest {
        val vm = createViewModel()

        advanceUntilIdle()

        val state = vm.uiState.value
        assertEquals(1, state.modules.size)
        vm.onModuleSelected("10")
        advanceUntilIdle()
        vm.onTopicSelected("20")
        advanceUntilIdle()
        vm.onSubtopicSelected("30")
        advanceUntilIdle()

        val selectedState = vm.uiState.value
        assertEquals(10, selectedState.selectedModuleId)
        assertEquals(20, selectedState.selectedTopicId)
        assertEquals(30, selectedState.selectedSubtopicId)
    }

    @Test
    fun sendMessageAppendsAssistantResponseAndPersistsContext() = runTest {
        val tutorRepo = FakeTutorRepository(
            response = LessonChatResponseDto(
                interactionId = 7,
                responseText = "Here is a helpful answer.",
                detectedIntent = "explain",
                contextJson = buildJsonObject {
                    put("turn", 1)
                },
            ),
        )
        val vm = createViewModel(tutorRepository = tutorRepo)

        advanceUntilIdle()
        vm.onModuleSelected("10")
        advanceUntilIdle()
        vm.onTopicSelected("20")
        advanceUntilIdle()
        vm.onSubtopicSelected("30")
        advanceUntilIdle()
        vm.onInputChanged("What does this mean?")
        vm.sendMessage()
        advanceUntilIdle()

        val state = vm.uiState.value
        assertEquals(2, state.messages.size)
        assertEquals("What does this mean?", state.messages.first().content)
        assertEquals("Here is a helpful answer.", state.messages.last().content)
        assertEquals(7, state.lastInteractionId)
        assertNotNull(state.chatContext)
        assertTrue(tutorRepo.lastHistory.isEmpty())
        assertEquals("What does this mean?", tutorRepo.lastMessage)
    }

    @Test
    fun rateInteractionShowsFeedback() = runTest {
        val tutorRepo = FakeTutorRepository(
            response = LessonChatResponseDto(interactionId = 9, responseText = "ok", detectedIntent = "explain"),
        )
        val vm = createViewModel(tutorRepository = tutorRepo)

        advanceUntilIdle()
        vm.onModuleSelected("10")
        advanceUntilIdle()
        vm.onTopicSelected("20")
        advanceUntilIdle()
        vm.onSubtopicSelected("30")
        advanceUntilIdle()
        vm.onInputChanged("Explain this")
        vm.sendMessage()
        advanceUntilIdle()
        vm.rateInteraction(helpful = true)
        advanceUntilIdle()

        assertEquals(true, tutorRepo.lastHelpful)
        assertNotNull(vm.uiState.value.ratingFeedback)
    }

    @Test
    fun resetConversationClearsMessagesAndContext() = runTest {
        val tutorRepo = FakeTutorRepository(
            response = LessonChatResponseDto(interactionId = 2, responseText = "ok", detectedIntent = "explain"),
        )
        val vm = createViewModel(tutorRepository = tutorRepo)

        advanceUntilIdle()
        vm.onModuleSelected("10")
        advanceUntilIdle()
        vm.onTopicSelected("20")
        advanceUntilIdle()
        vm.onSubtopicSelected("30")
        advanceUntilIdle()
        vm.onInputChanged("Hello")
        vm.sendMessage()
        advanceUntilIdle()
        vm.resetConversation()

        val state = vm.uiState.value
        assertTrue(state.messages.isEmpty())
        assertNull(state.chatContext)
        assertNull(state.lastInteractionId)
        assertFalse(state.sending)
    }

    private fun createViewModel(
        tutorRepository: FakeTutorRepository = FakeTutorRepository(),
    ): TutorViewModel {
        val contentRepository = ContentRepository(
            contentApi = FakeContentApi(),
            lessonCache = FakeLessonCache(),
        )
        return TutorViewModel(tutorRepository, contentRepository)
    }
}

private class FakeContentApi : ContentApi {
    override suspend fun modules(): PaginatedResponseDto<ModuleDto> =
        PaginatedResponseDto(
            items = listOf(
                ModuleDto(
                    id = 10,
                    category = "General",
                    slug = "general",
                    title = "General Ability",
                    orderIndex = 1,
                    isPublished = true,
                ),
            ),
            total = 1,
            skip = 0,
            limit = 1,
        )

    override suspend fun topics(moduleId: Int): List<TopicDto> =
        listOf(
            TopicDto(
                id = 20,
                moduleId = moduleId,
                slug = "topic",
                title = "Topic Alpha",
                orderIndex = 1,
                isPublished = true,
            ),
        )

    override suspend fun subtopics(topicId: Int): List<SubtopicDto> =
        listOf(
            SubtopicDto(
                id = 30,
                topicId = topicId,
                slug = "subtopic",
                title = "Subtopic One",
                orderIndex = 1,
                isPublished = true,
            ),
        )

    override suspend fun lesson(subtopicId: Int): LessonDto =
        LessonDto(
            id = 40,
            subtopicId = subtopicId,
            title = "Lesson",
            status = "PUBLISHED",
            contentJson = buildJsonObject {
                put("metadata", buildJsonObject { put("subtopic_id", subtopicId) })
            },
        )

    override suspend fun completeLesson(
        subtopicId: Int,
        request: LessonCompleteRequestDto,
        idempotencyKey: String?,
    ): LessonCompletionDto {
        return LessonCompletionDto(
            lessonId = subtopicId,
            userId = 1,
            completedAt = "2026-01-01T00:00:00Z",
            awardedXp = 10,
            alreadyCompleted = false,
        )
    }
}

private class FakeLessonCache : LessonCache {
    override suspend fun modules(): CachedContent<List<LearningModule>>? = null
    override suspend fun putModules(modules: List<LearningModule>) = Unit
    override suspend fun topics(moduleId: Int): CachedContent<List<LearningTopic>>? = null
    override suspend fun putTopics(moduleId: Int, topics: List<LearningTopic>) = Unit
    override suspend fun subtopics(topicId: Int): CachedContent<List<LearningSubtopic>>? = null
    override suspend fun putSubtopics(topicId: Int, subtopics: List<LearningSubtopic>) = Unit
    override suspend fun get(subtopicId: Int): Lesson? = null
    override suspend fun put(lesson: Lesson) = Unit
}

private class FakeTutorRepository(
    private val response: LessonChatResponseDto = LessonChatResponseDto(
        interactionId = 1,
        responseText = "default response",
        detectedIntent = "explain",
    ),
) : TutorRepositoryContract {
    var lastMessage: String? = null
    var lastHistory: List<LessonChatHistoryItemDto> = emptyList()
    var lastHelpful: Boolean? = null
    var lastContextJson: JsonElement? = null

    override suspend fun tutorAction(
        action: com.csnexus.app.feature.tutor.data.TutorAction,
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<com.csnexus.app.feature.tutor.data.TutorResponseDto> {
        error("Not used")
    }

    override suspend fun stepByStep(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<com.csnexus.app.feature.tutor.data.StepByStepDto> {
        error("Not used")
    }

    override suspend fun similar(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<com.csnexus.app.feature.tutor.data.SimilarQuestionDto> {
        error("Not used")
    }

    override suspend fun rateInteraction(interactionId: Int, helpful: Boolean): ApiResult<Unit> {
        lastHelpful = helpful
        return ApiResult.Success(Unit)
    }

    override suspend fun lessonChat(
        message: String,
        contextJson: JsonElement?,
        subtopicId: Int?,
        activeSectionIndex: Int?,
        history: List<LessonChatHistoryItemDto>,
    ): ApiResult<LessonChatResponseDto> {
        lastMessage = message
        lastContextJson = contextJson
        lastHistory = history
        return ApiResult.Success(response)
    }
}
