# Design Document: Smart Chat Engine

## Overview

This design upgrades the existing stateless `lesson_chat_engine.py` into a context-aware conversational engine. The engine remains purely rule-based (no LLM, no external APIs) but adds:

1. **Multi-turn conversation context** — a serializable `ConversationContext` data structure that tracks topic threads, discourse state, and anaphoric references across up to 10 exchanges.
2. **Discourse-aware intent classification** — a scoring-based classifier that uses conversation state as a disambiguation signal, replacing the current first-match regex approach.
3. **Socratic questioning** — a sub-module that conditionally generates guiding questions instead of direct answers based on mastery level and response history.
4. **Cross-lesson awareness** — a concept registry built from lesson metadata that enables contextual cross-references.
5. **Adaptive complexity** — response generation that adjusts vocabulary, sentence length, and example depth based on the learner's mastery score.
6. **Composable template system** — a declarative template format loaded from external JSON/YAML data files, replacing hardcoded response strings.

The engine's public interface changes from `generate_chat_response(content_json, message, active_section_index, history) → (str, str)` to `generate_chat_response(content_json, message, active_section_index, context, mastery_data, registry) → ChatResult` where `ChatResult` contains the response text, detected intent, and updated serialized context.

The existing `TutorService.lesson_chat()` orchestration point remains; it gains responsibility for fetching mastery data and passing it to the engine. The frontend continues to own conversation persistence — the serialized context replaces the flat `history[]` list.

## Architecture

```mermaid
flowchart TD
    subgraph Frontend ["Frontend (React PWA)"]
        UI[Chat UI Component]
        LS[LocalStorage / IndexedDB]
    end

    subgraph Backend ["Backend (FastAPI)"]
        R[POST /v1/tutor/lesson-chat]
        S[TutorService.lesson_chat]
        subgraph Engine ["Smart Chat Engine"]
            CTX[Context Manager]
            IC[Intent Classifier]
            AR[Anaphora Resolver]
            SM[Socratic Module]
            RG[Response Generator]
            TL[Template Loader]
        end
        CLR[Cross-Lesson Registry]
        MR[MasteryRepository]
    end

    subgraph Data ["Data Layer"]
        TD[Template Data Files<br/>data/chat_templates/]
        LD[Lesson Content JSON]
        DB[(user_subtopic_mastery)]
    end

    UI -->|POST {subtopic_id, message, context_json}| R
    R --> S
    S -->|fetch mastery| MR
    MR --> DB
    S -->|load lesson| LD
    S --> CTX
    CTX --> AR
    CTX --> IC
    IC --> SM
    IC --> RG
    SM --> RG
    RG --> TL
    TL --> TD
    RG -->|cross-ref lookup| CLR
    CLR --> LD
    S -->|ChatResult| R
    R -->|{response_text, intent, context_json}| UI
    UI -->|persist context| LS
```

### Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Context lives on frontend, passed per-request | Zero server-side session state; works with stateless Render deployment; context survives backend restarts |
| Scoring-based intent classifier (not first-match regex) | Enables discourse-aware disambiguation; same message maps to different intents based on state |
| Templates as external JSON files under `data/chat_templates/` | Decouples content authoring from code changes; aligns with existing `data/seed/` pattern |
| Cross-Lesson Registry built at startup from lesson metadata | Avoids per-request DB queries for concept lookup; lessons change only on seed/migration |
| Mastery data fetched by service layer, not engine | Engine remains a pure function with injected dependencies; easier to test |

## Components and Interfaces

### 1. Context Manager (`context_manager.py`)

Responsible for constructing, updating, serializing, and deserializing `ConversationContext`.

```python
@dataclass
class TopicThread:
    subject: str                    # normalized concept string
    start_exchange_index: int       # when thread started
    key_terms: list[str]            # terms associated with this thread
    is_active: bool

@dataclass
class SocraticState:
    active: bool
    target_concept: str | None
    key_terms: list[str]            # up to 3 terms expected in learner answer
    attempts: int                   # count of guiding questions sent (max 3)
    reasoning_type: str | None      # definition_recall | comparison | application | cause_effect

@dataclass
class ComplexityOverride:
    level: ComplexityLevel
    remaining_responses: int        # counts down from 3

@dataclass
class Exchange:
    user_message: str
    assistant_response: str
    intent: str
    topic_thread_subject: str

@dataclass
class ConversationContext:
    schema_version: int             # currently 1
    exchanges: list[Exchange]       # max 10
    topic_threads: list[TopicThread]  # max 4 (1 active + 3 preserved)
    discourse_state: DiscourseState
    socratic_state: SocraticState
    complexity_override: ComplexityOverride | None
    template_usage: dict[str, list[int]]  # intent → list of variant indices used

class ContextManager:
    def build_context(self, serialized: dict | None) -> ConversationContext: ...
    def update_context(self, ctx: ConversationContext, user_msg: str, response: str, intent: str) -> ConversationContext: ...
    def serialize(self, ctx: ConversationContext) -> dict: ...
    def detect_topic_shift(self, ctx: ConversationContext, message: str) -> bool: ...
    def evict_oldest(self, ctx: ConversationContext) -> ConversationContext: ...
```

