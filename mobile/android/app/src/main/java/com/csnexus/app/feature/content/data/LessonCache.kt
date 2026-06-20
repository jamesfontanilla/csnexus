package com.csnexus.app.feature.content.data

import android.content.Context
import com.csnexus.app.core.database.ContentCacheDao
import com.csnexus.app.core.database.ContentCacheEntity
import com.csnexus.app.core.database.LessonCacheDao
import com.csnexus.app.core.database.LessonCacheEntity
import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.InlineCheck
import com.csnexus.app.feature.content.domain.Lesson
import com.csnexus.app.feature.content.domain.LessonFreshness
import com.csnexus.app.feature.content.domain.LessonBlock
import com.csnexus.app.feature.content.domain.LessonExplanation
import com.csnexus.app.feature.content.domain.LessonSegment
import com.csnexus.app.feature.content.domain.LessonSection
import com.csnexus.app.feature.content.domain.LessonWorkedExample
import com.csnexus.app.feature.content.domain.PracticeProblem
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

interface LessonCache {
    suspend fun modules(): CachedContent<List<LearningModule>>?
    suspend fun putModules(modules: List<LearningModule>)
    suspend fun topics(moduleId: Int): CachedContent<List<LearningTopic>>?
    suspend fun putTopics(moduleId: Int, topics: List<LearningTopic>)
    suspend fun subtopics(topicId: Int): CachedContent<List<LearningSubtopic>>?
    suspend fun putSubtopics(topicId: Int, subtopics: List<LearningSubtopic>)
    suspend fun get(subtopicId: Int): Lesson?
    suspend fun put(lesson: Lesson)
}

data class CachedContent<T>(
    val value: T,
    val cachedAtMillis: Long,
)

class SharedPreferencesLessonCache(context: Context) : LessonCache {
    private val prefs = context.getSharedPreferences("lesson_cache", Context.MODE_PRIVATE)
    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun modules(): CachedContent<List<LearningModule>>? {
        return readCachedList<CachedModule>(KEY_MODULES)?.let { cached ->
            CachedContent(cached.items.map { it.toDomain() }, cached.cachedAtMillis)
        }
    }

    override suspend fun putModules(modules: List<LearningModule>) {
        writeCachedList(KEY_MODULES, modules.map(CachedModule::from))
    }

    override suspend fun topics(moduleId: Int): CachedContent<List<LearningTopic>>? {
        return readCachedList<CachedTopic>(topicsKey(moduleId))?.let { cached ->
            CachedContent(cached.items.map { it.toDomain() }, cached.cachedAtMillis)
        }
    }

    override suspend fun putTopics(moduleId: Int, topics: List<LearningTopic>) {
        writeCachedList(topicsKey(moduleId), topics.map(CachedTopic::from))
    }

    override suspend fun subtopics(topicId: Int): CachedContent<List<LearningSubtopic>>? {
        return readCachedList<CachedSubtopic>(subtopicsKey(topicId))?.let { cached ->
            CachedContent(cached.items.map { it.toDomain() }, cached.cachedAtMillis)
        }
    }

    override suspend fun putSubtopics(topicId: Int, subtopics: List<LearningSubtopic>) {
        writeCachedList(subtopicsKey(topicId), subtopics.map(CachedSubtopic::from))
    }

    override suspend fun get(subtopicId: Int): Lesson? {
        val raw = prefs.getString(key(subtopicId), null) ?: return null
        return runCatching { json.decodeFromString<CachedLesson>(raw).toDomain() }.getOrNull()
    }

    override suspend fun put(lesson: Lesson) {
        prefs.edit()
            .putString(key(lesson.subtopicId), json.encodeToString(CachedLesson.from(lesson)))
            .apply()
    }

    private fun key(subtopicId: Int): String = "lesson:$subtopicId"
    private fun topicsKey(moduleId: Int): String = "topics:$moduleId"
    private fun subtopicsKey(topicId: Int): String = "subtopics:$topicId"

    private inline fun <reified T> readCachedList(key: String): CachedList<T>? {
        val raw = prefs.getString(key, null) ?: return null
        return runCatching { json.decodeFromString<CachedList<T>>(raw) }.getOrNull()
    }

    private inline fun <reified T> writeCachedList(key: String, items: List<T>) {
        prefs.edit()
            .putString(
                key,
                json.encodeToString(
                    CachedList(
                        cachedAtMillis = System.currentTimeMillis(),
                        items = items,
                    ),
                ),
            )
            .apply()
    }

    private companion object {
        const val KEY_MODULES = "modules"
    }
}

