# Implementation Plan: Smart Chat Engine

## Overview

Upgrade the stateless keyword-matching `lesson_chat_engine.py` to a context-aware conversational engine with multi-turn tracking, discourse-aware intent classification, Socratic questioning, cross-lesson awareness, adaptive complexity, and composable templates. All new modules live under `app/features/tutor/algorithms/` with template data under `data/chat_templates/`. The existing `generate_chat_response` signature is replaced with a new keyword-arg interface returning `ChatResult`.

## Tasks

- [x] 1. Define core data models and enums
  - [x] 1.1 Create `app/features/tutor/algorithms/chat_models.py` with dataclasses and enums
    - Define `ComplexityLevel` enum (SIMPLIFIED, STANDARD, DETAILED)
    - Define `DiscourseState` enum (INITIAL, FOLLOW_UP, QUIZ_PENDING, SOCRATIC_EXCHANGE, CLARIFICATION)
    - Define `MasteryLevel` references (BEGINNER, FAMILIAR, PROFICIENT, ADVANCED, MASTERED)
    - Define `TopicThread`, `SocraticState`, `ComplexityOverride`, `Exchange`, `ConversationContext` dataclasses
    - Define `ResolvedMessage`, `IntentScore`, `ClassificationResult`, `SocraticPrompt`, `SocraticEvaluation`, `ChatResult` dataclasses
    - Define `ConceptEntry`, `TemplatePart`, `ResponseTemplate` dataclasses
    - _Requirements: 1.1, 1.6, 2.1, 3.2, 5.1, 6.1, 7.1_

  - [x] 1.2 Update `app/features/tutor/schemas.py` with new request/response schemas
    - Add `context_json: dict | None = None` field to `LessonChatRequest`
    - Keep deprecated `history` field for backward compatibility
    - Add `detected_intent: str` and `context_json: dict` to `LessonChatResponse`
    - _Requirements: 7.1, 7.2_

- [x] 2. Implement Context Manager
  - [x] 2.1 Create `app/features/tutor/algorithms/context_manager.py`
    - Implement `ContextManager.build_context()` that deserializes or creates fresh `ConversationContext`
    - Implement schema version validation and migration logic
    - Implement `serialize()` method producing JSON-compatible dict with `schema_version`
    - Implement `update_context()` that appends exchange, updates discourse state, manages topic threads
    - Implement `evict_oldest()` maintaining the 10-exchange window with topic thread subject preservation
    - Implement `detect_topic_shift()` based on key term disjointness and absence of anaphoric references
    - Handle malformed context gracefully — return fresh context on validation failure
    - _Requirements: 1.1, 1.4, 1.6, 1.7, 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 2.2 Write property test for context exchange window invariant
    - **Property 1: Context exchange window invariant**
    - **Validates: Requirements 1.6, 1.7**

  - [x] 2.3 Write property test for topic shift detection
    - **Property 3: Topic shift detection on term disjointness**
    - **Validates: Requirements 1.4**

  - [x] 2.4 Write property test for context serialization round-trip
    - **Property 17: Context serialization round-trip**
    - **Validates: Requirements 7.2, 7.3**

  - [x] 2.5 Write property test for malformed context graceful recovery
    - **Property 18: Malformed context graceful recovery**
    - **Validates: Requirements 7.4**

- [x] 3. Implement Anaphora Resolver
  - [x] 3.1 Create `app/features/tutor/algorithms/anaphora_resolver.py`
    - Define `ANAPHORIC_PATTERNS` for pronouns and demonstratives ("it", "that", "this", "the concept", etc.)
    - Implement `resolve()` method that matches anaphoric references and resolves to most recent active topic thread subject
    - Return `ResolvedMessage` with confidence score, candidate list, and chosen referent
    - When no candidate scores above threshold, return `referent=None` with candidates list for clarification
    - _Requirements: 1.2, 1.5_

  - [x] 3.2 Write property test for anaphora resolution targets most recent thread subject
    - **Property 2: Anaphora resolution targets most recent thread subject**
    - **Validates: Requirements 1.2**