### 2. Anaphora Resolver (`anaphora_resolver.py`)

Resolves pronouns and demonstratives to referents from topic thread history.

```python
class AnaphoraResolver:
    ANAPHORIC_PATTERNS: list[re.Pattern]  # "it", "that", "this", "the concept", etc.

    def resolve(self, message: str, ctx: ConversationContext) -> ResolvedMessage:
        """Returns message with references resolved to explicit terms,
        plus confidence score and candidate list."""
        ...

@dataclass
class ResolvedMessage:
    original: str
    resolved: str                   # message with pronouns replaced
    confidence: float               # 0.0 - 1.0
    candidates: list[str]           # candidate referents considered
    referent: str | None            # chosen referent (None if ambiguous)
```

### 3. Intent Classifier (`intent_classifier.py`)

Scoring-based classifier that replaces the current first-match regex approach.

```python
class DiscourseState(str, Enum):
    INITIAL = "initial"
    FOLLOW_UP = "follow_up"
    QUIZ_PENDING = "quiz_pending"
    SOCRATIC_EXCHANGE = "socratic_exchange"
    CLARIFICATION = "clarification"

@dataclass
class IntentScore:
    intent: str
    score: float                    # 0.0 - 1.0
    source: str                     # "pattern" | "discourse" | "context"

class IntentClassifier:
    CONFIDENCE_THRESHOLD: float = 0.4

    def classify(
        self,
        message: str,
        resolved_message: ResolvedMessage,
        ctx: ConversationContext,
    ) -> ClassificationResult: ...

@dataclass
class ClassificationResult:
    intent: str
    confidence: float
    all_scores: list[IntentScore]
    needs_disambiguation: bool
    disambiguation_options: list[str] | None
```

Intent scoring formula:
- **Base score**: regex pattern match strength (0.0–0.6)
- **Discourse bonus**: +0.3 if intent aligns with current discourse state expectations
- **Thread continuity bonus**: +0.1 if intent continues current topic thread
- Final score capped at 1.0

New intents added beyond current set:
- `conceptual_question` — why/how/relationship questions (Socratic trigger)
- `direct_answer_request` — explicit "just tell me", "give me the answer"
- `quiz_answer_attempt` — response to a pending quiz
- `complexity_adjustment` — "explain simpler", "go deeper"
- `cross_reference_request` — "how does this relate to X"

### 4. Socratic Module (`socratic_module.py`)

```python
class SocraticModule:
    def should_activate(self, intent: str, mastery_level: MasteryLevel, ctx: ConversationContext) -> bool: ...
    def generate_guiding_question(self, concept: str, section_content: str, reasoning_type: str) -> SocraticPrompt: ...
    def evaluate_response(self, message: str, socratic_state: SocraticState) -> SocraticEvaluation: ...

@dataclass
class SocraticPrompt:
    question: str
    target_concept: str
    key_terms: list[str]            # up to 3
    reasoning_type: str

@dataclass
class SocraticEvaluation:
    understood: bool                # ≥2 key terms matched
    matched_terms: list[str]
    should_escalate: bool           # True after 3 failed attempts
```

Activation rules:
- Intent is `conceptual_question`
- Mastery level is FAMILIAR or higher (score ≥ 0.2)
- Not already at max attempts (3)
- User hasn't explicitly requested direct answer

### 5. Cross-Lesson Registry (`cross_lesson_registry.py`)

```python
@dataclass
class ConceptEntry:
    term: str                       # normalized 1-5 word phrase
    subtopic_id: int
    subtopic_title: str
    source: str                     # "key_takeaway" | "section_heading" | "prerequisite"

class CrossLessonRegistry:
    _concepts: dict[str, list[ConceptEntry]]  # term → entries

    @classmethod
    def build_from_lessons(cls, lessons: list[dict]) -> CrossLessonRegistry: ...
    def find_related(self, terms: list[str], current_subtopic_id: int) -> list[ConceptEntry]: ...
    def find_by_subtopic(self, subtopic_id: int) -> list[ConceptEntry]: ...
```

