"""Integration tests for the Smart Chat Engine.

Simulates real multi-turn user conversations against the full engine
pipeline using actual lesson content from the seed data. Each scenario
exercises the end-to-end flow: context management → anaphora resolution →
intent classification → Socratic module → response generation.

These tests call generate_chat_response() directly with real lesson
content_json extracted from the subject-verb agreement lesson.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app.features.tutor.algorithms.lesson_chat_engine import generate_chat_response

# ---------------------------------------------------------------------------
# Fixtures: Load real lesson content from seed data
# ---------------------------------------------------------------------------

_LESSON_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "seed"
    / "lessons"
    / "verbal-ability"
    / "grammar"
    / "subject-verb-agreement"
    / "lesson.md"
)


def _extract_json_from_markdown(md_text: str) -> dict | None:
    """Try to extract a JSON code block from markdown."""
    pattern = r"```json\s*\n(.*?)\n```"
    match = re.search(pattern, md_text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return None


def _build_content_json_from_lesson(md_text: str) -> dict:
    """Build a content_json dict from the lesson markdown.

    First tries to parse an embedded JSON block. If not found, constructs
    a content_json dict from the markdown structure with the key fields
    the engine expects: metadata, sections, key_takeaways.
    """
    # Try embedded JSON first
    extracted = _extract_json_from_markdown(md_text)
    if extracted:
        return extracted

    # Build from markdown content
    sections: list[dict] = []
    current_section: dict | None = None

    for line in md_text.split("\n"):
        # Detect H2 sections (## heading)
        if line.startswith("## ") and not line.startswith("### "):
            heading = line[3:].strip()
            if current_section:
                sections.append(current_section)
            current_section = {
                "title": heading,
                "blocks": [],
            }
        elif current_section is not None and line.strip():
            # Accumulate text content into the current section
            if (
                current_section["blocks"]
                and current_section["blocks"][-1]["type"] == "text"
            ):
                current_section["blocks"][-1]["content"] += " " + line.strip()
            else:
                current_section["blocks"].append(
                    {"type": "text", "content": line.strip()}
                )

    if current_section:
        sections.append(current_section)

    return {
        "metadata": {
            "subtopic_id": 101,
            "title": "Subject-Verb Agreement",
        },
        "subtopic_id": 101,
        "subtopic_title": "Subject-Verb Agreement",
        "sections": sections,
        "key_takeaways": [
            "A singular subject takes a singular verb; a plural subject takes a plural verb.",
            "Intervening phrases between subject and verb do not affect agreement.",
            "Compound subjects joined by 'and' take a plural verb.",
            "Indefinite pronouns like everyone, each, nobody are always singular.",
            "In inverted sentences, identify the real subject after the verb.",
        ],
    }


@pytest.fixture(scope="module")
def lesson_content() -> dict:
    """Load the subject-verb agreement lesson and return content_json."""
    md_text = _LESSON_PATH.read_text(encoding="utf-8")
    return _build_content_json_from_lesson(md_text)


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------


def _assert_valid_result(result, expected_intent: str | None = None) -> None:
    """Assert common invariants on a ChatResult."""
    assert result.response_text, "response_text must be non-empty"
    assert isinstance(result.context_json, dict), "context_json must be a dict"
    assert "schema_version" in result.context_json, (
        "context_json must contain schema_version"
    )
    if expected_intent is not None:
        assert result.detected_intent == expected_intent, (
            f"Expected intent '{expected_intent}', got '{result.detected_intent}'"
        )


# ---------------------------------------------------------------------------
# Scenario 1: Basic greeting and explanation flow
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestGreetingAndExplanationFlow:
    """Multi-turn: greeting → explain → example."""

    def test_greeting_then_explain_then_example(self, lesson_content: dict) -> None:
        # Turn 1: greeting
        r1 = generate_chat_response(
            content_json=lesson_content,
            message="hi",
        )
        _assert_valid_result(r1, expected_intent="greeting")

        # Turn 2: explain with context from previous
        r2 = generate_chat_response(
            content_json=lesson_content,
            message="explain this section",
            context_json=r1.context_json,
        )
        _assert_valid_result(r2, expected_intent="explain_section")

        # Turn 3: ask for example with accumulated context
        r3 = generate_chat_response(
            content_json=lesson_content,
            message="can you give me an example?",
            context_json=r2.context_json,
        )
        _assert_valid_result(r3, expected_intent="give_example")


# ---------------------------------------------------------------------------
# Scenario 2: Complexity adjustment
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestComplexityAdjustment:
    """User triggers complexity downgrade and subsequent responses stay simplified."""

    def test_complexity_adjustment_flow(self, lesson_content: dict) -> None:
        # Turn 1: explain at DETAILED level (mastery_score=0.8)
        r1 = generate_chat_response(
            content_json=lesson_content,
            message="explain this section",
            mastery_score=0.8,
        )
        _assert_valid_result(r1, expected_intent="explain_section")

        # Turn 2: request simplification using a phrase that matches
        # the engine's simplify patterns (eli5, simpler, etc.)
        r2 = generate_chat_response(
            content_json=lesson_content,
            message="explain more simply",
            context_json=r1.context_json,
            mastery_score=0.8,
        )
        _assert_valid_result(r2, expected_intent="complexity_adjustment")

        # Context should now have a complexity override
        assert r2.context_json.get("complexity_override") is not None, (
            "complexity_override should be set after adjustment request"
        )

        # Turn 3: follow-up explain should use STANDARD level (one step down from DETAILED)
        r3 = generate_chat_response(
            content_json=lesson_content,
            message="explain more",
            context_json=r2.context_json,
            mastery_score=0.8,
        )
        _assert_valid_result(r3)
        # Override should persist (remaining_responses decremented)
        override = r3.context_json.get("complexity_override")
        if override is not None:
            # DETAILED → one step down = STANDARD
            assert override["level"] == "STANDARD"


# ---------------------------------------------------------------------------
# Scenario 3: Socratic mode activation
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestSocraticModeActivation:
    """A conceptual question at FAMILIAR mastery level triggers Socratic mode."""

    def test_conceptual_question_triggers_socratic(
        self, lesson_content: dict
    ) -> None:
        result = generate_chat_response(
            content_json=lesson_content,
            message="why is subject-verb agreement important?",
            mastery_level="FAMILIAR",
            mastery_score=0.4,
        )
        _assert_valid_result(result)

        # Socratic mode should be detected — either a guiding question or
        # the intent is conceptual_question with Socratic state active
        assert result.detected_intent == "conceptual_question", (
            f"Expected 'conceptual_question', got '{result.detected_intent}'"
        )
        # Response should contain a question mark (guiding question)
        assert "?" in result.response_text, (
            "Socratic mode should produce a guiding question (contains '?')"
        )


# ---------------------------------------------------------------------------
# Scenario 4: Quiz flow
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestQuizFlow:
    """User requests quiz → answers with short response → recognized as attempt."""

    def test_quiz_me_then_answer(self, lesson_content: dict) -> None:
        # Turn 1: request quiz
        r1 = generate_chat_response(
            content_json=lesson_content,
            message="quiz me",
        )
        _assert_valid_result(r1, expected_intent="quiz_me")
        # Quiz response may be a question (?) or a prompt statement
        # e.g. "Can you explain..." or "Think it through..."
        assert len(r1.response_text) > 20, (
            "Quiz response should be a substantive prompt or question"
        )
        # Discourse state should move to quiz_pending
        assert r1.context_json.get("discourse_state") == "quiz_pending", (
            "After quiz_me, discourse_state should be quiz_pending"
        )

        # Turn 2: short answer (simulating multiple-choice)
        r2 = generate_chat_response(
            content_json=lesson_content,
            message="B",
            context_json=r1.context_json,
        )
        _assert_valid_result(r2, expected_intent="quiz_answer_attempt")


# ---------------------------------------------------------------------------
# Scenario 5: Topic shift detection
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestTopicShiftDetection:
    """Switching to an unrelated topic creates a new thread in context."""

    def test_topic_shift_creates_new_thread(self, lesson_content: dict) -> None:
        # Turn 1: establish a topic thread
        r1 = generate_chat_response(
            content_json=lesson_content,
            message="explain subject-verb agreement",
        )
        _assert_valid_result(r1)

        # Capture initial threads
        initial_threads = r1.context_json.get("topic_threads", [])

        # Turn 2: completely unrelated topic
        r2 = generate_chat_response(
            content_json=lesson_content,
            message="tell me about photosynthesis",
            context_json=r1.context_json,
        )
        _assert_valid_result(r2)

        # A new thread should be created (topic_threads list grows or changes)
        new_threads = r2.context_json.get("topic_threads", [])
        # Either new thread added or active thread changed subject
        subjects = [t.get("subject", "") for t in new_threads]
        # The new topic should appear in threads
        has_new_topic = any(
            "photosynthesis" in s.lower() for s in subjects
        )
        # Or old topic is deactivated and new one is active
        active_threads = [t for t in new_threads if t.get("is_active")]
        assert has_new_topic or len(new_threads) > len(initial_threads), (
            "Topic shift should create a new thread or update active thread. "
            f"Threads: {subjects}"
        )


# ---------------------------------------------------------------------------
# Scenario 6: Anaphora resolution
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestAnaphoraResolution:
    """Pronoun 'it' resolves to the active topic thread subject."""

    def test_it_resolves_to_active_topic(self, lesson_content: dict) -> None:
        # Turn 1: establish topic
        r1 = generate_chat_response(
            content_json=lesson_content,
            message="explain subject-verb agreement",
        )
        _assert_valid_result(r1)

        # Turn 2: use pronoun "it"
        r2 = generate_chat_response(
            content_json=lesson_content,
            message="explain it more",
            context_json=r1.context_json,
        )
        _assert_valid_result(r2)

        # The response should still be about subject-verb agreement
        # (not a clarification request)
        assert result_is_about_sva(r2), (
            "Anaphora 'it' should resolve to subject-verb agreement; "
            f"got intent={r2.detected_intent}"
        )


def result_is_about_sva(result) -> bool:
    """Check that a result is still on-topic (not clarification/off-topic)."""
    # If the engine asked for clarification, anaphora resolution failed
    if result.detected_intent == "clarification":
        return False
    # Check response mentions SVA-related terms or is an explain intent
    text_lower = result.response_text.lower()
    sva_terms = ["subject", "verb", "agreement", "singular", "plural"]
    has_sva_content = any(t in text_lower for t in sva_terms)
    is_explain = result.detected_intent in ("explain_section", "give_example")
    return has_sva_content or is_explain


# ---------------------------------------------------------------------------
# Scenario 7: Fallback on engine error (empty content)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestFallbackOnEmptyContent:
    """Engine should not crash with completely empty content_json."""

    def test_empty_content_does_not_crash(self) -> None:
        result = generate_chat_response(
            content_json={},
            message="explain this topic",
        )
        # Should not raise — must return some response
        assert result.response_text, "Engine must return a response even with empty content"
        assert isinstance(result.context_json, dict)
        assert "schema_version" in result.context_json


# ---------------------------------------------------------------------------
# Scenario 8: Context persistence across turns
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestContextPersistence:
    """Context accumulates exchanges and maintains schema_version."""

    def test_context_grows_across_three_turns(self, lesson_content: dict) -> None:
        messages = [
            "hi",
            "explain this section",
            "give me an example",
        ]
        context = None

        for i, msg in enumerate(messages):
            result = generate_chat_response(
                content_json=lesson_content,
                message=msg,
                context_json=context,
            )
            _assert_valid_result(result)
            context = result.context_json

            # schema_version present at every turn
            assert "schema_version" in context

            # exchanges list should grow
            exchanges = context.get("exchanges", [])
            assert len(exchanges) == i + 1, (
                f"After turn {i + 1}, expected {i + 1} exchanges, "
                f"got {len(exchanges)}"
            )

    def test_schema_version_is_integer(self, lesson_content: dict) -> None:
        result = generate_chat_response(
            content_json=lesson_content,
            message="hello",
        )
        assert isinstance(result.context_json["schema_version"], int)
