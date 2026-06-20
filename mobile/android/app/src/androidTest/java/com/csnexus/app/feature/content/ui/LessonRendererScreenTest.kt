package com.csnexus.app.feature.content.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.Modifier
import androidx.compose.ui.test.hasSetTextAction
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.assertIsEnabled
import androidx.compose.ui.test.assertIsNotEnabled
import androidx.compose.ui.test.assertTextContains
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.test.performTextInput
import com.csnexus.app.core.design.CSNexusTheme
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.content.data.CachedContent
import com.csnexus.app.feature.content.data.ContentApi
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.content.data.LessonCache
import com.csnexus.app.feature.content.data.LessonCompleteRequestDto
import com.csnexus.app.feature.content.data.LessonCompletionDto
import com.csnexus.app.feature.content.data.LessonDto
import com.csnexus.app.feature.content.data.ModuleDto
import com.csnexus.app.feature.content.data.PaginatedResponseDto
import com.csnexus.app.feature.content.data.SubtopicDto
import com.csnexus.app.feature.content.data.TopicDto
import com.csnexus.app.feature.content.domain.InlineCheck
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.Lesson
import com.csnexus.app.feature.content.domain.LessonBlock
import com.csnexus.app.feature.content.domain.LessonSection
import com.csnexus.app.feature.tutor.data.LessonChatHistoryItemDto
import com.csnexus.app.feature.tutor.data.LessonChatResponseDto
import com.csnexus.app.feature.tutor.data.SimilarQuestionDto
import com.csnexus.app.feature.tutor.data.StepByStepDto
import com.csnexus.app.feature.tutor.data.TutorAction
import com.csnexus.app.feature.tutor.data.TutorRepositoryContract
import com.csnexus.app.feature.tutor.data.TutorResponseDto
import java.io.IOException
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonNull
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test

class LessonRendererScreenTest {
    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun rendererShowsCoreBlocksFallbackAndInlineCheckReveal() {
        composeRule.setContent {
            CSNexusTheme {
                Column(Modifier.verticalScroll(rememberScrollState())) {
                    LessonBlockRenderer(
                        LessonBlock(
                            type = "table",
                            headers = listOf("Rule", "Example"),
                            rows = listOf(listOf("Subject", "Learner answers")),
                        ),
                    )
                    LessonBlockRenderer(LessonBlock(type = "code", text = "fun main() = Unit", language = "kotlin"))
                    LessonBlockRenderer(LessonBlock(type = "formula", text = "a^2 + b^2 = c^2"))
                    LessonBlockRenderer(LessonBlock(type = "tip", text = "Read the prompt twice."))
                    LessonBlockRenderer(LessonBlock(type = "warning", text = "Avoid unsupported assumptions."))
                    LessonBlockRenderer(LessonBlock(type = "example", text = "A worked example appears here."))
                    LessonBlockRenderer(LessonBlock(type = "step_by_step", items = listOf("Read", "Solve")))
                    LessonBlockRenderer(LessonBlock(type = "list", items = listOf("Recall", "Apply")))
                    LessonBlockRenderer(
                        LessonBlock(
                            type = "image",
                            text = "diagram-source",
                            fallbackText = "Diagram fallback",
                        ),
                    )
                    LessonBlockRenderer(
                        LessonBlock(
                            type = "check_understanding",
                            checks = listOf(
                                InlineCheck(
                                    question = "Which option agrees?",
                                    answer = "The singular verb.",
                                    rationale = "The subject is singular.",
                                ),
                            ),
                        ),
                    )
                    LessonBlockRenderer(
                        LessonBlock(
                            type = "interactive_lab",
                            text = "future block",
                            fallbackText = "Open the web app for this lab.",
                        ),
                    )
                }
            }
        }

        composeRule.onNodeWithText("Rule").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("Learner answers").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("fun main() = Unit").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("a^2 + b^2 = c^2").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("Tip").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("Watch out").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("A worked example appears here.").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("1. Read").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("- Recall").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("Diagram fallback").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("Unsupported lesson block").performScrollTo().assertIsDisplayed()
        composeRule.onNodeWithText("Open the web app for this lab.").performScrollTo().assertIsDisplayed()

        composeRule.onNodeWithText("Which option agrees?").performScrollTo().performClick()

        composeRule.onNodeWithText("The singular verb.").assertIsDisplayed()
        composeRule.onNodeWithText("The subject is singular.").assertIsDisplayed()
    }