The registry is built once at application startup (or lazily on first use) by iterating all lesson `content_json` records and extracting:
- `key_takeaways` → split into normalized phrases
- `sections[*].title` → each section heading as a concept
- `metadata.prerequisites` → prerequisite subtopic IDs as relationships

### 6. Response Generator (`response_generator.py`)

```python
class ComplexityLevel(str, Enum):
    SIMPLIFIED = "SIMPLIFIED"       # score < 0.3
    STANDARD = "STANDARD"           # 0.3 ≤ score ≤ 0.7
    DETAILED = "DETAILED"           # score > 0.7

class ResponseGenerator:
    def generate(
        self,
        intent: str,
        content_json: dict,
        ctx: ConversationContext,
        complexity: ComplexityLevel,
        cross_refs: list[ConceptEntry],
        socratic_prompt: SocraticPrompt | None,
        active_section_index: int | None,
    ) -> str: ...

    def _select_template(self, intent: str, complexity: ComplexityLevel, ctx: ConversationContext) -> ResponseTemplate: ...
    def _compose_response(self, template: ResponseTemplate, parts: dict[str, str]) -> str: ...
```

### 7. Template Loader (`template_loader.py`)

```python
@dataclass
class TemplatePart:
    key: str                        # "opener" | "core" | "cross_reference" | "closing"
    variants: list[str]             # at least 3 per intent-complexity combo

@dataclass  
class ResponseTemplate:
    intent: str
    complexity: ComplexityLevel
    parts: dict[str, TemplatePart]

class TemplateLoader:
    _templates: dict[str, dict[ComplexityLevel, ResponseTemplate]]

    @classmethod
    def load(cls, templates_dir: Path) -> TemplateLoader: ...
    def get_template(self, intent: str, complexity: ComplexityLevel) -> ResponseTemplate: ...
```

Template files stored at `data/chat_templates/{intent}.json`:

```json
{
  "intent": "explain_section",
  "variants": {
    "SIMPLIFIED": {
      "opener": [
        "Let me break this down simply. ",
        "Here's the easy version. ",
        "Think of it this way. "
      ],
      "core": "{content}",
      "cross_reference": "By the way, this connects to {related_topic} which you've studied before. ",
      "closing": [
        "Want me to give you an example?",
        "Does that make more sense now?",
        "Should I explain any part differently?"
      ]
    },
    "STANDARD": { ... },
    "DETAILED": { ... }
  }
}
```

### 8. Engine Orchestrator (updated `lesson_chat_engine.py`)

The main entry point ties all components together:

```python
@dataclass
class ChatResult:
    response_text: str
    detected_intent: str
    context_json: dict              # serialized ConversationContext for frontend

def generate_chat_response(
    *,
    content_json: dict[str, Any],
    message: str,
    active_section_index: int | None = None,
    context_json: dict | None = None,
    mastery_score: float | None = None,
    mastery_level: str | None = None,
    cross_lesson_registry: CrossLessonRegistry | None = None,
) -> ChatResult:
    """Main entry point for the smart chat engine.
    
    Replaces the old generate_chat_response signature.
    Backward-compatible: if context_json is None, starts fresh.
    """
    ...
```

## Data Models

### ConversationContext Schema (JSON serialization format)

```json
{
  "schema_version": 1,
  "exchanges": [
    {
      "user_message": "What is subject-verb agreement?",
      "assistant_response": "Subject-verb agreement means...",
      "intent": "explain_section",
      "topic_thread_subject": "subject-verb agreement"
    }
  ],
  "topic_threads": [
    {
      "subject": "subject-verb agreement",
      "start_exchange_index": 0,
      "key_terms": ["subject", "verb", "agreement", "singular", "plural"],
      "is_active": true
    }
  ],
  "discourse_state": "follow_up",
  "socratic_state": {
    "active": false,
    "target_concept": null,
    "key_terms": [],
    "attempts": 0,
    "reasoning_type": null
  },
  "complexity_override": null,
  "template_usage": {
    "explain_section": [0, 2]
  }
}
```

### Updated API Contract

**Request** (enhanced `LessonChatRequest`):