class RoomLessonCache(
    private val contentCacheDao: ContentCacheDao,
    private val lessonCacheDao: LessonCacheDao,
    private val json: Json = Json { ignoreUnknownKeys = true },
) : LessonCache {
    override suspend fun modules(): CachedContent<List<LearningModule>>? {
        return readCachedList<CachedModule>(KEY_MODULES)?.let { cached ->
            CachedContent(cached.items.map { it.toDomain() }, cached.cachedAtMillis)
        }
    }

    override suspend fun putModules(modules: List<LearningModule>) {
        writeCachedList(KEY_MODULES, modules.map(CachedModule::from))
    }

    override suspend fun topics(moduleId: Int): CachedContent<List<LearningTopic>>? {
        return readCachedList<CachedTopic>(topicsKey(moduleId))?.let { cached ->
            CachedContent(cached.items.map { it.toDomain() }, cached.cachedAtMillis)
        }
    }

    override suspend fun putTopics(moduleId: Int, topics: List<LearningTopic>) {
        writeCachedList(topicsKey(moduleId), topics.map(CachedTopic::from))
    }

    override suspend fun subtopics(topicId: Int): CachedContent<List<LearningSubtopic>>? {
        return readCachedList<CachedSubtopic>(subtopicsKey(topicId))?.let { cached ->
            CachedContent(cached.items.map { it.toDomain() }, cached.cachedAtMillis)
        }
    }

    override suspend fun putSubtopics(topicId: Int, subtopics: List<LearningSubtopic>) {
        writeCachedList(subtopicsKey(topicId), subtopics.map(CachedSubtopic::from))
    }

    override suspend fun get(subtopicId: Int): Lesson? {
        val entity = lessonCacheDao.get(subtopicId) ?: return null
        return runCatching {
            json.decodeFromString<CachedLesson>(entity.payloadJson).toDomain()
        }.getOrNull()
    }

    override suspend fun put(lesson: Lesson) {
        lessonCacheDao.put(
            LessonCacheEntity(
                subtopicId = lesson.subtopicId,
                payloadJson = json.encodeToString(CachedLesson.from(lesson)),
                cachedAtMillis = System.currentTimeMillis(),
            ),
        )
    }

    private suspend inline fun <reified T> readCachedList(key: String): CachedList<T>? {
        val entity = contentCacheDao.get(key) ?: return null
        return runCatching { json.decodeFromString<CachedList<T>>(entity.payloadJson) }.getOrNull()
    }

    private suspend inline fun <reified T> writeCachedList(key: String, items: List<T>) {
        contentCacheDao.put(
            ContentCacheEntity(
                cacheKey = key,
                payloadJson = json.encodeToString(
                    CachedList(
                        cachedAtMillis = System.currentTimeMillis(),
                        items = items,
                    ),
                ),
                cachedAtMillis = System.currentTimeMillis(),
            ),
        )
    }

    private fun topicsKey(moduleId: Int): String = "topics:$moduleId"
    private fun subtopicsKey(topicId: Int): String = "subtopics:$topicId"

    private companion object {
        const val KEY_MODULES = "modules"
    }
}

@Serializable
private data class CachedList<T>(
    val cachedAtMillis: Long,
    val items: List<T>,
)

@Serializable
data class CachedModule(
    val id: Int,
    val title: String,
    val category: String,
    val slug: String,
    val isPublished: Boolean,
) {
    fun toDomain(): LearningModule = LearningModule(id, title, category, slug, isPublished)

    companion object {
        fun from(module: LearningModule): CachedModule = CachedModule(
            id = module.id,
            title = module.title,
            category = module.category,
            slug = module.slug,
            isPublished = module.isPublished,
        )
    }
}

@Serializable
data class CachedTopic(
    val id: Int,
    val title: String,
    val moduleId: Int,
    val isPublished: Boolean,
) {
    fun toDomain(): LearningTopic = LearningTopic(id, title, moduleId, isPublished)

    companion object {
        fun from(topic: LearningTopic): CachedTopic = CachedTopic(
            id = topic.id,
            title = topic.title,
            moduleId = topic.moduleId,
            isPublished = topic.isPublished,
        )
    }
}

@Serializable
data class CachedSubtopic(
    val id: Int,
    val title: String,
    val topicId: Int,
    val isPublished: Boolean,
) {
    fun toDomain(): LearningSubtopic = LearningSubtopic(id, title, topicId, isPublished)

    companion object {
        fun from(subtopic: LearningSubtopic): CachedSubtopic = CachedSubtopic(
            id = subtopic.id,
            title = subtopic.title,
            topicId = subtopic.topicId,
            isPublished = subtopic.isPublished,
        )
    }
}