    @Test
    fun segmentedLessonRequiresRevealBeforeContinueAndCompletesThroughBackend() {
        val repository = ContentRepository(
            contentApi = StaticLessonApi(
                lessonJson = segmentedLessonJson(),
                completion = LessonCompletionDto(awardedXp = 12, alreadyCompleted = false),
            ),
            lessonCache = MemoryLessonCache(),
        )

        composeRule.setContent {
            CSNexusTheme {
                LessonReaderScreen(
                    repository = repository,
                    tutorRepository = null,
                    subtopicId = 99,
                    contentPadding = PaddingValues(),
                )
            }
        }

        waitForText("Segmented lesson")
        composeRule.onNodeWithText("Part 1/2").assertIsDisplayed()
        composeRule.onNodeWithText("Continue").assertIsNotEnabled()

        composeRule.onNodeWithText("Check understanding").performClick()
        composeRule.onNodeWithText("Reveal answer").performClick()
        composeRule.onNodeWithText("The first idea.").assertIsDisplayed()
        composeRule.onNodeWithText("Continue").assertIsEnabled().performClick()

        composeRule.onNodeWithText("Part 2/2").assertIsDisplayed()
        composeRule.onNodeWithText("Final chunk").assertIsDisplayed()
        composeRule.onNodeWithText("Complete lesson").assertIsEnabled().performClick()

        waitForText("Lesson completed (+12 XP).")
        composeRule.onNodeWithText("Lesson completed (+12 XP).").assertIsDisplayed()
    }

    @Test
    fun cachedOfflineLessonShowsBannerAndDisablesCompletion() {
        val cachedLesson = Lesson(
            id = 7,
            subtopicId = 77,
            title = "Cached lesson",
            status = "published",
            rawContentJson = "{}",
            summary = "Available while offline.",
            sections = listOf(
                LessonSection(
                    title = "Offline section",
                    blocks = listOf(LessonBlock(type = "prose", text = "Read from cache.")),
                ),
            ),
        )
        val cache = MemoryLessonCache()
        runBlocking { cache.put(cachedLesson) }
        val repository = ContentRepository(OfflineContentApi(), cache)

        composeRule.setContent {
            CSNexusTheme {
                LessonReaderScreen(
                    repository = repository,
                    tutorRepository = null,
                    subtopicId = 77,
                    contentPadding = PaddingValues(),
                )
            }
        }

        waitForText("Cached lesson")
        composeRule.onNodeWithText("Offline. Showing saved lesson.").assertIsDisplayed()
        composeRule.onNodeWithText("Read from cache.").assertIsDisplayed()
        composeRule.onNodeWithText("Complete lesson").assertIsNotEnabled()
        composeRule.onNodeWithText("Reconnect to complete this lesson and update progress.").assertIsDisplayed()
    }