```python
class LessonChatRequest(BaseModel):
    subtopic_id: int
    message: str = Field(min_length=1, max_length=1000)
    active_section_index: int | None = None
    context_json: dict | None = None   # replaces history[]
    # Deprecated: history field kept for backward compat, ignored if context_json present
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)
```

**Response** (enhanced `LessonChatResponse`):

```python
class LessonChatResponse(BaseModel):
    interaction_id: int
    response_text: str
    detected_intent: str
    context_json: dict                  # serialized ConversationContext for frontend to persist
```

### Cross-Lesson Registry Data Structure (in-memory)

```python
# Built from all lesson content_json at startup
registry = {
    "subject-verb agreement": [
        ConceptEntry(term="subject-verb agreement", subtopic_id=42, subtopic_title="Subject-Verb Agreement", source="section_heading"),
    ],
    "singular plural": [
        ConceptEntry(term="singular plural", subtopic_id=42, subtopic_title="Subject-Verb Agreement", source="key_takeaway"),
        ConceptEntry(term="singular plural", subtopic_id=45, subtopic_title="Noun Forms", source="key_takeaway"),
    ],
}
```

### Template Data File Structure

```
data/
└── chat_templates/
    ├── explain_section.json
    ├── give_example.json
    ├── summarize.json
    ├── quiz_me.json
    ├── relate_to_exam.json
    ├── memory_aid.json
    ├── next_step.json
    ├── greeting.json
    ├── thanks.json
    ├── conceptual_question.json
    ├── direct_answer_request.json
    ├── quiz_answer_attempt.json
    ├── complexity_adjustment.json
    ├── cross_reference_request.json
    ├── socratic_prompt.json
    └── fallback.json
```

### Mastery Integration (no new models — uses existing)

The service layer fetches `UserSubtopicMastery` for the current user+subtopic and passes `mastery_score` and `mastery_level` to the engine. No schema changes to the mastery models.



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Context exchange window invariant

*For any* sequence of N user-assistant exchanges (N ≥ 1) added to a ConversationContext, the context SHALL contain at most 10 exchanges, the oldest SHALL be evicted first, and any TopicThread subject from an evicted exchange SHALL remain in the topic_threads list if that thread is still referenced by exchanges within the window.

**Validates: Requirements 1.6, 1.7**

### Property 2: Anaphora resolution targets most recent thread subject

*For any* message containing an anaphoric reference (pronoun or demonstrative) and a ConversationContext with an active TopicThread, the AnaphoraResolver SHALL resolve the reference to the subject of the most recent active TopicThread.

**Validates: Requirements 1.2**

### Property 3: Topic shift detection on term disjointness

*For any* user message and active TopicThread, if the message shares zero key terms with the thread's subject AND contains no anaphoric references, the ContextManager SHALL detect a topic shift and start a new TopicThread.

**Validates: Requirements 1.4**

### Property 4: Short message classified as quiz answer in quiz-pending state

*For any* message of 30 characters or fewer, when the DiscourseState is `quiz_pending`, the IntentClassifier SHALL classify the message as `quiz_answer_attempt` regardless of message content.

**Validates: Requirements 2.2**

### Property 5: Discourse state disambiguates intent for identical messages

*For any* message that matches multiple intent patterns, the IntentClassifier SHALL produce different final intents when the DiscourseState differs, specifically: the discourse-aligned intent SHALL receive a scoring bonus that changes the winner.

**Validates: Requirements 2.1**

### Property 6: Thread-continuing intent wins ties

*For any* message that produces two or more intents with equal scores, the IntentClassifier SHALL select the intent that continues the current active TopicThread over one that would start a new thread.

**Validates: Requirements 2.4**

### Property 7: Low-confidence triggers disambiguation

*For any* message where all intent candidate scores are below 0.4 and at least two candidates exist, the Chat_Engine SHALL produce a disambiguation response presenting exactly the top two candidates as options.

**Validates: Requirements 2.5**

### Property 8: Socratic activation for conceptual questions at FAMILIAR+

*For any* message classified as `conceptual_question` and any mastery_level in {FAMILIAR, PROFICIENT, ADVANCED, MASTERED}, the SocraticModule SHALL activate and produce a guiding question rather than a direct answer, and the SocraticState SHALL contain a non-null target_concept with 1–3 key_terms.

**Validates: Requirements 3.1, 3.2**

### Property 9: Socratic evaluation partitions on key term match count

*For any* learner response to a Socratic question with stored key_terms of length K (1 ≤ K ≤ 3), if the response contains ≥ 2 of those terms the evaluation SHALL return `understood=True`, and if it contains < 2 the evaluation SHALL return `understood=False`.