- [x] 4. Implement Intent Classifier
  - [x] 4.1 Create `app/features/tutor/algorithms/intent_classifier.py`
    - Implement scoring-based classifier with base score from regex pattern match (0.0–0.6)
    - Add discourse bonus (+0.3) when intent aligns with current discourse state expectations
    - Add thread continuity bonus (+0.1) when intent continues current topic thread
    - Cap final score at 1.0
    - Handle `quiz_pending` state: messages ≤ 30 chars classify as `quiz_answer_attempt`
    - Handle post-explanation follow-ups as deeper explanation requests
    - When all scores < 0.4 with ≥ 2 candidates, return disambiguation with top 2 options
    - When all scores < 0.4 with < 2 candidates, return open-ended clarifying prompt
    - When tied scores, prefer thread-continuing intent
    - Add new intents: `conceptual_question`, `direct_answer_request`, `quiz_answer_attempt`, `complexity_adjustment`, `cross_reference_request`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 4.2 Write property test for short message classified as quiz answer in quiz-pending state
    - **Property 4: Short message classified as quiz answer in quiz-pending state**
    - **Validates: Requirements 2.2**

  - [x] 4.3 Write property test for discourse state disambiguates intent
    - **Property 5: Discourse state disambiguates intent for identical messages**
    - **Validates: Requirements 2.1**

  - [x] 4.4 Write property test for thread-continuing intent wins ties
    - **Property 6: Thread-continuing intent wins ties**
    - **Validates: Requirements 2.4**

  - [x] 4.5 Write property test for low-confidence triggers disambiguation
    - **Property 7: Low-confidence triggers disambiguation**
    - **Validates: Requirements 2.5**


- [x] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement Socratic Module
  - [x] 6.1 Create `app/features/tutor/algorithms/socratic_module.py`
    - Implement `should_activate()` checking intent is `conceptual_question`, mastery ≥ FAMILIAR, not at max attempts, no direct answer request
    - Implement `generate_guiding_question()` selecting from predefined templates categorized by reasoning type (definition_recall, comparison, application, cause_effect) with ≥ 3 templates per type
    - Implement `evaluate_response()` that checks ≥ 2 key terms matched → `understood=True`, < 2 → `understood=False`
    - Track attempts up to 3; after 3 consecutive fails, signal escalation to direct answer
    - On successful evaluation, support extending with cross-lesson insight
    - Honor explicit `direct_answer_request` intent to bypass Socratic mode
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

  - [x] 6.2 Write property test for Socratic activation at FAMILIAR+
    - **Property 8: Socratic activation for conceptual questions at FAMILIAR+**
    - **Validates: Requirements 3.1, 3.2**

  - [x] 6.3 Write property test for Socratic evaluation partitions on key term match
    - **Property 9: Socratic evaluation partitions on key term match count**
    - **Validates: Requirements 3.3, 3.4**

  - [x] 6.4 Write property test for Socratic inactive for BEGINNER mastery
    - **Property 10: Socratic inactive for BEGINNER mastery**
    - **Validates: Requirements 3.7**

- [x] 7. Implement Cross-Lesson Registry
  - [x] 7.1 Create `app/features/tutor/algorithms/cross_lesson_registry.py`
    - Implement `CrossLessonRegistry.build_from_lessons()` that extracts key_takeaways (normalized to 1–5 word phrases), section headings, and prerequisite relationships
    - Implement `find_related()` that matches terms from current context to other subtopics
    - Limit cross-references to at most 2 per response, each ≤ 150 characters and single sentence
    - Differentiate behavior: mastery data exists → note connection; no mastery data → mention as future learning
    - Support comparison responses when user explicitly asks how topics relate
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

  - [x] 7.2 Write property test for cross-lesson registry completeness
    - **Property 11: Cross-lesson registry completeness**
    - **Validates: Requirements 4.1**

  - [x] 7.3 Write property test for cross-reference output constraints
    - **Property 12: Cross-reference output constraints**
    - **Validates: Requirements 4.3, 4.6**