    @Test
    fun lessonTutorCompanionSendsStructuredPayloadKeepsHistoryAndAllowsRating() {
        val tutorRepository = RecordingTutorRepository()
        val repository = ContentRepository(
            contentApi = StaticLessonApi(
                lessonJson = segmentedLessonJson(),
                completion = LessonCompletionDto(awardedXp = 12, alreadyCompleted = false),
            ),
            lessonCache = MemoryLessonCache(),
        )

        composeRule.setContent {
            CSNexusTheme {
                LessonReaderScreen(
                    repository = repository,
                    tutorRepository = tutorRepository,
                    subtopicId = 99,
                    contentPadding = PaddingValues(),
                )
            }
        }

        waitForText("Segmented lesson")
        composeRule.onNodeWithText("Check understanding").performScrollTo().performClick()
        composeRule.onNodeWithText("Reveal answer").performScrollTo().performClick()
        composeRule.onNodeWithText("Tutor").performScrollTo().performClick()
        composeRule.onAllNodesWithText("Summarize")[0].performScrollTo().performClick()

        waitForText("Tutor says: Summarize this section")
        assertEquals("Summarize this section", tutorRepository.lastMessage)
        assertEquals(99, tutorRepository.lastSubtopicId)
        assertEquals(0, tutorRepository.lastActiveSectionIndex)
        assertTrue(tutorRepository.lastHistory.isEmpty())

        composeRule.onNodeWithText("Continue").performScrollTo().performClick()
        waitForText("Part 2/2")
        composeRule.onAllNodes(hasSetTextAction())[0].performTextInput("How is this tested?")
        composeRule.onNodeWithText("Send").performScrollTo().performClick()

        waitForText("Tutor says: How is this tested?")
        assertEquals("How is this tested?", tutorRepository.lastMessage)
        assertEquals(1, tutorRepository.lastActiveSectionIndex)
        assertEquals(2, tutorRepository.lastHistory.size)
        assertEquals("Summarize this section", tutorRepository.lastHistory[0].content)
        assertEquals("Tutor says: Summarize this section", tutorRepository.lastHistory[1].content)

        composeRule.onNodeWithText("Helpful").performScrollTo().performClick()
        composeRule.waitUntil(timeoutMillis = 5_000) { tutorRepository.lastRatedInteractionId == 42 }
        assertEquals(true, tutorRepository.lastRatedHelpful)
    }

    @Test
    fun lessonTutorOfflinePreservesDraftInField() {
        val repository = ContentRepository(
            contentApi = StaticLessonApi(
                lessonJson = segmentedLessonJson(),
                completion = LessonCompletionDto(awardedXp = 12, alreadyCompleted = false),
            ),
            lessonCache = MemoryLessonCache(),
        )

        composeRule.setContent {
            CSNexusTheme {
                LessonReaderScreen(
                    repository = repository,
                    tutorRepository = null,
                    subtopicId = 99,
                    contentPadding = PaddingValues(),
                )
            }
        }

        waitForText("Segmented lesson")
        composeRule.onNodeWithText("Tutor").performScrollTo().performClick()
        composeRule.onAllNodes(hasSetTextAction())[0].performTextInput("Please explain this step")
        composeRule.onNodeWithText("Send").performScrollTo().performClick()

        composeRule
            .onNodeWithText("Tutor is unavailable offline. Your draft will stay in the field until you reconnect.")
            .performScrollTo()
            .assertIsDisplayed()
        composeRule.onAllNodes(hasSetTextAction())[0].assertTextContains("Please explain this step")
    }

    private fun waitForText(text: String) {
        composeRule.waitUntil(timeoutMillis = 5_000) {
            composeRule.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty()
        }
    }
}

private class StaticLessonApi(
    private val lessonJson: JsonElement,
    private val completion: LessonCompletionDto,
) : ContentApi {
    override suspend fun modules(): PaginatedResponseDto<ModuleDto> = PaginatedResponseDto(emptyList(), 0, 0, 20)

    override suspend fun topics(moduleId: Int): List<TopicDto> = emptyList()

    override suspend fun subtopics(topicId: Int): List<SubtopicDto> = emptyList()

    override suspend fun lesson(subtopicId: Int): LessonDto = LessonDto(
        id = 1,
        subtopicId = subtopicId,
        title = "Segmented lesson",
        status = "published",
        contentJson = lessonJson,
    )

    override suspend fun completeLesson(
        subtopicId: Int,
        request: LessonCompleteRequestDto,
        idempotencyKey: String?,
    ): LessonCompletionDto = completion
}

private class OfflineContentApi : ContentApi {
    override suspend fun modules(): PaginatedResponseDto<ModuleDto> = throw IOException("offline")

    override suspend fun topics(moduleId: Int): List<TopicDto> = throw IOException("offline")

    override suspend fun subtopics(topicId: Int): List<SubtopicDto> = throw IOException("offline")

    override suspend fun lesson(subtopicId: Int): LessonDto = throw IOException("offline")

    override suspend fun completeLesson(
        subtopicId: Int,
        request: LessonCompleteRequestDto,
        idempotencyKey: String?,
    ): LessonCompletionDto = throw IOException("offline")
}