**Validates: Requirements 3.3, 3.4**

### Property 10: Socratic inactive for BEGINNER mastery

*For any* message classified as `conceptual_question` and mastery_level = BEGINNER, the SocraticModule SHALL NOT activate and the Chat_Engine SHALL produce a direct explanation.

**Validates: Requirements 3.7**

### Property 11: Cross-lesson registry completeness

*For any* lesson content_json containing key_takeaways and sections with titles, building the CrossLessonRegistry SHALL produce entries for every key_takeaway phrase (normalized to 1–5 words) and every section heading, each mapped to the correct subtopic_id.

**Validates: Requirements 4.1**

### Property 12: Cross-reference output constraints

*For any* response that includes cross-references, there SHALL be at most 2 cross-references, and each cross-reference text SHALL be at most 150 characters and constitute a single sentence.

**Validates: Requirements 4.3, 4.6**

### Property 13: Cross-reference placement ordering

*For any* composed response containing cross-reference text, the cross-reference section SHALL appear after the core content section and before the closing prompt section in the final output string.

**Validates: Requirements 4.8**

### Property 14: Complexity level mapping

*For any* mastery_score in [0.0, 1.0], the computed ComplexityLevel SHALL be SIMPLIFIED when score < 0.3, STANDARD when 0.3 ≤ score ≤ 0.7, and DETAILED when score > 0.7. When mastery_score is None, the level SHALL be STANDARD.

**Validates: Requirements 5.1, 5.7**

### Property 15: Complexity override lifetime

*For any* complexity override triggered by a complexity adjustment phrase, the override SHALL be active for exactly the current response plus the next 3 responses in the same TopicThread (remaining_responses counts down from 3 to 0), and the response immediately after expiry SHALL use the mastery-computed ComplexityLevel.

**Validates: Requirements 5.5, 5.6**

### Property 16: Template variant non-repetition

*For any* sequence of consecutive responses with the same intent within a TopicThread, no two adjacent responses SHALL use the same template variant index for the opener or closing parts.

**Validates: Requirements 6.4**

### Property 17: Context serialization round-trip

*For any* valid ConversationContext, serializing to JSON and deserializing back SHALL produce a structurally equal ConversationContext where all fields contain the same values (i.e., `serialize(deserialize(serialize(ctx))) == serialize(ctx)`).

**Validates: Requirements 7.2, 7.3**

### Property 18: Malformed context graceful recovery

*For any* dict that fails ConversationContext validation (missing required fields, wrong types, or unrecognized schema_version), the ContextManager SHALL return a fresh default ConversationContext without raising an exception.

**Validates: Requirements 7.4**

### Property 19: Response always contains core content

*For any* valid combination of intent, ComplexityLevel, and ConversationContext, the composed response SHALL always include the core content template part (non-empty string).

**Validates: Requirements 6.2**

## Error Handling

### Input Validation Errors

| Scenario | Behavior |
|----------|----------|
| `message` empty or > 1000 chars | Pydantic rejects with 422 (existing behavior) |
| `context_json` is malformed/invalid | Engine discards it, starts fresh context (Property 18) — no error surfaced to user |
| `subtopic_id` not found | Service raises HTTPException 404 (existing behavior) |
| `active_section_index` out of bounds | Engine treats as None — falls back to keyword search (existing behavior) |

### Engine Internal Errors

| Scenario | Behavior |
|----------|----------|
| Template file missing for intent | `TemplateLoader.get_template()` falls back to `fallback.json` template; logs warning |
| Cross-lesson registry unavailable | Engine generates response without cross-references (Requirement 4.7 pattern) |
| Mastery data unavailable (user has no record) | Default to STANDARD complexity (Requirement 5.7) |
| Anaphora resolution fails (no candidates) | Ask clarifying question with candidate list (Requirement 1.5) |
| All intent scores below threshold | Disambiguation response (Requirements 2.5, 2.6) |
| Socratic key term matching finds zero terms | Treat as "not understood" — provide narrower guiding question |

### Schema Migration Errors

| Scenario | Behavior |
|----------|----------|
| Unknown `schema_version` (newer than engine) | Discard context, start fresh (safe fallback) |
| Missing fields in older version | Migration fills defaults; if migration fails, discard and start fresh |

### Service Layer Error Propagation

