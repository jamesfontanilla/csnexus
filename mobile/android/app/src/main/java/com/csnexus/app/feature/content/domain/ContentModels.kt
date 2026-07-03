package com.csnexus.app.feature.content.domain

data class LearningModule(
    val id: Int,
    val title: String,
    val category: String,
    val slug: String,
    val isPublished: Boolean = true,
)

data class LearningTopic(
    val id: Int,
    val title: String,
    val moduleId: Int,
    val isPublished: Boolean = true,
)

data class LearningSubtopic(
    val id: Int,
    val title: String,
    val topicId: Int,
    val isPublished: Boolean = true,
)

data class Lesson(
    val id: Int,
    val subtopicId: Int,
    val title: String,
    val status: String,
    val rawContentJson: String,
    val freshness: LessonFreshness? = null,
    val explanations: List<LessonExplanation> = emptyList(),
    val workedExamples: List<LessonWorkedExample> = emptyList(),
    val keyTakeaways: List<String> = emptyList(),
    val summary: String = "",
    val learningObjectives: List<String> = emptyList(),
    val guidedSession: GuidedSession? = null,
    val sections: List<LessonSection> = emptyList(),
    val isSegmented: Boolean = false,
    val segments: List<LessonSegment> = emptyList(),
    val screenPlan: LessonScreenPlan? = null,
    val practiceProblems: List<PracticeProblem> = emptyList(),
    val memoryAids: List<String> = emptyList(),
    val examStrategies: List<String> = emptyList(),
)

data class LessonFreshness(
    val schemaVersion: Int? = null,
    val contentVersion: String? = null,
    val etag: String? = null,
    val contentHash: String? = null,
    val updatedAt: String? = null,
)

data class LessonExplanation(
    val heading: String,
    val body: String,
)

data class LessonWorkedExample(
    val title: String,
    val body: String,
)

data class LessonSection(
    val title: String,
    val blocks: List<LessonBlock>,
)

data class GuidedSession(
    val title: String = "",
    val objective: String = "",
    val mustKnow: List<String> = emptyList(),
    val steps: List<GuidedSessionStep> = emptyList(),
)

data class GuidedSessionStep(
    val index: Int,
    val kind: String,
    val title: String,
    val summary: String = "",
    val sectionIndex: Int? = null,
    val estimatedReadingSeconds: Int = 0,
    val subsectionCount: Int = 0,
    val focusTags: List<String> = emptyList(),
)

data class LessonSegment(
    val index: Int,
    val estimatedMinutes: Int,
    val sections: List<LessonSection>,
    val checks: List<InlineCheck> = emptyList(),
)

data class LessonScreenPlan(
    val title: String = "",
    val objective: String = "",
    val mustKnow: List<String> = emptyList(),
    val screens: List<LessonScreen> = emptyList(),
    val estimatedReadingMinutes: Int = 0,
    val screenCount: Int = 0,
)

data class LessonScreen(
    val index: Int,
    val kind: String,
    val title: String,
    val summary: String = "",
    val sectionIndices: List<Int> = emptyList(),
    val sectionTitles: List<String> = emptyList(),
    val estimatedReadingSeconds: Int = 0,
    val focusTags: List<String> = emptyList(),
    val nodeKinds: List<String> = emptyList(),
    val callToAction: String = "",
)

data class LessonBlock(
    val type: String,
    val text: String = "",
    val language: String? = null,
    val headers: List<String> = emptyList(),
    val rows: List<List<String>> = emptyList(),
    val items: List<String> = emptyList(),
    val checks: List<InlineCheck> = emptyList(),
    val fallbackText: String? = null,
)

data class InlineCheck(
    val question: String,
    val answer: String,
    val rationale: String = "",
)

data class PracticeProblem(
    val number: Int,
    val question: String,
    val answer: String,
    val explanation: String = "",
    val difficulty: String = "",
)

data class LessonCompletion(
    val awardedXp: Int = 0,
    val alreadyCompleted: Boolean = false,
    val queuedOffline: Boolean = false,
)