private class MemoryLessonCache : LessonCache {
    private var cachedModules: CachedContent<List<LearningModule>>? = null
    private val cachedTopics = mutableMapOf<Int, CachedContent<List<LearningTopic>>>()
    private val cachedSubtopics = mutableMapOf<Int, CachedContent<List<LearningSubtopic>>>()
    private val lessons = mutableMapOf<Int, Lesson>()

    override suspend fun modules(): CachedContent<List<LearningModule>>? = cachedModules

    override suspend fun putModules(modules: List<LearningModule>) {
        this.cachedModules = CachedContent(modules, 1L)
    }

    override suspend fun topics(moduleId: Int): CachedContent<List<LearningTopic>>? = cachedTopics[moduleId]

    override suspend fun putTopics(moduleId: Int, topics: List<LearningTopic>) {
        this.cachedTopics[moduleId] = CachedContent(topics, 1L)
    }

    override suspend fun subtopics(topicId: Int): CachedContent<List<LearningSubtopic>>? = cachedSubtopics[topicId]

    override suspend fun putSubtopics(topicId: Int, subtopics: List<LearningSubtopic>) {
        this.cachedSubtopics[topicId] = CachedContent(subtopics, 1L)
    }

    override suspend fun get(subtopicId: Int): Lesson? = lessons[subtopicId]

    override suspend fun put(lesson: Lesson) {
        lessons[lesson.subtopicId] = lesson
    }
}

private class RecordingTutorRepository : TutorRepositoryContract {
    var lastMessage: String? = null
    var lastSubtopicId: Int? = null
    var lastActiveSectionIndex: Int? = null
    var lastHistory: List<LessonChatHistoryItemDto> = emptyList()
    var lastRatedInteractionId: Int = -1
    var lastRatedHelpful: Boolean? = null
    private var interactionIdCounter = 40

    override suspend fun tutorAction(
        action: TutorAction,
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<TutorResponseDto> = ApiResult.Success(TutorResponseDto(responseText = "unused"))

    override suspend fun stepByStep(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<StepByStepDto> = ApiResult.Success(StepByStepDto())

    override suspend fun similar(
        questionId: Int,
        selectedAnswer: String?,
    ): ApiResult<SimilarQuestionDto> = ApiResult.Success(SimilarQuestionDto())

    override suspend fun rateInteraction(interactionId: Int, helpful: Boolean): ApiResult<Unit> {
        lastRatedInteractionId = interactionId
        lastRatedHelpful = helpful
        return ApiResult.Success(Unit)
    }

    override suspend fun lessonChat(
        message: String,
        context: String?,
        subtopicId: Int?,
        activeSectionIndex: Int?,
        history: List<LessonChatHistoryItemDto>,
    ): ApiResult<LessonChatResponseDto> {
        interactionIdCounter += 1
        lastMessage = message
        lastSubtopicId = subtopicId
        lastActiveSectionIndex = activeSectionIndex
        lastHistory = history
        return ApiResult.Success(
            LessonChatResponseDto(
                interactionId = interactionIdCounter,
                responseText = "Tutor says: $message",
            ),
        )
    }
}

private fun segmentedLessonJson(): JsonElement = Json.parseToJsonElement(
    """
    {
      "summary": "Learn in gated chunks.",
      "is_segmented": true,
      "segments": [
        {
          "index": 0,
          "estimated_minutes": 4,
          "sections": [
            {
              "title": "First chunk",
              "blocks": [
                { "type": "prose", "content": { "text": "Read the first idea." } }
              ]
            }
          ],
          "checks": [
            {
              "question": "What should you remember?",
              "answer": "The first idea.",
              "rationale": "The next segment unlocks after at least one reveal."
            }
          ]
        },
        {
          "index": 1,
          "estimated_minutes": 3,
          "sections": [
            {
              "title": "Final chunk",
              "blocks": [
                { "type": "formula", "content": { "formula": "x = y + z" } }
              ]
            }
          ],
          "checks": []
        }
      ],
      "practice_problems": [
        { "number": 1, "question": "Practice?", "answer": "Practice answer.", "difficulty": "easy" }
      ],
      "memory_aids": ["Remember the first idea."],
      "exam_strategies": ["Check the final formula."]
    }
    """.trimIndent(),
)