The `TutorService.lesson_chat()` method wraps engine calls in a try/except:
- Engine exceptions are caught, logged with full traceback, and a generic fallback response is returned to the user rather than a 500 error.
- The fallback response uses the `fallback` intent template to maintain UX consistency.

## Testing Strategy

### Unit Tests (pytest)

Following the existing three-layer test pattern:

**Repository layer** — No changes needed (existing `TutorRepository` tests cover `create_interaction`).

**Service layer** — Test `TutorService.lesson_chat()` with mocked repositories:
- Happy path: mastery data found, context valid, response generated
- No mastery data: defaults to STANDARD complexity
- Malformed context_json: engine starts fresh (no crash)
- Lesson not found: 404

**Router layer** — Test `POST /v1/tutor/lesson-chat` with mocked service:
- Valid request with `context_json`: 200 with response including updated `context_json`
- Valid request without `context_json` (backward compat): 200 with fresh context
- Invalid `message` (empty): 422
- Missing `subtopic_id`: 422

**Algorithm unit tests** (under `tests/features/tutor/algorithms/`):
- `test_context_manager.py` — Context construction, eviction, topic shift detection
- `test_anaphora_resolver.py` — Pronoun resolution, confidence scoring, edge cases
- `test_intent_classifier.py` — Scoring, discourse weighting, tie-breaking, disambiguation
- `test_socratic_module.py` — Activation rules, evaluation, attempt counting
- `test_cross_lesson_registry.py` — Building from metadata, concept matching
- `test_response_generator.py` — Template selection, composition, variant cycling
- `test_template_loader.py` — File loading, validation, fallback behavior

### Property-Based Tests (hypothesis)

Property-based testing is applicable to this feature because the engine is a pure-function pipeline with clear input/output behavior, large input spaces (messages, contexts, mastery scores), and well-defined universal invariants.

**Library:** `hypothesis` (already in project dependencies)
**Configuration:** Minimum 100 iterations per property (`@settings(max_examples=100)`)
**Tag format:** `# Feature: smart-chat-engine, Property {N}: {title}`

Each property from the Correctness Properties section maps to a single `@given(...)` test:

| Property | Test File | Key Generators |
|----------|-----------|----------------|
| P1: Context exchange window | `test_context_manager_props.py` | `st.lists(st.builds(Exchange, ...))` |
| P2: Anaphora resolution | `test_anaphora_props.py` | Messages with pronouns + random TopicThreads |
| P3: Topic shift detection | `test_context_manager_props.py` | Disjoint term sets |
| P4: Quiz answer classification | `test_intent_classifier_props.py` | `st.text(max_size=30)` + quiz_pending state |
| P5: Discourse disambiguation | `test_intent_classifier_props.py` | Multi-match messages + varying DiscourseState |
| P6: Thread-continuing wins ties | `test_intent_classifier_props.py` | Equal-score scenarios |
| P7: Low-confidence disambiguation | `test_intent_classifier_props.py` | Low-scoring messages |
| P8: Socratic activation | `test_socratic_module_props.py` | Conceptual questions + FAMILIAR+ mastery |
| P9: Socratic evaluation | `test_socratic_module_props.py` | Responses with varying key term overlap |
| P10: Socratic inactive for BEGINNER | `test_socratic_module_props.py` | Conceptual questions + BEGINNER mastery |
| P11: Registry completeness | `test_cross_lesson_registry_props.py` | Random lesson content_json dicts |
| P12: Cross-ref constraints | `test_response_generator_props.py` | Responses with cross-references |
| P13: Cross-ref placement | `test_response_generator_props.py` | Composed responses |
| P14: Complexity mapping | `test_response_generator_props.py` | `st.floats(0.0, 1.0)` |
| P15: Override lifetime | `test_response_generator_props.py` | Override trigger + N subsequent calls |
| P16: Variant non-repetition | `test_response_generator_props.py` | Same-intent sequences |
| P17: Context round-trip | `test_context_manager_props.py` | `st.builds(ConversationContext, ...)` |
| P18: Malformed context recovery | `test_context_manager_props.py` | `st.dictionaries(...)` (random invalid dicts) |
| P19: Core content presence | `test_response_generator_props.py` | All (intent, complexity) combos |

### Integration Tests

- End-to-end flow through `POST /v1/tutor/lesson-chat` with real DB session (in-memory SQLite), real lesson content, real mastery records
- Multi-turn conversation simulation: 5+ exchanges verifying context persistence and evolution
- Cross-lesson reference with seeded lessons containing overlapping key_takeaways
- Schema migration: context with `schema_version: 0` migrated to current version
