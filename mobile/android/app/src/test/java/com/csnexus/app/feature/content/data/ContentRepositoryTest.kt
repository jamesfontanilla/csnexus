package com.csnexus.app.feature.content.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.Lesson
import kotlinx.coroutines.test.runTest
import kotlinx.serialization.json.JsonNull
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.IOException

class ContentRepositoryTest {
    @Test
    fun modulesFallsBackToCachedListWhenNetworkFails() = runTest {
        val cache = MemoryLessonCache()
        cache.putModules(
            listOf(
                LearningModule(
                    id = 1,
                    title = "Verbal Ability",
                    category = "PROFESSIONAL",
                    slug = "verbal",
                ),
            ),
        )
        val repository = ContentRepository(FailingContentApi(), cache)

        val result = repository.modules()

        assertTrue(result is ApiResult.Success)
        val payload = (result as ApiResult.Success).value
        assertTrue(payload.fromCache)
        assertEquals("Verbal Ability", payload.value.single().title)
    }

    @Test
    fun topicsAndSubtopicsFallBackToCachedListsWhenNetworkFails() = runTest {
        val cache = MemoryLessonCache()
        cache.putTopics(1, listOf(LearningTopic(id = 2, title = "Grammar", moduleId = 1)))
        cache.putSubtopics(2, listOf(LearningSubtopic(id = 3, title = "Subject Verb Agreement", topicId = 2)))
        val repository = ContentRepository(FailingContentApi(), cache)

        val topics = repository.topics(1) as ApiResult.Success
        val subtopics = repository.subtopics(2) as ApiResult.Success

        assertTrue(topics.value.fromCache)
        assertTrue(subtopics.value.fromCache)
        assertEquals("Grammar", topics.value.value.single().title)
        assertEquals("Subject Verb Agreement", subtopics.value.value.single().title)
    }

    @Test
    fun completeLessonMapsAwardedXpResponse() = runTest {
        val api = CompletionContentApi(LessonCompletionDto(awardedXp = 15, alreadyCompleted = false))
        val repository = ContentRepository(
            api,
            MemoryLessonCache(),
        )

        val result = repository.completeLesson(3)

        assertTrue(result is ApiResult.Success)
        val completion = (result as ApiResult.Success).value
        assertEquals(15, completion.awardedXp)
        assertEquals(false, completion.alreadyCompleted)
        assertEquals(3, api.completedSubtopicId)
        assertTrue(api.completionRequest?.clientEventId?.startsWith("lesson:") == true)
        assertEquals(api.completionRequest?.clientEventId, api.idempotencyKey)
    }
}

private class FailingContentApi : ContentApi {
    override suspend fun modules(): PaginatedResponseDto<ModuleDto> = throw IOException("offline")

    override suspend fun topics(moduleId: Int): List<TopicDto> = throw IOException("offline")

    override suspend fun subtopics(topicId: Int): List<SubtopicDto> = throw IOException("offline")

    override suspend fun lesson(subtopicId: Int): LessonDto = LessonDto(
        id = 1,
        subtopicId = subtopicId,
        title = "Unused",
        status = "published",
        contentJson = JsonNull,
    )

    override suspend fun completeLesson(
        subtopicId: Int,
        request: LessonCompleteRequestDto,
        idempotencyKey: String?,
    ): LessonCompletionDto = throw IOException("offline")
}

private class CompletionContentApi(
    private val completion: LessonCompletionDto,
) : ContentApi {
    var completedSubtopicId: Int? = null
        private set
    var completionRequest: LessonCompleteRequestDto? = null
        private set
    var idempotencyKey: String? = null
        private set

    override suspend fun modules(): PaginatedResponseDto<ModuleDto> = PaginatedResponseDto(emptyList(), 0, 0, 20)

    override suspend fun topics(moduleId: Int): List<TopicDto> = emptyList()

    override suspend fun subtopics(topicId: Int): List<SubtopicDto> = emptyList()

    override suspend fun lesson(subtopicId: Int): LessonDto = LessonDto(
        id = 1,
        subtopicId = subtopicId,
        title = "Unused",
        status = "published",
        contentJson = JsonNull,
    )

    override suspend fun completeLesson(
        subtopicId: Int,
        request: LessonCompleteRequestDto,
        idempotencyKey: String?,
    ): LessonCompletionDto {
        completedSubtopicId = subtopicId
        completionRequest = request
        this.idempotencyKey = idempotencyKey
        return completion
    }
}

private class MemoryLessonCache : LessonCache {
    private var cachedModules: CachedContent<List<LearningModule>>? = null
    private val cachedTopics = mutableMapOf<Int, CachedContent<List<LearningTopic>>>()
    private val cachedSubtopics = mutableMapOf<Int, CachedContent<List<LearningSubtopic>>>()
    private val lessons = mutableMapOf<Int, Lesson>()

    override suspend fun modules(): CachedContent<List<LearningModule>>? = cachedModules

    override suspend fun putModules(modules: List<LearningModule>) {
        cachedModules = CachedContent(modules, 1L)
    }

    override suspend fun topics(moduleId: Int): CachedContent<List<LearningTopic>>? = cachedTopics[moduleId]

    override suspend fun putTopics(moduleId: Int, topics: List<LearningTopic>) {
        cachedTopics[moduleId] = CachedContent(topics, 1L)
    }

    override suspend fun subtopics(topicId: Int): CachedContent<List<LearningSubtopic>>? = cachedSubtopics[topicId]

    override suspend fun putSubtopics(topicId: Int, subtopics: List<LearningSubtopic>) {
        cachedSubtopics[topicId] = CachedContent(subtopics, 1L)
    }

    override suspend fun get(subtopicId: Int): Lesson? = lessons[subtopicId]

    override suspend fun put(lesson: Lesson) {
        lessons[lesson.subtopicId] = lesson
    }
}
