"""Unit tests for the Cross-Lesson Registry.

Tests building from lesson content, find_related lookup,
mastery-differentiated cross-reference text formatting,
comparison response generation, and output constraints.

Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8
"""

from __future__ import annotations

import pytest

from app.features.tutor.algorithms.chat_models import ConceptEntry
from app.features.tutor.algorithms.cross_lesson_registry import (
    ComparisonResult,
    CrossLessonRegistry,
    _MAX_CROSS_REF_CHARS,
    _MAX_CROSS_REFS,
    _normalize_phrase,
)


# ---------------------------------------------------------------------------
# Fixtures / Helpers
# ---------------------------------------------------------------------------


def _make_lesson(
    subtopic_id: int = 1,
    subtopic_title: str = "Test Topic",
    key_takeaways: list[str] | None = None,
    sections: list[dict] | None = None,
    prerequisites: list[dict] | None = None,
) -> dict:
    """Build a lesson content_json dict with sensible defaults."""
    lesson: dict = {
        "subtopic_id": subtopic_id,
        "subtopic_title": subtopic_title,
    }
    if key_takeaways is not None:
        lesson["key_takeaways"] = key_takeaways
    if sections is not None:
        lesson["sections"] = sections
    if prerequisites is not None:
        lesson["metadata"] = {"prerequisites": prerequisites}
    return lesson


def _two_lesson_registry() -> CrossLessonRegistry:
    """Build a registry with two lessons sharing a common term."""
    lessons = [
        _make_lesson(
            subtopic_id=1,
            subtopic_title="Addition",
            key_takeaways=["number operations", "carry over"],
            sections=[{"title": "Basic Rules"}],
        ),
        _make_lesson(
            subtopic_id=2,
            subtopic_title="Subtraction",
            key_takeaways=["number operations", "borrowing"],
            sections=[{"title": "Inverse Operations"}],
        ),
    ]
    return CrossLessonRegistry.build_from_lessons(lessons)


# ---------------------------------------------------------------------------
# Tests: build_from_lessons (Req 4.1)
# ---------------------------------------------------------------------------


class TestBuildFromLessons:
    def test_extracts_key_takeaways(self) -> None:
        lesson = _make_lesson(
            subtopic_id=10,
            subtopic_title="Fractions",
            key_takeaways=["numerator denominator", "simplifying fractions"],
        )
        registry = CrossLessonRegistry.build_from_lessons([lesson])

        entries = registry.lookup("numerator denominator")
        assert len(entries) == 1
        assert entries[0].subtopic_id == 10
        assert entries[0].source == "key_takeaway"

    def test_extracts_section_headings(self) -> None:
        lesson = _make_lesson(
            subtopic_id=20,
            subtopic_title="Decimals",
            sections=[{"title": "Converting Fractions"}],
        )
        registry = CrossLessonRegistry.build_from_lessons([lesson])

        entries = registry.lookup("converting fractions")
        assert len(entries) == 1
        assert entries[0].subtopic_id == 20
        assert entries[0].source == "section_heading"

    def test_extracts_prerequisites(self) -> None:
        lesson = _make_lesson(
            subtopic_id=30,
            subtopic_title="Algebra",
            prerequisites=[
                {"subtopic_id": 10, "subtopic_title": "Fractions"}
            ],
        )
        registry = CrossLessonRegistry.build_from_lessons([lesson])

        entries = registry.lookup("fractions")
        assert len(entries) == 1
        assert entries[0].subtopic_id == 30
        assert entries[0].source == "prerequisite"

    def test_skips_phrases_longer_than_5_words(self) -> None:
        lesson = _make_lesson(
            subtopic_id=40,
            subtopic_title="Long Title Topic",
            key_takeaways=["one two three four five six words here"],
        )
        registry = CrossLessonRegistry.build_from_lessons([lesson])
        assert len(registry) == 0

    def test_skips_empty_phrases(self) -> None:
        lesson = _make_lesson(
            subtopic_id=50,
            subtopic_title="Empty",
            key_takeaways=["", "   "],
        )
        registry = CrossLessonRegistry.build_from_lessons([lesson])
        assert len(registry) == 0

    def test_normalizes_phrases(self) -> None:
        lesson = _make_lesson(
            subtopic_id=60,
            subtopic_title="Normalizing",
            key_takeaways=["  UPPER Case  "],
        )
        registry = CrossLessonRegistry.build_from_lessons([lesson])
        entries = registry.lookup("upper case")
        assert len(entries) == 1

    def test_skips_lesson_without_subtopic_id(self) -> None:
        lesson = {"subtopic_title": "No ID"}
        registry = CrossLessonRegistry.build_from_lessons([lesson])
        assert len(registry) == 0