@Serializable
data class CachedLesson(
    val id: Int,
    val subtopicId: Int,
    val title: String,
    val status: String,
    val rawContentJson: String,
    val schemaVersion: Int? = null,
    val contentVersion: String? = null,
    val etag: String? = null,
    val contentHash: String? = null,
    val updatedAt: String? = null,
    val summary: String,
    val keyTakeaways: List<String>,
    val explanations: List<CachedLessonExplanation>,
    val workedExamples: List<CachedLessonWorkedExample>,
    val sections: List<CachedLessonSection>,
    val isSegmented: Boolean = false,
    val segments: List<CachedLessonSegment> = emptyList(),
    val practiceProblems: List<CachedPracticeProblem> = emptyList(),
    val memoryAids: List<String> = emptyList(),
    val examStrategies: List<String> = emptyList(),
) {
    fun toDomain(): Lesson = Lesson(
        id = id,
        subtopicId = subtopicId,
        title = title,
        status = status,
        rawContentJson = rawContentJson,
        freshness = LessonFreshness(
            schemaVersion = schemaVersion,
            contentVersion = contentVersion,
            etag = etag,
            contentHash = contentHash,
            updatedAt = updatedAt,
        ),
        summary = summary,
        keyTakeaways = keyTakeaways,
        explanations = explanations.map { LessonExplanation(it.heading, it.body) },
        workedExamples = workedExamples.map { LessonWorkedExample(it.title, it.body) },
        sections = sections.map { LessonSection(it.title, it.blocks.map(CachedLessonBlock::toDomain)) },
        isSegmented = isSegmented,
        segments = segments.map(CachedLessonSegment::toDomain),
        practiceProblems = practiceProblems.map(CachedPracticeProblem::toDomain),
        memoryAids = memoryAids,
        examStrategies = examStrategies,
    )

    companion object {
        fun from(lesson: Lesson): CachedLesson = CachedLesson(
            id = lesson.id,
            subtopicId = lesson.subtopicId,
            title = lesson.title,
            status = lesson.status,
            rawContentJson = lesson.rawContentJson,
            schemaVersion = lesson.freshness?.schemaVersion,
            contentVersion = lesson.freshness?.contentVersion,
            etag = lesson.freshness?.etag,
            contentHash = lesson.freshness?.contentHash,
            updatedAt = lesson.freshness?.updatedAt,
            summary = lesson.summary,
            keyTakeaways = lesson.keyTakeaways,
            explanations = lesson.explanations.map { CachedLessonExplanation(it.heading, it.body) },
            workedExamples = lesson.workedExamples.map { CachedLessonWorkedExample(it.title, it.body) },
            sections = lesson.sections.map { CachedLessonSection(it.title, it.blocks.map(CachedLessonBlock::from)) },
            isSegmented = lesson.isSegmented,
            segments = lesson.segments.map(CachedLessonSegment::from),
            practiceProblems = lesson.practiceProblems.map(CachedPracticeProblem::from),
            memoryAids = lesson.memoryAids,
            examStrategies = lesson.examStrategies,
        )
    }
}

@Serializable
data class CachedLessonExplanation(
    val heading: String,
    val body: String,
)

@Serializable
data class CachedLessonWorkedExample(
    val title: String,
    val body: String,
)

@Serializable
data class CachedLessonSection(
    val title: String,
    val blocks: List<CachedLessonBlock>,
) {
    fun toDomain(): LessonSection = LessonSection(title, blocks.map(CachedLessonBlock::toDomain))

    companion object {
        fun from(section: LessonSection): CachedLessonSection = CachedLessonSection(
            title = section.title,
            blocks = section.blocks.map(CachedLessonBlock::from),
        )
    }
}

@Serializable
data class CachedLessonSegment(
    val index: Int,
    val estimatedMinutes: Int,
    val sections: List<CachedLessonSection>,
    val checks: List<CachedInlineCheck>,
) {
    fun toDomain(): LessonSegment = LessonSegment(
        index = index,
        estimatedMinutes = estimatedMinutes,
        sections = sections.map(CachedLessonSection::toDomain),
        checks = checks.map { InlineCheck(it.question, it.answer, it.rationale) },
    )

    companion object {
        fun from(segment: LessonSegment): CachedLessonSegment = CachedLessonSegment(
            index = segment.index,
            estimatedMinutes = segment.estimatedMinutes,
            sections = segment.sections.map(CachedLessonSection::from),
            checks = segment.checks.map { CachedInlineCheck(it.question, it.answer, it.rationale) },
        )
    }
}

@Serializable
data class CachedPracticeProblem(
    val number: Int,
    val question: String,
    val answer: String,
    val explanation: String,
    val difficulty: String,
) {
    fun toDomain(): PracticeProblem = PracticeProblem(number, question, answer, explanation, difficulty)

    companion object {
        fun from(problem: PracticeProblem): CachedPracticeProblem = CachedPracticeProblem(
            number = problem.number,
            question = problem.question,
            answer = problem.answer,
            explanation = problem.explanation,
            difficulty = problem.difficulty,
        )
    }
}

@Serializable
data class CachedLessonBlock(
    val type: String,
    val text: String,
    val language: String?,
    val headers: List<String>,
    val rows: List<List<String>>,
    val items: List<String>,
    val checks: List<CachedInlineCheck>,
    val fallbackText: String?,
) {
    fun toDomain(): LessonBlock = LessonBlock(
        type = type,
        text = text,
        language = language,
        headers = headers,
        rows = rows,
        items = items,
        checks = checks.map { InlineCheck(it.question, it.answer, it.rationale) },
        fallbackText = fallbackText,
    )

    companion object {
        fun from(block: LessonBlock): CachedLessonBlock = CachedLessonBlock(
            type = block.type,
            text = block.text,
            language = block.language,
            headers = block.headers,
            rows = block.rows,
            items = block.items,
            checks = block.checks.map { CachedInlineCheck(it.question, it.answer, it.rationale) },
            fallbackText = block.fallbackText,
        )
    }
}

@Serializable
data class CachedInlineCheck(
    val question: String,
    val answer: String,
    val rationale: String,
)
