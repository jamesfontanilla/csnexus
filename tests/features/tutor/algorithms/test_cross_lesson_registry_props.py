"""Property-based tests for the Cross-Lesson Registry.

Uses Hypothesis to validate universal correctness properties of the
CrossLessonRegistry build and lookup logic.
"""

from __future__ import annotations

from hypothesis import given, settings, assume
from hypothesis.strategies import (
    composite,
    integers,
    lists,
    text,
)

from app.features.tutor.algorithms.cross_lesson_registry import (
    CrossLessonRegistry,
    _normalize_phrase,
)
from app.features.tutor.algorithms.chat_models import ConceptEntry


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Alphabet for generating human-readable concept phrases
_PHRASE_ALPHA = "abcdefghijklmnopqrstuvwxyz "


@composite
def phrase_1_to_5_words(draw):
    """Generate a phrase that normalizes to 1-5 words (non-empty)."""
    # Generate 1-5 words, each 2-10 chars
    word_count = draw(integers(min_value=1, max_value=5))
    words = [
        draw(text(min_size=2, max_size=10, alphabet="abcdefghijklmnopqrstuvwxyz"))
        for _ in range(word_count)
    ]
    return " ".join(words)


@composite
def section_dict(draw):
    """Generate a section dict with a title that is 1-5 words."""
    title = draw(phrase_1_to_5_words())
    return {"title": title}


@composite
def lesson_content_json(draw):
    """Generate a lesson content_json dict with key_takeaways and sections."""
    subtopic_id = draw(integers(min_value=1, max_value=10000))
    subtopic_title = draw(
        text(min_size=3, max_size=40, alphabet=_PHRASE_ALPHA)
    )

    # Generate 1-5 key_takeaways, each 1-5 words
    key_takeaways = draw(
        lists(phrase_1_to_5_words(), min_size=1, max_size=5)
    )

    # Generate 1-4 sections with titles
    sections = draw(lists(section_dict(), min_size=1, max_size=4))

    return {
        "subtopic_id": subtopic_id,
        "subtopic_title": subtopic_title,
        "key_takeaways": key_takeaways,
        "sections": sections,
    }


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 11: Cross-lesson registry completeness
# ---------------------------------------------------------------------------


class TestCrossLessonRegistryCompleteness:
    """For any lesson content_json containing key_takeaways and sections with
    titles, building the CrossLessonRegistry SHALL produce entries for every
    key_takeaway phrase (normalized to 1–5 words) and every section heading,
    each mapped to the correct subtopic_id.

    **Validates: Requirements 4.1**
    """

    @settings(max_examples=30)
    @given(lesson=lesson_content_json())
    def test_all_key_takeaways_registered(self, lesson: dict) -> None:
        """Every key_takeaway from a lesson is findable in the registry
        with the correct subtopic_id."""
        registry = CrossLessonRegistry.build_from_lessons([lesson])

        subtopic_id = lesson["subtopic_id"]
        key_takeaways = lesson["key_takeaways"]

        for takeaway in key_takeaways:
            normalized = _normalize_phrase(takeaway)
            # Our strategy guarantees 1-5 words, but verify after normalization
            assume(1 <= len(normalized.split()) <= 5)
            assume(len(normalized) > 0)

            entries = registry.lookup(normalized)
            assert len(entries) >= 1, (
                f"key_takeaway '{takeaway}' (normalized: '{normalized}') "
                f"not found in registry.\n"
                f"Registry terms: {registry.all_terms}\n"
            )

            # At least one entry should have the correct subtopic_id
            matching = [e for e in entries if e.subtopic_id == subtopic_id]
            assert len(matching) >= 1, (
                f"key_takeaway '{normalized}' found in registry but not "
                f"mapped to subtopic_id={subtopic_id}.\n"
                f"Found entries: {entries}\n"
            )

            # Source should be key_takeaway
            assert any(e.source == "key_takeaway" for e in matching), (
                f"key_takeaway '{normalized}' entry has wrong source.\n"
                f"Found: {[e.source for e in matching]}\n"
            )

    @settings(max_examples=30)
    @given(lesson=lesson_content_json())
    def test_all_section_headings_registered(self, lesson: dict) -> None:
        """Every section heading from a lesson is findable in the registry
        with the correct subtopic_id."""
        registry = CrossLessonRegistry.build_from_lessons([lesson])

        subtopic_id = lesson["subtopic_id"]
        sections = lesson["sections"]

        for section in sections:
            title = section["title"]
            normalized = _normalize_phrase(title)
            # Our strategy guarantees 1-5 words, but verify after normalization
            assume(1 <= len(normalized.split()) <= 5)
            assume(len(normalized) > 0)

            entries = registry.lookup(normalized)
            assert len(entries) >= 1, (
                f"section heading '{title}' (normalized: '{normalized}') "
                f"not found in registry.\n"
                f"Registry terms: {registry.all_terms}\n"
            )

            # At least one entry should have the correct subtopic_id
            matching = [e for e in entries if e.subtopic_id == subtopic_id]
            assert len(matching) >= 1, (
                f"section heading '{normalized}' found in registry but not "
                f"mapped to subtopic_id={subtopic_id}.\n"
                f"Found entries: {entries}\n"
            )

            # Source should be section_heading
            assert any(e.source == "section_heading" for e in matching), (
                f"section heading '{normalized}' entry has wrong source.\n"
                f"Found: {[e.source for e in matching]}\n"
            )

    @settings(max_examples=30)
    @given(lessons=lists(lesson_content_json(), min_size=2, max_size=5))
    def test_registry_completeness_across_multiple_lessons(
        self, lessons: list[dict]
    ) -> None:
        """Building from multiple lessons registers all concepts from each,
        and every registered lesson can be looked up by its terms."""
        registry = CrossLessonRegistry.build_from_lessons(lessons)

        for lesson in lessons:
            subtopic_id = lesson["subtopic_id"]
            key_takeaways = lesson["key_takeaways"]
            sections = lesson["sections"]

            # Every key_takeaway should be registered
            for takeaway in key_takeaways:
                normalized = _normalize_phrase(takeaway)
                if not normalized or not (1 <= len(normalized.split()) <= 5):
                    continue
                entries = registry.lookup(normalized)
                matching = [e for e in entries if e.subtopic_id == subtopic_id]
                assert len(matching) >= 1, (
                    f"key_takeaway '{normalized}' from subtopic {subtopic_id} "
                    f"missing in multi-lesson registry.\n"
                )

            # Every section heading should be registered
            for section in sections:
                title = section["title"]
                normalized = _normalize_phrase(title)
                if not normalized or not (1 <= len(normalized.split()) <= 5):
                    continue
                entries = registry.lookup(normalized)
                matching = [e for e in entries if e.subtopic_id == subtopic_id]
                assert len(matching) >= 1, (
                    f"section heading '{normalized}' from subtopic {subtopic_id} "
                    f"missing in multi-lesson registry.\n"
                )

            # find_by_subtopic should return entries for this subtopic
            subtopic_entries = registry.find_by_subtopic(subtopic_id)
            assert len(subtopic_entries) >= 1, (
                f"find_by_subtopic({subtopic_id}) returned no entries "
                f"but lesson has key_takeaways and sections.\n"
            )