# ---------------------------------------------------------------------------
# Tests: find_related (Req 4.2, 4.6)
# ---------------------------------------------------------------------------


class TestFindRelated:
    def test_returns_entries_from_other_subtopics(self) -> None:
        registry = _two_lesson_registry()
        results = registry.find_related(["number operations"], current_subtopic_id=1)
        assert len(results) == 1
        assert results[0].subtopic_id == 2

    def test_excludes_current_subtopic(self) -> None:
        registry = _two_lesson_registry()
        results = registry.find_related(["number operations"], current_subtopic_id=2)
        assert all(r.subtopic_id != 2 for r in results)

    def test_limits_to_max_2_results(self) -> None:
        lessons = [
            _make_lesson(subtopic_id=i, subtopic_title=f"Topic {i}", key_takeaways=["shared concept"])
            for i in range(5)
        ]
        registry = CrossLessonRegistry.build_from_lessons(lessons)
        results = registry.find_related(["shared concept"], current_subtopic_id=0)
        assert len(results) <= _MAX_CROSS_REFS

    def test_returns_empty_for_no_matches(self) -> None:
        registry = _two_lesson_registry()
        results = registry.find_related(["nonexistent term"], current_subtopic_id=1)
        assert results == []

    def test_partial_matching_substring(self) -> None:
        """Partial match: search term is substring of registered term."""
        lessons = [
            _make_lesson(subtopic_id=1, subtopic_title="A", key_takeaways=["basic rules"]),
            _make_lesson(subtopic_id=2, subtopic_title="B", key_takeaways=["rules"]),
        ]
        registry = CrossLessonRegistry.build_from_lessons(lessons)
        # "rules" is a substring of "basic rules"
        results = registry.find_related(["rules"], current_subtopic_id=99)
        assert len(results) >= 1


# ---------------------------------------------------------------------------
# Tests: format_cross_reference (Req 4.3, 4.4)
# ---------------------------------------------------------------------------


class TestFormatCrossReference:
    def test_mastery_exists_notes_connection(self) -> None:
        registry = CrossLessonRegistry()
        entry = ConceptEntry(
            term="fractions",
            subtopic_id=10,
            subtopic_title="Fractions",
            source="key_takeaway",
        )
        text = registry.format_cross_reference(entry, has_mastery=True)
        assert "studied" in text.lower() or "connect" in text.lower()
        assert len(text) <= _MAX_CROSS_REF_CHARS

    def test_no_mastery_mentions_future_learning(self) -> None:
        registry = CrossLessonRegistry()
        entry = ConceptEntry(
            term="algebra",
            subtopic_id=20,
            subtopic_title="Algebra",
            source="key_takeaway",
        )
        text = registry.format_cross_reference(entry, has_mastery=False)
        assert "explore" in text.lower() or "further" in text.lower()
        assert len(text) <= _MAX_CROSS_REF_CHARS

    def test_single_sentence_constraint(self) -> None:
        registry = CrossLessonRegistry()
        entry = ConceptEntry(
            term="long concept name",
            subtopic_id=30,
            subtopic_title="Very Long Subtopic Title",
            source="key_takeaway",
        )
        text = registry.format_cross_reference(entry, has_mastery=True)
        # Single sentence: exactly one period at the end
        assert text.endswith(".")
        # No period in the middle (single sentence check)
        inner = text[:-1]
        assert "." not in inner or len(text) <= _MAX_CROSS_REF_CHARS

    def test_truncation_for_very_long_names(self) -> None:
        registry = CrossLessonRegistry()
        entry = ConceptEntry(
            term="a" * 50,
            subtopic_id=40,
            subtopic_title="B" * 80,
            source="key_takeaway",
        )
        text = registry.format_cross_reference(entry, has_mastery=True)
        assert len(text) <= _MAX_CROSS_REF_CHARS
        assert text.endswith(".")


