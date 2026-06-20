package com.csnexus.app.feature.content.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlinx.serialization.json.Json

class ContentMappersTest {
    @Test
    fun mapsModuleDtoToDomainModel() {
        val dto = ModuleDto(
            id = 1,
            category = "PROFESSIONAL",
            slug = "verbal-ability",
            title = "Verbal Ability",
            orderIndex = 0,
            isPublished = true,
        )

        val module = dto.toDomain()

        assertEquals(1, module.id)
        assertEquals("Verbal Ability", module.title)
        assertEquals("PROFESSIONAL", module.category)
        assertEquals("verbal-ability", module.slug)
    }

    @Test
    fun decodesBackendTopicAndSubtopicResponsesWithoutPublishedFlags() {
        val json = Json { ignoreUnknownKeys = true }
        val topic = json.decodeFromString<TopicDto>(
            """
            {
              "id": 10,
              "module_id": 1,
              "slug": "clerical-ability",
              "title": "Clerical Ability",
              "order_index": 2
            }
            """.trimIndent(),
        ).toDomain()
        val subtopic = json.decodeFromString<SubtopicDto>(
            """
            {
              "id": 20,
              "topic_id": 10,
              "slug": "filing",
              "title": "Filing and Alphabetizing",
              "order_index": 1
            }
            """.trimIndent(),
        ).toDomain()

        assertEquals("Clerical Ability", topic.title)
        assertTrue(topic.isPublished)
        assertEquals("Filing and Alphabetizing", subtopic.title)
        assertTrue(subtopic.isPublished)
    }

    @Test
    fun decodesBackendLessonResponseWithoutTopLevelTitle() {
        val json = Json { ignoreUnknownKeys = true }
        val lesson = json.decodeFromString<LessonDto>(
            """
            {
              "id": 30,
              "subtopic_id": 20,
              "status": "PUBLISHED",
              "content_json": {
                "metadata": {
                  "title": "Filing Basics"
                },
                "sections": [
                  {
                    "title": "Overview",
                    "blocks": [
                      { "type": "prose", "content": { "text": "Sort records by rule." } }
                    ]
                  }
                ]
              }
            }
            """.trimIndent(),
        ).toDomain()

        assertEquals("Filing Basics", lesson.title)
        assertEquals("PUBLISHED", lesson.status)
    }

    @Test
    fun mapsTypedLessonBlocksToDomainBlocks() {
        val content = Json.parseToJsonElement(
            """
            {
              "sections": [
                {
                  "title": "Tables",
                  "blocks": [
                    {
                      "type": "table",
                      "content": {
                        "headers": ["Rule", "Example"],
                        "rows": [["Subject", "The learner"], ["Verb", "answers"]]
                      }
                    },
                    {
                      "type": "check_understanding",
                      "content": [
                        {
                          "question": "Which verb agrees?",
                          "answer": "answers",
                          "rationale": "Singular subject."
                        }
                      ]
                    }
                  ]
                }
              ]
            }
            """.trimIndent(),
        )

        val lesson = LessonDto(
            id = 1,
            subtopicId = 2,
            title = "Agreement",
            status = "published",
            contentJson = content,
        ).toDomain()

        val table = lesson.sections.single().blocks[0]
        val check = lesson.sections.single().blocks[1]
        assertEquals(listOf("Rule", "Example"), table.headers)
        assertEquals("Subject", table.rows.first().first())
        assertEquals("Which verb agrees?", check.checks.single().question)
    }

    @Test
    fun unknownLessonBlocksUseSafeFallbackText() {
        val content = Json.parseToJsonElement(
            """
            {
              "sections": [
                {
                  "title": "Future block",
                  "blocks": [
                    {
                      "type": "immersive_simulation",
                      "fallback_text": "Open the web app for the simulation.",
                      "content": { "id": "sim-1" }
                    }
                  ]
                }
              ]
            }
            """.trimIndent(),
        )

        val block = LessonDto(
            id = 1,
            subtopicId = 2,
            title = "Simulation",
            status = "published",
            contentJson = content,
        ).toDomain().sections.single().blocks.single()

        assertEquals("immersive_simulation", block.type)
        assertEquals("Open the web app for the simulation.", block.fallbackText)
        assertTrue(block.text.isNotBlank())
    }

    @Test
    fun mapsSegmentedLessonsAndPracticeMetadata() {
        val content = Json.parseToJsonElement(
            """
            {
              "summary": "Learn in focused chunks.",
              "is_segmented": true,
              "segments": [
                {
                  "index": 0,
                  "estimated_minutes": 5,
                  "sections": [
                    {
                      "title": "Chunk 1",
                      "blocks": [
                        { "type": "prose", "content": { "text": "Read this first." } }
                      ]
                    }
                  ],
                  "checks": [
                    {
                      "question": "What comes first?",
                      "answer": "Read.",
                      "rationale": "The first segment starts with reading."
                    }
                  ]
                }
              ],
              "practice_problems": [
                {
                  "number": 1,
                  "question": "Try it?",
                  "answer": "Yes",
                  "explanation": "Practice reinforces the segment.",
                  "difficulty": "easy"
                }
              ],
              "memory_aids": ["Chunk before speed."],
              "exam_strategies": ["Eliminate distractors."]
            }
            """.trimIndent(),
        )

        val lesson = LessonDto(
            id = 7,
            subtopicId = 8,
            title = "Segmented",
            status = "published",
            contentJson = content,
        ).toDomain()

        assertTrue(lesson.isSegmented)
        assertEquals(5, lesson.segments.single().estimatedMinutes)
        assertEquals("What comes first?", lesson.segments.single().checks.single().question)
        assertEquals("Try it?", lesson.practiceProblems.single().question)
        assertEquals("Chunk before speed.", lesson.memoryAids.single())
        assertEquals("Eliminate distractors.", lesson.examStrategies.single())
    }

    @Test
    fun mapsLessonFreshnessMetadataAndPreservesItForCaching() {
        val content = Json.parseToJsonElement(
            """
            {
              "metadata": {
                "schema_version": 2,
                "content_version": "2026-06-08T00:00:00Z",
                "etag": "lesson-1001-v2",
                "content_hash": "sha256:abc123",
                "updated_at": "2026-06-08T00:00:00Z"
              },
              "sections": [
                {
                  "title": "Overview",
                  "blocks": [
                    { "type": "prose", "content": { "text": "Freshness metadata should round-trip." } }
                  ]
                }
              ]
            }
            """.trimIndent(),
        )

        val lesson = LessonDto(
            id = 11,
            subtopicId = 12,
            title = "Freshness",
            status = "published",
            contentJson = content,
        ).toDomain()

        val cached = CachedLesson.from(lesson).toDomain()

        assertEquals(2, lesson.freshness?.schemaVersion)
        assertEquals("2026-06-08T00:00:00Z", lesson.freshness?.contentVersion)
        assertEquals("lesson-1001-v2", lesson.freshness?.etag)
        assertEquals("sha256:abc123", lesson.freshness?.contentHash)
        assertEquals("2026-06-08T00:00:00Z", lesson.freshness?.updatedAt)
        assertEquals(lesson.freshness, cached.freshness)
    }
}