- [x] 8. Implement Template System
  - [x] 8.1 Create `app/features/tutor/algorithms/template_loader.py`
    - Implement `TemplateLoader.load()` that reads JSON files from `data/chat_templates/` directory
    - Implement `get_template()` returning `ResponseTemplate` for a given intent-complexity combo
    - Fall back to `fallback.json` template when intent file missing; log warning
    - Validate template structure on load (≥ 3 variants per opener/closing per intent-complexity)
    - _Requirements: 6.1, 6.3, 6.6_

  - [x] 8.2 Create template data files under `data/chat_templates/`
    - Create JSON template files for all intents: `explain_section.json`, `give_example.json`, `summarize.json`, `quiz_me.json`, `relate_to_exam.json`, `memory_aid.json`, `next_step.json`, `greeting.json`, `thanks.json`, `conceptual_question.json`, `direct_answer_request.json`, `quiz_answer_attempt.json`, `complexity_adjustment.json`, `cross_reference_request.json`, `socratic_prompt.json`, `fallback.json`
    - Each file contains SIMPLIFIED, STANDARD, DETAILED variants with ≥ 3 openers and ≥ 3 closings
    - _Requirements: 6.1, 6.3, 6.6_

- [x] 9. Implement Response Generator
  - [x] 9.1 Create `app/features/tutor/algorithms/response_generator.py`
    - Implement complexity level computation: score < 0.3 → SIMPLIFIED, 0.3 ≤ score ≤ 0.7 → STANDARD, score > 0.7 → DETAILED, None → STANDARD
    - Implement complexity override logic (active for current + next 3 responses, then revert)
    - Implement `_select_template()` with variant cycling — no two adjacent same-intent responses use same variant
    - Implement `_compose_response()` assembling parts: opener + core content + cross_reference + closing
    - Ensure core content is always non-empty; cross_reference and closing may be omitted
    - Place cross-references after core content and before closing prompt
    - Enforce SIMPLIFIED constraints (≤ 20 word avg sentences, no jargon without inline definition, concrete analogy)
    - Enforce STANDARD constraints (domain terms with ≤ 8-word parenthetical, one example)
    - Enforce DETAILED constraints (no inline definitions, edge case reference, exam application)
    - Reset variant usage tracking when all variants exhausted, starting from random selection
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 9.2 Write property test for complexity level mapping
    - **Property 14: Complexity level mapping**
    - **Validates: Requirements 5.1, 5.7**

  - [x] 9.3 Write property test for complexity override lifetime
    - **Property 15: Complexity override lifetime**
    - **Validates: Requirements 5.5, 5.6**

  - [x] 9.4 Write property test for template variant non-repetition
    - **Property 16: Template variant non-repetition**
    - **Validates: Requirements 6.4**

  - [x] 9.5 Write property test for cross-reference placement ordering
    - **Property 13: Cross-reference placement ordering**
    - **Validates: Requirements 4.8**

  - [x] 9.6 Write property test for response always contains core content
    - **Property 19: Response always contains core content**
    - **Validates: Requirements 6.2**

- [x] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 11. Implement Engine Orchestrator
  - [x] 11.1 Rewrite `app/features/tutor/algorithms/lesson_chat_engine.py` with new `generate_chat_response` signature
    - Replace old signature with `generate_chat_response(*, content_json, message, active_section_index, context_json, mastery_score, mastery_level, cross_lesson_registry) → ChatResult`
    - Wire orchestration: ContextManager → AnaphoraResolver → IntentClassifier → SocraticModule → ResponseGenerator
    - Handle clarification responses when anaphora resolution fails (present ≤ 2 candidates)
    - Handle disambiguation responses when intent confidence < 0.4
    - Detect and handle complexity adjustment intents (override for current + 3 responses)
    - Return `ChatResult` with response_text, detected_intent, and serialized context_json
    - Maintain backward compatibility: if `context_json` is None, start fresh
    - _Requirements: 1.1, 1.3, 1.5, 2.1, 2.5, 2.6, 3.1, 3.5, 3.6, 4.7, 5.5, 7.1_

- [x] 12. Integrate with Service Layer
  - [x] 12.1 Update `app/features/tutor/service.py` to pass mastery data and registry to engine
    - Fetch `UserSubtopicMastery` for current user + subtopic
    - Pass `mastery_score` and `mastery_level` to `generate_chat_response`
    - Build or inject `CrossLessonRegistry` (lazy-loaded singleton at app startup)
    - Pass `context_json` from request to engine; return updated `context_json` in response
    - Wrap engine call in try/except; on failure, return fallback response using fallback template
    - _Requirements: 4.2, 5.1, 5.7, 7.1_

  - [x] 12.2 Register `CrossLessonRegistry` initialization at app startup
    - Add startup event or lifespan handler in `app/main.py` that builds registry from all lesson content_json records
    - Expose registry via dependency injection for the tutor service
    - _Requirements: 4.1, 4.2_