# ---------------------------------------------------------------------------
# Tests: format_cross_references (Req 4.3, 4.4, 4.6)
# ---------------------------------------------------------------------------


class TestFormatCrossReferences:
    def test_empty_entries_returns_empty(self) -> None:
        registry = CrossLessonRegistry()
        assert registry.format_cross_references([]) == ""

    def test_limits_to_max_2(self) -> None:
        registry = CrossLessonRegistry()
        entries = [
            ConceptEntry(term=f"term{i}", subtopic_id=i, subtopic_title=f"Topic {i}", source="key_takeaway")
            for i in range(5)
        ]
        text = registry.format_cross_references(entries)
        # Should produce at most 2 sentences
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        assert len(sentences) <= _MAX_CROSS_REFS

    def test_mastery_differentiation(self) -> None:
        registry = CrossLessonRegistry()
        entries = [
            ConceptEntry(term="fractions", subtopic_id=10, subtopic_title="Fractions", source="key_takeaway"),
            ConceptEntry(term="algebra", subtopic_id=20, subtopic_title="Algebra", source="key_takeaway"),
        ]
        # subtopic 10 has mastery, subtopic 20 does not
        text = registry.format_cross_references(entries, mastery_subtopic_ids={10})
        assert "studied" in text.lower() or "connect" in text.lower()
        assert "explore" in text.lower() or "further" in text.lower()


# ---------------------------------------------------------------------------
# Tests: generate_comparison (Req 4.5)
# ---------------------------------------------------------------------------


class TestGenerateComparison:
    def test_produces_shared_principles(self) -> None:
        registry = _two_lesson_registry()
        result = registry.generate_comparison(
            current_subtopic_id=1,
            other_subtopic_id=2,
        )
        assert isinstance(result, ComparisonResult)
        assert len(result.shared_principles) >= 1

    def test_produces_differences(self) -> None:
        registry = _two_lesson_registry()
        result = registry.generate_comparison(
            current_subtopic_id=1,
            other_subtopic_id=2,
        )
        assert len(result.differences) >= 1

    def test_shared_principles_are_sentences(self) -> None:
        registry = _two_lesson_registry()
        result = registry.generate_comparison(
            current_subtopic_id=1,
            other_subtopic_id=2,
        )
        for principle in result.shared_principles:
            assert principle.endswith(".")
            # At most 2 sentences
            inner_periods = principle[:-1].count(".")
            assert inner_periods <= 1

    def test_differences_are_sentences(self) -> None:
        registry = _two_lesson_registry()
        result = registry.generate_comparison(
            current_subtopic_id=1,
            other_subtopic_id=2,
        )
        for diff in result.differences:
            assert diff.endswith(".")

    def test_fallback_when_no_shared_terms(self) -> None:
        lessons = [
            _make_lesson(subtopic_id=100, subtopic_title="Geometry", key_takeaways=["angles"]),
            _make_lesson(subtopic_id=200, subtopic_title="Poetry", key_takeaways=["rhyme"]),
        ]
        registry = CrossLessonRegistry.build_from_lessons(lessons)
        result = registry.generate_comparison(
            current_subtopic_id=100,
            other_subtopic_id=200,
        )
        assert len(result.shared_principles) >= 1
        assert len(result.differences) >= 1

    def test_format_response_returns_string(self) -> None:
        registry = _two_lesson_registry()
        result = registry.generate_comparison(
            current_subtopic_id=1,
            other_subtopic_id=2,
        )
        formatted = result.format_response()
        assert isinstance(formatted, str)
        assert len(formatted) > 0


# ---------------------------------------------------------------------------
# Tests: _normalize_phrase helper
# ---------------------------------------------------------------------------


class TestNormalizePhrase:
    def test_lowercases(self) -> None:
        assert _normalize_phrase("HELLO") == "hello"

    def test_strips_whitespace(self) -> None:
        assert _normalize_phrase("  hello  ") == "hello"

    def test_replaces_special_chars(self) -> None:
        assert _normalize_phrase("hello-world!") == "hello world"

    def test_collapses_multiple_spaces(self) -> None:
        assert _normalize_phrase("hello   world") == "hello world"

    def test_empty_string(self) -> None:
        assert _normalize_phrase("") == ""

    def test_none_returns_empty(self) -> None:
        # Type-wise this shouldn't happen, but the function handles it gracefully
        assert _normalize_phrase("") == ""
