package com.csnexus.app.feature.content.data

import com.csnexus.app.feature.content.domain.LearningModule
import com.csnexus.app.feature.content.domain.LearningSubtopic
import com.csnexus.app.feature.content.domain.LearningTopic
import com.csnexus.app.feature.content.domain.LessonFreshness
import com.csnexus.app.feature.content.domain.Lesson
import com.csnexus.app.feature.content.domain.InlineCheck
import com.csnexus.app.feature.content.domain.LessonBlock
import com.csnexus.app.feature.content.domain.LessonExplanation
import com.csnexus.app.feature.content.domain.LessonSegment
import com.csnexus.app.feature.content.domain.LessonSection
import com.csnexus.app.feature.content.domain.LessonWorkedExample
import com.csnexus.app.feature.content.domain.PracticeProblem
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.contentOrNull
import kotlinx.serialization.json.decodeFromJsonElement
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject

fun ModuleDto.toDomain(): LearningModule = LearningModule(
    id = id,
    title = title,
    category = category,
    slug = slug,
    isPublished = isPublished,
)

fun TopicDto.toDomain(): LearningTopic = LearningTopic(
    id = id,
    title = title,
    moduleId = moduleId,
    isPublished = isPublished,
)

fun SubtopicDto.toDomain(): LearningSubtopic = LearningSubtopic(
    id = id,
    title = title,
    topicId = topicId,
    isPublished = isPublished,
)

private val lessonJson = Json { ignoreUnknownKeys = true }

fun LessonDto.toDomain(): Lesson {
    val parsed = runCatching {
        lessonJson.decodeFromJsonElement(LessonContentDto.serializer(), contentJson)
    }.getOrNull()
    val metadata = parsed?.metadata

    return Lesson(
        id = id,
        subtopicId = subtopicId,
        title = title.ifBlank { metadata?.title.orEmpty().ifBlank { "Lesson" } },
        status = status,
        rawContentJson = contentJson.toString(),
        freshness = metadata?.let {
            LessonFreshness(
                schemaVersion = it.schemaVersion,
                contentVersion = it.contentVersion,
                etag = it.etag,
                contentHash = it.contentHash,
                updatedAt = it.updatedAt,
            )
        },
        explanations = parsed?.explanations.orEmpty().map {
            LessonExplanation(heading = it.heading, body = it.body)
        },
        workedExamples = parsed?.workedExamples.orEmpty().map {
            LessonWorkedExample(title = it.title, body = it.body)
        },
        keyTakeaways = parsed?.keyTakeaways.orEmpty(),
        summary = parsed?.summary.orEmpty(),
        sections = parsed?.sections.orEmpty().map { it.toDomainSection() },
        isSegmented = parsed?.isSegmented == true && parsed.segments.isNotEmpty(),
        segments = parsed?.segments.orEmpty().map { it.toDomainSegment() },
        practiceProblems = parsed?.practiceProblems.orEmpty().map {
            PracticeProblem(
                number = it.number,
                question = it.question,
                answer = it.answer,
                explanation = it.explanation,
                difficulty = it.difficulty,
            )
        },
        memoryAids = parsed?.memoryAids.orEmpty(),
        examStrategies = parsed?.examStrategies.orEmpty(),
    )
}

private fun LessonSectionDto.toDomainSection(): LessonSection = LessonSection(
    title = title,
    blocks = blocks.map { it.toDomainBlock() },
)

private fun LessonSegmentDto.toDomainSegment(): LessonSegment = LessonSegment(
    index = index,
    estimatedMinutes = estimatedMinutes,
    sections = sections.map { it.toDomainSection() },
    checks = checks.map {
        InlineCheck(
            question = it.question,
            answer = it.answer,
            rationale = it.rationale,
        )
    },
)

private fun LessonBlockDto.toDomainBlock(): LessonBlock {
    val normalizedType = type.ifBlank { "prose" }
    val contentObject = content as? JsonObject
    val fallback = fallbackText ?: contentObject?.string("fallback_text")
    val languageValue = language ?: contentObject?.string("language")
    val text = content.textValue()

    return when (normalizedType) {
        "table" -> LessonBlock(
            type = normalizedType,
            text = contentObject?.string("summary").orEmpty(),
            headers = contentObject?.stringList("headers").orEmpty(),
            rows = contentObject?.rows("rows").orEmpty(),
            fallbackText = fallback,
        )
        "check_understanding" -> LessonBlock(
            type = normalizedType,
            checks = content.checks(),
            fallbackText = fallback,
        )
        "step_by_step" -> LessonBlock(
            type = normalizedType,
            text = text,
            items = contentObject?.stringList("steps").orEmpty().ifEmpty { text.lines().cleanLines() },
            fallbackText = fallback,
        )
        "list" -> LessonBlock(
            type = normalizedType,
            text = text,
            items = contentObject?.stringList("items").orEmpty().ifEmpty { text.lines().cleanLines() },
            fallbackText = fallback,
        )
        "prose", "code", "formula", "tip", "warning", "example", "svg", "image" -> LessonBlock(
            type = normalizedType,
            text = text,
            language = languageValue,
            fallbackText = fallback,
        )
        else -> LessonBlock(
            type = normalizedType,
            text = text,
            language = languageValue,
            fallbackText = fallback ?: "This lesson block is available in the web app until Android support is added.",
        )
    }
}

private fun JsonElement?.textValue(): String {
    return when (this) {
        null -> ""
        is JsonPrimitive -> contentOrNull.orEmpty()
        is JsonObject -> string("text")
            ?: string("body")
            ?: string("content")
            ?: string("markdown")
            ?: string("formula")
            ?: string("code")
            ?: string("svg")
            ?: string("url")
            ?: toString()
        else -> toString()
    }
}

private fun JsonElement?.checks(): List<InlineCheck> {
    val array = when (this) {
        is JsonArray -> this
        is JsonObject -> this["checks"] as? JsonArray
        else -> null
    } ?: return emptyList()

    return array.mapNotNull { element ->
        val obj = element as? JsonObject ?: return@mapNotNull null
        val question = obj.string("question").orEmpty()
        val answer = obj.string("answer").orEmpty()
        if (question.isBlank() && answer.isBlank()) return@mapNotNull null
        InlineCheck(
            question = question,
            answer = answer,
            rationale = obj.string("rationale").orEmpty(),
        )
    }
}

private fun JsonObject.string(key: String): String? =
    (this[key] as? JsonPrimitive)?.contentOrNull

private fun JsonObject.stringList(key: String): List<String> =
    (this[key] as? JsonArray)?.mapNotNull { (it as? JsonPrimitive)?.contentOrNull }.orEmpty()

private fun JsonObject.rows(key: String): List<List<String>> =
    (this[key] as? JsonArray)?.map { row ->
        when (row) {
            is JsonArray -> row.map { cell -> cell.textValue() }
            else -> listOf(row.textValue())
        }
    }.orEmpty()

private fun List<String>.cleanLines(): List<String> =
    map { it.replace(Regex("^(Step\\s+\\d+[:.]|\\d+\\.|[-*])\\s*", RegexOption.IGNORE_CASE), "").trim() }
        .filter { it.isNotBlank() }