- [x] 13. Write unit tests for all algorithm modules
  - [x] 13.1 Create `tests/features/tutor/algorithms/test_context_manager.py`
    - Test context construction from None (fresh), valid dict, malformed dict
    - Test exchange eviction at 10 exchanges with topic thread subject preservation
    - Test topic shift detection for disjoint terms
    - Test serialization/deserialization round-trip
    - Test schema version migration
    - _Requirements: 1.1, 1.4, 1.6, 1.7, 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 13.2 Create `tests/features/tutor/algorithms/test_anaphora_resolver.py`
    - Test pronoun resolution to most recent thread subject
    - Test resolution when no candidates found (returns None referent)
    - Test confidence scoring for ambiguous vs clear references
    - _Requirements: 1.2, 1.5_

  - [x] 13.3 Create `tests/features/tutor/algorithms/test_intent_classifier.py`
    - Test quiz_pending + short message → quiz_answer_attempt
    - Test post-explanation follow-up → deeper explanation request
    - Test discourse bonus changes winner between identical messages
    - Test tie-breaking favors thread-continuing intent
    - Test low confidence returns disambiguation options
    - Test all new intent patterns match expected messages
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 13.4 Create `tests/features/tutor/algorithms/test_socratic_module.py`
    - Test activation at FAMILIAR+ with conceptual_question intent
    - Test inactive at BEGINNER
    - Test evaluation: ≥ 2 key terms → understood, < 2 → not understood
    - Test escalation after 3 failed attempts
    - Test direct answer request bypasses Socratic mode
    - Test question template selection covers all reasoning types
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

  - [x] 13.5 Create `tests/features/tutor/algorithms/test_cross_lesson_registry.py`
    - Test building from lesson content with key_takeaways and section headings
    - Test find_related returns concepts from other subtopics only
    - Test max 2 cross-references limit
    - Test 150-char constraint on cross-reference text
    - _Requirements: 4.1, 4.2, 4.3, 4.6_

  - [x] 13.6 Create `tests/features/tutor/algorithms/test_response_generator.py`
    - Test complexity level computation for boundary values
    - Test override activation and expiry
    - Test variant non-repetition across consecutive same-intent responses
    - Test composed response structure (opener → core → cross-ref → closing)
    - Test template fallback when intent file missing
    - _Requirements: 5.1, 5.5, 5.6, 6.1, 6.2, 6.4_

- [x] 14. Update service and router tests
  - [x] 14.1 Update `tests/features/tutor/test_service.py` with new chat flow tests
    - Test happy path with mastery data, valid context, response includes updated context_json
    - Test no mastery data defaults to STANDARD complexity
    - Test malformed context_json starts fresh (no crash)
    - Test engine exception caught and fallback response returned
    - _Requirements: 5.7, 7.4_

  - [x] 14.2 Update `tests/features/tutor/test_router.py` with new endpoint contract
    - Test POST `/v1/tutor/lesson-chat` with `context_json` returns 200 with response including `context_json` and `detected_intent`
    - Test request without `context_json` (backward compat) returns fresh context
    - Test invalid message (empty) returns 422
    - _Requirements: 7.1_

- [x] 15. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The engine remains purely rule-based — no LLM or external API calls
- Template data files under `data/chat_templates/` decouple content from code
- The `CrossLessonRegistry` is built once at startup; no per-request DB queries for concept lookup

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "3.1", "8.1", "8.2"] },
    { "id": 2, "tasks": ["2.2", "2.3", "2.4", "2.5", "3.2", "4.1"] },
    { "id": 3, "tasks": ["4.2", "4.3", "4.4", "4.5", "6.1", "7.1"] },
    { "id": 4, "tasks": ["6.2", "6.3", "6.4", "7.2", "7.3", "9.1"] },
    { "id": 5, "tasks": ["9.2", "9.3", "9.4", "9.5", "9.6", "11.1"] },
    { "id": 6, "tasks": ["12.1", "12.2"] },
    { "id": 7, "tasks": ["13.1", "13.2", "13.3", "13.4", "13.5", "13.6"] },
    { "id": 8, "tasks": ["14.1", "14.2"] }
  ]
}
```
