package com.csnexus.app.feature.content.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement

@Serializable
data class PaginatedResponseDto<T>(
    val items: List<T>,
    val total: Int,
    val skip: Int,
    val limit: Int,
)

@Serializable
data class ModuleDto(
    val id: Int,
    val category: String,
    val slug: String,
    val title: String,
    @SerialName("order_index")
    val orderIndex: Int,
    @SerialName("is_published")
    val isPublished: Boolean,
)

@Serializable
data class TopicDto(
    val id: Int,
    @SerialName("module_id")
    val moduleId: Int,
    val slug: String,
    val title: String,
    @SerialName("order_index")
    val orderIndex: Int,
    @SerialName("is_published")
    val isPublished: Boolean = true,
)

@Serializable
data class SubtopicDto(
    val id: Int,
    @SerialName("topic_id")
    val topicId: Int,
    val slug: String,
    val title: String,
    @SerialName("order_index")
    val orderIndex: Int,
    @SerialName("is_published")
    val isPublished: Boolean = true,
)

@Serializable
data class LessonDto(
    val id: Int,
    @SerialName("subtopic_id")
    val subtopicId: Int,
    val title: String = "",
    val status: String = "PUBLISHED",
    @SerialName("content_json")
    val contentJson: JsonElement,
)

@Serializable
data class LessonContentDto(
    @SerialName("metadata")
    val metadata: LessonMetadataDto? = null,
    val explanations: List<LessonExplanationDto> = emptyList(),
    @SerialName("worked_examples")
    val workedExamples: List<LessonWorkedExampleDto> = emptyList(),
    @SerialName("key_takeaways")
    val keyTakeaways: List<String> = emptyList(),
    val summary: String = "",
    @SerialName("learning_objectives")
    val learningObjectives: List<String> = emptyList(),
    @SerialName("guided_session")
    val guidedSession: GuidedSessionDto? = null,
    val sections: List<LessonSectionDto> = emptyList(),
    @SerialName("is_segmented")
    val isSegmented: Boolean = false,
    val segments: List<LessonSegmentDto> = emptyList(),
    @SerialName("practice_problems")
    val practiceProblems: List<PracticeProblemDto> = emptyList(),
    @SerialName("memory_aids")
    val memoryAids: List<String> = emptyList(),
    @SerialName("exam_strategies")
    val examStrategies: List<String> = emptyList(),
)

@Serializable
data class LessonMetadataDto(
    val title: String = "",
    @SerialName("schema_version")
    val schemaVersion: Int? = null,
    @SerialName("content_version")
    val contentVersion: String? = null,
    val etag: String? = null,
    @SerialName("content_hash")
    val contentHash: String? = null,
    @SerialName("updated_at")
    val updatedAt: String? = null,
)

@Serializable
data class LessonExplanationDto(
    val heading: String = "",
    val body: String = "",
)

@Serializable
data class LessonWorkedExampleDto(
    val title: String = "",
    val body: String = "",
)

@Serializable
data class LessonSectionDto(
    val title: String = "",
    val blocks: List<LessonBlockDto> = emptyList(),
)

@Serializable
data class GuidedSessionDto(
    val title: String = "",
    val objective: String = "",
    @SerialName("must_know")
    val mustKnow: List<String> = emptyList(),
    val steps: List<GuidedSessionStepDto> = emptyList(),
)

@Serializable
data class GuidedSessionStepDto(
    val index: Int = 0,
    val kind: String = "",
    val title: String = "",
    val summary: String = "",
    @SerialName("section_index")
    val sectionIndex: Int? = null,
    @SerialName("estimated_reading_seconds")
    val estimatedReadingSeconds: Int = 0,
    @SerialName("subsection_count")
    val subsectionCount: Int = 0,
    @SerialName("focus_tags")
    val focusTags: List<String> = emptyList(),
)

@Serializable
data class LessonSegmentDto(
    val index: Int = 0,
    @SerialName("estimated_minutes")
    val estimatedMinutes: Int = 0,
    val sections: List<LessonSectionDto> = emptyList(),
    val checks: List<InlineCheckDto> = emptyList(),
)

@Serializable
data class LessonBlockDto(
    val type: String = "",
    val content: JsonElement? = null,
    val language: String? = null,
    @SerialName("fallback_text")
    val fallbackText: String? = null,
    @SerialName("requires_client_capability")
    val requiresClientCapability: String? = null,
)

@Serializable
data class InlineCheckDto(
    val question: String = "",
    val answer: String = "",
    val rationale: String = "",
)

@Serializable
data class PracticeProblemDto(
    val number: Int = 0,
    val question: String = "",
    val answer: String = "",
    val explanation: String = "",
    val difficulty: String = "",
)

@Serializable
data class LessonCompleteRequestDto(
    @SerialName("client_event_id")
    val clientEventId: String,
    @SerialName("completed_at")
    val completedAt: String? = null,
)

@Serializable
data class LessonCompletionDto(
    @SerialName("lesson_id")
    val lessonId: Int = 0,
    @SerialName("user_id")
    val userId: Int = 0,
    @SerialName("completed_at")
    val completedAt: String = "",
    @SerialName("awarded_xp")
    val awardedXp: Int = 0,
    @SerialName("already_completed")
    val alreadyCompleted: Boolean = false,
)
