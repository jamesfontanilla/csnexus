"""Property-based tests for the Response Generator.

Uses Hypothesis to validate universal correctness properties of the
response generation pipeline, focusing on cross-reference output constraints,
composition ordering, and core content presence guarantees.
"""

from __future__ import annotations

from hypothesis import given, settings, assume, HealthCheck
from hypothesis.strategies import (
    composite,
    floats,
    integers,
    lists,
    sampled_from,
    text,
)

from app.features.tutor.algorithms.cross_lesson_registry import (
    CrossLessonRegistry,
    _normalize_phrase,
)
from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ComplexityOverride,
    ConceptEntry,
    ConversationContext,
)
from app.features.tutor.algorithms.response_generator import (
    activate_override,
    compose_response,
    compute_complexity_level,
    decrement_override,
    format_cross_references,
    resolve_effective_complexity,
    select_template_variant,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_PHRASE_ALPHA = "abcdefghijklmnopqrstuvwxyz "


@composite
def phrase_1_to_5_words(draw):
    """Generate a phrase that normalizes to 1-5 words (non-empty)."""
    word_count = draw(integers(min_value=1, max_value=5))
    words = [
        draw(text(min_size=2, max_size=10, alphabet="abcdefghijklmnopqrstuvwxyz"))
        for _ in range(word_count)
    ]
    return " ".join(words)


@composite
def concept_entry(draw):
    """Generate a valid ConceptEntry with realistic field lengths."""
    term = draw(phrase_1_to_5_words())
    subtopic_id = draw(integers(min_value=1, max_value=10000))
    subtopic_title = draw(text(min_size=3, max_size=60, alphabet=_PHRASE_ALPHA))
    source = draw(text(min_size=5, max_size=15, alphabet="abcdefghijklmnopqrstuvwxyz_"))
    return ConceptEntry(
        term=term,
        subtopic_id=subtopic_id,
        subtopic_title=subtopic_title.strip(),
        source=source,
    )


@composite
def lesson_content_json(draw):
    """Generate a lesson content_json dict with key_takeaways and sections."""
    subtopic_id = draw(integers(min_value=1, max_value=10000))
    subtopic_title = draw(text(min_size=3, max_size=40, alphabet=_PHRASE_ALPHA))

    key_takeaways = draw(lists(phrase_1_to_5_words(), min_size=1, max_size=5))
    sections = draw(
        lists(
            phrase_1_to_5_words().map(lambda t: {"title": t}),
            min_size=1,
            max_size=4,
        )
    )

    return {
        "subtopic_id": subtopic_id,
        "subtopic_title": subtopic_title,
        "key_takeaways": key_takeaways,
        "sections": sections,
    }


@composite
def multi_lesson_with_shared_terms(draw):
    """Generate multiple lessons where at least some share terms.

    This ensures find_related() has opportunities to return cross-references.
    """
    # Create a shared set of terms
    shared_terms = draw(lists(phrase_1_to_5_words(), min_size=2, max_size=4))

    lessons = []
    num_lessons = draw(integers(min_value=3, max_value=6))
    for i in range(num_lessons):
        subtopic_id = i + 1  # Unique IDs
        subtopic_title = draw(text(min_size=3, max_size=40, alphabet=_PHRASE_ALPHA))

        # Each lesson gets some shared terms + some unique ones
        unique_terms = draw(lists(phrase_1_to_5_words(), min_size=0, max_size=3))
        # Include at least one shared term in each lesson
        lesson_takeaways = shared_terms[:2] + unique_terms

        sections = draw(
            lists(
                phrase_1_to_5_words().map(lambda t: {"title": t}),
                min_size=1,
                max_size=3,
            )
        )

        lessons.append({
            "subtopic_id": subtopic_id,
            "subtopic_title": subtopic_title,
            "key_takeaways": lesson_takeaways,
            "sections": sections,
        })

    return lessons


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 12: Cross-reference output constraints
# ---------------------------------------------------------------------------


class TestCrossReferenceOutputConstraints:
    """For any response that includes cross-references, there SHALL be at most
    2 cross-references, and each cross-reference text SHALL be at most 150
    characters and constitute a single sentence.

    **Validates: Requirements 4.3, 4.6**
    """

    @settings(max_examples=30)
    @given(lessons=multi_lesson_with_shared_terms())
    def test_find_related_returns_at_most_2(self, lessons: list[dict]) -> None:
        """find_related() never returns more than 2 cross-references
        regardless of how many matching terms exist."""
        registry = CrossLessonRegistry.build_from_lessons(lessons)

        # Try finding related from each lesson's perspective
        for lesson in lessons:
            subtopic_id = lesson["subtopic_id"]
            terms = lesson.get("key_takeaways", [])
            if not terms:
                continue

            results = registry.find_related(terms, subtopic_id)
            assert len(results) <= 2, (
                f"find_related() returned {len(results)} entries "
                f"(max allowed: 2) for subtopic_id={subtopic_id} "
                f"with terms={terms}"
            )

    @settings(max_examples=30)
    @given(entries=lists(concept_entry(), min_size=1, max_size=10))
    def test_format_cross_references_at_most_2_sentences(
        self, entries: list[ConceptEntry]
    ) -> None:
        """format_cross_references() produces at most 2 cross-reference
        sentences regardless of how many entries are provided."""
        result = format_cross_references(entries)

        if not result:
            return  # Empty result is valid

        # Each cross-reference ends with a period. Count sentences.
        # The format is "sentence1. sentence2." joined by space.
        sentences = [s.strip() for s in result.split(". ") if s.strip()]
        # Account for last sentence having its own period
        if sentences and not sentences[-1].endswith("."):
            pass  # Split removed trailing period
        # Re-count by splitting on period-space or trailing period
        sentences = [s.strip().rstrip(".") for s in result.rstrip(".").split(". ") if s.strip()]
        assert len(sentences) <= 2, (
            f"format_cross_references() produced {len(sentences)} sentences "
            f"(max allowed: 2). Output: '{result}'"
        )

    @settings(max_examples=30)
    @given(entries=lists(concept_entry(), min_size=1, max_size=10))
    def test_each_cross_reference_at_most_150_chars(
        self, entries: list[ConceptEntry]
    ) -> None:
        """Each individual cross-reference text is at most 150 characters."""
        # Test the constraint on individual entries (up to 2)
        for entry in entries[:2]:
            ref_text = f"This connects to {entry.term} in {entry.subtopic_title}."
            # The implementation truncates to 150 chars
            if len(ref_text) > 150:
                ref_text = ref_text[:149] + "."

            assert len(ref_text) <= 150, (
                f"Cross-reference text exceeds 150 chars ({len(ref_text)}): "
                f"'{ref_text}'"
            )

        # Also verify the implementation's format_cross_references does it
        result = format_cross_references(entries)
        if not result:
            return

        # Split into individual references. Format is "Sentence1. Sentence2."
        # Split by ". " and re-add the period
        individual_refs = []
        remaining = result
        while ". " in remaining:
            idx = remaining.index(". ")
            individual_refs.append(remaining[: idx + 1])
            remaining = remaining[idx + 2:]
        if remaining:
            individual_refs.append(remaining)

        for ref in individual_refs:
            assert len(ref) <= 150, (
                f"Individual cross-reference exceeds 150 chars "
                f"({len(ref)}): '{ref}'"
            )

    @settings(max_examples=30)
    @given(entries=lists(concept_entry(), min_size=1, max_size=10))
    def test_each_cross_reference_is_single_sentence(
        self, entries: list[ConceptEntry]
    ) -> None:
        """Each cross-reference constitutes a single sentence (exactly one
        terminal period)."""
        result = format_cross_references(entries)
        if not result:
            return

        # Split into individual references
        individual_refs = []
        remaining = result
        while ". " in remaining:
            idx = remaining.index(". ")
            individual_refs.append(remaining[: idx + 1])
            remaining = remaining[idx + 2:]
        if remaining:
            individual_refs.append(remaining)

        assert len(individual_refs) <= 2, (
            f"More than 2 cross-references in output: {individual_refs}"
        )

        for ref in individual_refs:
            # A single sentence should have exactly one period at the end
            ref_stripped = ref.strip()
            assert ref_stripped.endswith("."), (
                f"Cross-reference does not end with period: '{ref_stripped}'"
            )
            # Count periods — should be exactly 1 (the terminal one)
            # But note: terms like "e.g." could have periods. The real constraint
            # is that the reference is a single sentence, which means one terminal
            # punctuation mark and no sentence-splitting internal periods.
            inner_text = ref_stripped[:-1]  # Remove trailing period
            # The generated format is "This connects to {term} in {title}."
            # where term and title come from our generators (alpha + space only)
            # so internal periods would only appear from unusual input.
            # For the implementation, verify no ". " pattern inside (sentence boundary)
            assert ". " not in inner_text, (
                f"Cross-reference contains multiple sentences: '{ref_stripped}'"
            )

    @settings(max_examples=30, suppress_health_check=[HealthCheck.too_slow])
    @given(lessons=multi_lesson_with_shared_terms())
    def test_end_to_end_cross_reference_constraints(
        self, lessons: list[dict]
    ) -> None:
        """End-to-end: build registry, find related, format output —
        all constraints hold together."""
        registry = CrossLessonRegistry.build_from_lessons(lessons)

        for lesson in lessons:
            subtopic_id = lesson["subtopic_id"]
            terms = lesson.get("key_takeaways", [])
            if not terms:
                continue

            related = registry.find_related(terms, subtopic_id)

            # Constraint: at most 2
            assert len(related) <= 2

            # Format them
            output = format_cross_references(related)
            if not output:
                continue

            # Split into individual references
            individual_refs = []
            remaining = output
            while ". " in remaining:
                idx = remaining.index(". ")
                individual_refs.append(remaining[: idx + 1])
                remaining = remaining[idx + 2:]
            if remaining:
                individual_refs.append(remaining)

            # At most 2 references
            assert len(individual_refs) <= 2, (
                f"Output has {len(individual_refs)} refs: {individual_refs}"
            )

            # Each <= 150 chars and single sentence
            for ref in individual_refs:
                assert len(ref) <= 150, (
                    f"Ref exceeds 150 chars ({len(ref)}): '{ref}'"
                )
                assert ref.strip().endswith("."), (
                    f"Ref doesn't end with period: '{ref}'"
                )
                inner = ref.strip()[:-1]
                assert ". " not in inner, (
                    f"Ref contains multiple sentences: '{ref}'"
                )



# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 19: Response always contains core content
# ---------------------------------------------------------------------------


class TestResponseAlwaysContainsCoreContent:
    """For any valid combination of intent, ComplexityLevel, and
    ConversationContext, the composed response SHALL always include the
    core content template part (non-empty string).

    **Validates: Requirements 6.2**
    """

    FALLBACK_TEXT = "Here's what you need to know about this topic."

    @settings(max_examples=30)
    @given(
        opener=text(min_size=0, max_size=50, alphabet=_PHRASE_ALPHA),
        core_content=text(min_size=1, max_size=200, alphabet=_PHRASE_ALPHA),
        cross_reference=text(min_size=0, max_size=100, alphabet=_PHRASE_ALPHA),
        closing=text(min_size=0, max_size=50, alphabet=_PHRASE_ALPHA),
    )
    def test_compose_response_always_contains_core_content(
        self,
        opener: str,
        core_content: str,
        cross_reference: str,
        closing: str,
    ) -> None:
        """compose_response() output always contains the core_content text
        when core_content is non-empty."""
        assume(core_content.strip() != "")

        result = compose_response(opener, core_content, cross_reference, closing)

        assert core_content in result, (
            f"core_content '{core_content}' not found in composed response: '{result}'"
        )

    @settings(max_examples=30)
    @given(
        opener=text(min_size=0, max_size=50, alphabet=_PHRASE_ALPHA),
        cross_reference=text(min_size=0, max_size=100, alphabet=_PHRASE_ALPHA),
        closing=text(min_size=0, max_size=50, alphabet=_PHRASE_ALPHA),
    )
    def test_compose_response_uses_fallback_when_core_content_empty(
        self,
        opener: str,
        cross_reference: str,
        closing: str,
    ) -> None:
        """When core_content is empty, compose_response() uses the fallback
        text instead, ensuring the response is never missing core content."""
        result = compose_response(opener, "", cross_reference, closing)

        assert self.FALLBACK_TEXT in result, (
            f"Fallback text not found in response when core_content is empty. "
            f"Response: '{result}'"
        )

    @settings(max_examples=30)
    @given(
        opener=text(min_size=0, max_size=50, alphabet=_PHRASE_ALPHA),
        core_content=text(min_size=0, max_size=200, alphabet=_PHRASE_ALPHA),
        cross_reference=text(min_size=0, max_size=100, alphabet=_PHRASE_ALPHA),
        closing=text(min_size=0, max_size=50, alphabet=_PHRASE_ALPHA),
    )
    def test_compose_response_never_returns_empty_string(
        self,
        opener: str,
        core_content: str,
        cross_reference: str,
        closing: str,
    ) -> None:
        """compose_response() NEVER returns an empty string, regardless of
        what combination of inputs is provided."""
        result = compose_response(opener, core_content, cross_reference, closing)

        assert result != "", (
            f"compose_response() returned empty string with inputs: "
            f"opener='{opener}', core_content='{core_content}', "
            f"cross_reference='{cross_reference}', closing='{closing}'"
        )
        assert result.strip() != "", (
            f"compose_response() returned whitespace-only string: '{result}'"
        )

    @settings(max_examples=30)
    @given(
        core_content=text(min_size=1, max_size=200, alphabet=_PHRASE_ALPHA),
    )
    def test_core_content_present_when_other_parts_empty(
        self,
        core_content: str,
    ) -> None:
        """Even when opener, cross_reference, and closing are all empty,
        core_content is still present in the output."""
        assume(core_content.strip() != "")

        result = compose_response("", core_content, "", "")

        assert core_content in result, (
            f"core_content '{core_content}' not in output when all other "
            f"parts are empty. Result: '{result}'"
        )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 15: Complexity override lifetime
# ---------------------------------------------------------------------------


class TestComplexityOverrideLifetime:
    """For any complexity override triggered by a complexity adjustment phrase,
    the override SHALL be active for exactly the current response plus the next
    3 responses in the same TopicThread (remaining_responses counts down from 3
    to 0), and the response immediately after expiry SHALL use the
    mastery-computed ComplexityLevel.

    **Validates: Requirements 5.5, 5.6**
    """

    @settings(max_examples=30)
    @given(
        mastery_score=floats(min_value=0.0, max_value=1.0, allow_nan=False),
        direction=sampled_from(["simpler", "deeper"]),
    )
    def test_activate_override_sets_remaining_to_3(
        self, mastery_score: float, direction: str
    ) -> None:
        """When a complexity override is activated, remaining_responses
        starts at 3 (covering current + next 3 responses)."""
        ctx = ConversationContext()
        current_level = compute_complexity_level(mastery_score)

        activate_override(ctx, direction, current_level)

        assert ctx.complexity_override is not None
        assert ctx.complexity_override.remaining_responses == 3

    @settings(max_examples=30)
    @given(
        mastery_score=floats(min_value=0.0, max_value=1.0, allow_nan=False),
        direction=sampled_from(["simpler", "deeper"]),
    )
    def test_decrement_override_decreases_remaining_by_1(
        self, mastery_score: float, direction: str
    ) -> None:
        """decrement_override() decreases remaining_responses by 1 each call."""
        ctx = ConversationContext()
        current_level = compute_complexity_level(mastery_score)
        activate_override(ctx, direction, current_level)

        # After activation, remaining = 3
        # Decrement once → 2
        decrement_override(ctx)
        assert ctx.complexity_override is not None
        assert ctx.complexity_override.remaining_responses == 2

        # Decrement again → 1
        decrement_override(ctx)
        assert ctx.complexity_override is not None
        assert ctx.complexity_override.remaining_responses == 1

        # Decrement again → 0
        decrement_override(ctx)
        assert ctx.complexity_override is not None
        assert ctx.complexity_override.remaining_responses == 0

    @settings(max_examples=30)
    @given(
        mastery_score=floats(min_value=0.0, max_value=1.0, allow_nan=False),
        direction=sampled_from(["simpler", "deeper"]),
    )
    def test_override_expires_after_4_decrements(
        self, mastery_score: float, direction: str
    ) -> None:
        """After 4 total decrements (current response + 3 subsequent),
        the override is cleared (set to None)."""
        ctx = ConversationContext()
        current_level = compute_complexity_level(mastery_score)
        activate_override(ctx, direction, current_level)

        # Decrement 4 times: 3 → 2 → 1 → 0 → cleared
        for _ in range(4):
            decrement_override(ctx)

        assert ctx.complexity_override is None

    @settings(max_examples=30)
    @given(
        mastery_score=floats(min_value=0.0, max_value=1.0, allow_nan=False),
        direction=sampled_from(["simpler", "deeper"]),
    )
    def test_override_active_for_exactly_4_responses(
        self, mastery_score: float, direction: str
    ) -> None:
        """The override persists for the current response + next 3 responses.
        resolve_effective_complexity returns the override level for exactly
        4 calls with decrement_override between them, then reverts."""
        ctx = ConversationContext()
        current_level = compute_complexity_level(mastery_score)
        override_level = activate_override(ctx, direction, current_level)

        # The override should be active for 4 responses total
        for i in range(4):
            effective = resolve_effective_complexity(mastery_score, ctx)
            assert effective == override_level, (
                f"Response {i + 1}: expected override level {override_level}, "
                f"got {effective}"
            )
            decrement_override(ctx)

        # After the 4th decrement, override is cleared
        assert ctx.complexity_override is None

        # Next call should revert to mastery-computed level
        effective_after = resolve_effective_complexity(mastery_score, ctx)
        assert effective_after == current_level, (
            f"After override expiry: expected mastery-computed level "
            f"{current_level}, got {effective_after}"
        )

    @settings(max_examples=30)
    @given(
        mastery_score=floats(min_value=0.0, max_value=1.0, allow_nan=False),
        direction=sampled_from(["simpler", "deeper"]),
    )
    def test_decrement_on_none_override_is_noop(
        self, mastery_score: float, direction: str
    ) -> None:
        """Calling decrement_override when no override is set does nothing."""
        ctx = ConversationContext()

        # No override set
        assert ctx.complexity_override is None
        decrement_override(ctx)
        assert ctx.complexity_override is None

    @settings(max_examples=30)
    @given(
        mastery_score=floats(min_value=0.0, max_value=1.0, allow_nan=False),
        direction=sampled_from(["simpler", "deeper"]),
    )
    def test_override_cleared_when_remaining_drops_below_zero(
        self, mastery_score: float, direction: str
    ) -> None:
        """When remaining_responses drops below 0 via decrement, the override
        is cleared (set to None)."""
        ctx = ConversationContext()
        current_level = compute_complexity_level(mastery_score)
        activate_override(ctx, direction, current_level)

        # Manually set remaining_responses to 0 to simulate edge
        ctx.complexity_override.remaining_responses = 0

        # One more decrement should clear it (remaining goes to -1 → cleared)
        decrement_override(ctx)
        assert ctx.complexity_override is None


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 14: Complexity level mapping
# ---------------------------------------------------------------------------


class TestComplexityLevelMapping:
    """For any mastery_score in [0.0, 1.0], the computed ComplexityLevel SHALL
    be SIMPLIFIED when score < 0.3, STANDARD when 0.3 <= score <= 0.7, and
    DETAILED when score > 0.7. When mastery_score is None, the level SHALL
    be STANDARD.

    **Validates: Requirements 5.1, 5.7**
    """

    @settings(max_examples=30)
    @given(score=floats(min_value=0.0, max_value=0.2999999))
    def test_score_below_threshold_returns_simplified(self, score: float) -> None:
        """Scores strictly below 0.3 map to SIMPLIFIED."""
        assume(score < 0.3)
        result = compute_complexity_level(score)
        assert result == ComplexityLevel.SIMPLIFIED, (
            f"Expected SIMPLIFIED for score {score}, got {result}"
        )

    @settings(max_examples=30)
    @given(score=floats(min_value=0.3, max_value=0.7))
    def test_score_in_standard_range_returns_standard(self, score: float) -> None:
        """Scores in [0.3, 0.7] map to STANDARD."""
        result = compute_complexity_level(score)
        assert result == ComplexityLevel.STANDARD, (
            f"Expected STANDARD for score {score}, got {result}"
        )

    @settings(max_examples=30)
    @given(score=floats(min_value=0.7000001, max_value=1.0))
    def test_score_above_threshold_returns_detailed(self, score: float) -> None:
        """Scores strictly above 0.7 map to DETAILED."""
        assume(score > 0.7)
        result = compute_complexity_level(score)
        assert result == ComplexityLevel.DETAILED, (
            f"Expected DETAILED for score {score}, got {result}"
        )

    @settings(max_examples=30)
    @given(score=floats(min_value=0.0, max_value=1.0))
    def test_none_always_returns_standard(self, score: float) -> None:
        """When mastery_score is None, the result is always STANDARD
        regardless of what other scores might suggest."""
        result = compute_complexity_level(None)
        assert result == ComplexityLevel.STANDARD, (
            f"Expected STANDARD for None mastery_score, got {result}"
        )

    @settings(max_examples=30)
    @given(score=floats(min_value=0.0, max_value=1.0))
    def test_all_scores_map_to_valid_complexity_level(self, score: float) -> None:
        """Every score in [0.0, 1.0] maps to exactly one of the three
        ComplexityLevel values — no gaps or undefined regions."""
        result = compute_complexity_level(score)
        assert result in (
            ComplexityLevel.SIMPLIFIED,
            ComplexityLevel.STANDARD,
            ComplexityLevel.DETAILED,
        ), f"Score {score} mapped to unexpected value: {result}"

    @settings(max_examples=30)
    @given(score=floats(min_value=0.0, max_value=1.0))
    def test_partition_is_exhaustive_and_exclusive(self, score: float) -> None:
        """Each score belongs to exactly one partition — the mapping function
        is a total function over [0.0, 1.0] with no overlapping regions."""
        result = compute_complexity_level(score)

        if score < 0.3:
            assert result == ComplexityLevel.SIMPLIFIED
        elif score > 0.7:
            assert result == ComplexityLevel.DETAILED
        else:
            assert result == ComplexityLevel.STANDARD


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 13: Cross-reference placement ordering
# ---------------------------------------------------------------------------


@composite
def tagged_response_parts(draw):
    """Generate four distinct response parts with unique prefixes.

    Each part gets a unique tag prefix to prevent substring collision
    when checking positions in the composed output.
    """
    suffix = draw(text(min_size=2, max_size=40, alphabet="abcdefghijklmnopqrstuvwxyz "))
    opener = f"OPENER {suffix.strip() or 'hello'}"
    core = f"CORE {draw(text(min_size=2, max_size=40, alphabet='abcdefghijklmnopqrstuvwxyz ')).strip() or 'main'}"
    xref = f"XREF {draw(text(min_size=2, max_size=40, alphabet='abcdefghijklmnopqrstuvwxyz ')).strip() or 'link'}"
    closing = f"CLOSING {draw(text(min_size=2, max_size=40, alphabet='abcdefghijklmnopqrstuvwxyz ')).strip() or 'bye'}"
    return opener, core, xref, closing


class TestCrossReferencePlacementOrdering:
    """For any composed response containing cross-reference text, the
    cross-reference section SHALL appear after the core content section
    and before the closing prompt section in the final output string.

    compose_response(opener, core_content, cross_reference, closing) maintains
    the order: opener -> core -> cross_reference -> closing.

    **Validates: Requirements 4.8**
    """

    @settings(max_examples=30)
    @given(parts=tagged_response_parts())
    def test_cross_reference_after_core_before_closing(
        self,
        parts: tuple[str, str, str, str],
    ) -> None:
        """Cross-reference appears after core content and before closing."""
        opener, core_content, cross_reference, closing = parts

        result = compose_response(opener, core_content, cross_reference, closing)

        # All parts should be present in the output
        assert core_content in result
        assert cross_reference in result
        assert closing in result

        # Verify ordering: core before cross_reference before closing
        core_pos = result.index(core_content)
        xref_pos = result.index(cross_reference)
        closing_pos = result.index(closing)

        assert core_pos < xref_pos, (
            f"Core content (pos={core_pos}) should appear before "
            f"cross-reference (pos={xref_pos}) in: '{result}'"
        )
        assert xref_pos < closing_pos, (
            f"Cross-reference (pos={xref_pos}) should appear before "
            f"closing (pos={closing_pos}) in: '{result}'"
        )

    @settings(max_examples=30)
    @given(parts=tagged_response_parts())
    def test_full_ordering_opener_core_xref_closing(
        self,
        parts: tuple[str, str, str, str],
    ) -> None:
        """Full ordering: opener -> core -> cross_reference -> closing."""
        opener, core_content, cross_reference, closing = parts

        result = compose_response(opener, core_content, cross_reference, closing)

        opener_pos = result.index(opener)
        core_pos = result.index(core_content)
        xref_pos = result.index(cross_reference)
        closing_pos = result.index(closing)

        assert opener_pos < core_pos < xref_pos < closing_pos, (
            f"Order violated. Positions: opener={opener_pos}, "
            f"core={core_pos}, xref={xref_pos}, closing={closing_pos}. "
            f"Result: '{result}'"
        )

    @settings(max_examples=30)
    @given(
        core_suffix=text(min_size=2, max_size=40, alphabet="abcdefghijklmnopqrstuvwxyz "),
        closing_suffix=text(min_size=2, max_size=40, alphabet="abcdefghijklmnopqrstuvwxyz "),
        opener_suffix=text(min_size=0, max_size=40, alphabet="abcdefghijklmnopqrstuvwxyz "),
    )
    def test_empty_cross_reference_omitted_order_preserved(
        self,
        core_suffix: str,
        closing_suffix: str,
        opener_suffix: str,
    ) -> None:
        """When cross_reference is empty, it's omitted but order of other
        parts is preserved."""
        core_content = f"CORE {core_suffix.strip() or 'main'}"
        closing = f"CLOSING {closing_suffix.strip() or 'bye'}"
        opener = f"OPENER {opener_suffix.strip()}" if opener_suffix.strip() else ""

        result = compose_response(opener, core_content, "", closing)

        # Core content and closing must be present
        assert core_content in result
        assert closing in result

        core_pos = result.index(core_content)
        closing_pos = result.index(closing)

        # Core before closing even without cross_reference
        assert core_pos < closing_pos, (
            f"Core (pos={core_pos}) should appear before closing "
            f"(pos={closing_pos}) when cross_reference is empty. "
            f"Result: '{result}'"
        )

        # If opener is non-empty, it should be before core
        if opener:
            assert opener in result
            opener_pos = result.index(opener)
            assert opener_pos < core_pos, (
                f"Opener (pos={opener_pos}) should appear before "
                f"core (pos={core_pos}). Result: '{result}'"
            )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 16: Template variant non-repetition
# ---------------------------------------------------------------------------


_INTENTS = [
    "explain_section",
    "give_example",
    "summarize",
    "quiz_me",
    "relate_to_exam",
    "memory_aid",
    "conceptual_question",
    "direct_answer_request",
    "cross_reference_request",
]

_PART_KEYS = ["opener", "closing"]


class TestTemplateVariantNonRepetition:
    """For any sequence of consecutive responses with the same intent within a
    TopicThread, no two adjacent responses SHALL use the same template variant
    index for the opener or closing parts.

    **Validates: Requirements 6.4**
    """

    @settings(max_examples=30)
    @given(
        intent=sampled_from(_INTENTS),
        part_key=sampled_from(_PART_KEYS),
        available_count=integers(min_value=2, max_value=10),
        num_calls=integers(min_value=2, max_value=20),
    )
    def test_adjacent_calls_never_repeat_variant(
        self,
        intent: str,
        part_key: str,
        available_count: int,
        num_calls: int,
    ) -> None:
        """select_template_variant() never returns the same index for two
        consecutive calls with the same intent and part_key when
        available_count >= 2."""
        ctx = ConversationContext()

        previous_idx: int | None = None
        for _ in range(num_calls):
            idx = select_template_variant(intent, part_key, available_count, ctx)
            assert 0 <= idx < available_count, (
                f"Variant index {idx} out of range [0, {available_count})"
            )
            if previous_idx is not None:
                assert idx != previous_idx, (
                    f"Adjacent calls returned same variant index {idx} "
                    f"for intent='{intent}', part_key='{part_key}', "
                    f"available_count={available_count}"
                )
            previous_idx = idx

    @settings(max_examples=30)
    @given(
        intent=sampled_from(_INTENTS),
        part_key=sampled_from(_PART_KEYS),
        available_count=integers(min_value=2, max_value=6),
    )
    def test_exhaustion_resets_and_still_avoids_last(
        self,
        intent: str,
        part_key: str,
        available_count: int,
    ) -> None:
        """When all variants are exhausted, tracking resets and the next pick
        still avoids the last-used index (no adjacent repetition)."""
        ctx = ConversationContext()

        # Call exactly available_count times to exhaust all variants
        previous_idx: int | None = None
        for _ in range(available_count):
            idx = select_template_variant(intent, part_key, available_count, ctx)
            if previous_idx is not None:
                assert idx != previous_idx, (
                    f"Adjacent repetition during exhaustion phase: "
                    f"index={idx}, available_count={available_count}"
                )
            previous_idx = idx

        # Next call should trigger reset — verify no adjacent repetition
        post_reset_idx = select_template_variant(intent, part_key, available_count, ctx)
        assert post_reset_idx != previous_idx, (
            f"After exhaustion reset, adjacent repetition occurred: "
            f"last={previous_idx}, post_reset={post_reset_idx}, "
            f"available_count={available_count}"
        )

    @settings(max_examples=30)
    @given(
        intent=sampled_from(_INTENTS),
        part_key=sampled_from(_PART_KEYS),
        available_count=integers(min_value=2, max_value=6),
        num_cycles=integers(min_value=2, max_value=4),
    )
    def test_multiple_cycles_maintain_non_repetition(
        self,
        intent: str,
        part_key: str,
        available_count: int,
        num_cycles: int,
    ) -> None:
        """Across multiple full exhaustion cycles, adjacent non-repetition
        is always maintained."""
        ctx = ConversationContext()
        total_calls = available_count * num_cycles + 1

        previous_idx: int | None = None
        for _ in range(total_calls):
            idx = select_template_variant(intent, part_key, available_count, ctx)
            assert 0 <= idx < available_count
            if previous_idx is not None:
                assert idx != previous_idx, (
                    f"Adjacent repetition in multi-cycle test: "
                    f"index={idx}, available_count={available_count}, "
                    f"num_cycles={num_cycles}"
                )
            previous_idx = idx

    @settings(max_examples=30)
    @given(
        intent=sampled_from(_INTENTS),
        part_key=sampled_from(_PART_KEYS),
        available_count=integers(min_value=2, max_value=8),
    )
    def test_usage_tracking_records_selections(
        self,
        intent: str,
        part_key: str,
        available_count: int,
    ) -> None:
        """select_template_variant() updates ctx.template_usage with the
        chosen indices, keyed by '{intent}:{part_key}'."""
        ctx = ConversationContext()
        usage_key = f"{intent}:{part_key}"

        # Make a few calls
        indices = []
        for _ in range(min(available_count, 4)):
            idx = select_template_variant(intent, part_key, available_count, ctx)
            indices.append(idx)

        # Verify the context tracks usage
        assert usage_key in ctx.template_usage, (
            f"Usage key '{usage_key}' not found in template_usage after calls"
        )
        tracked = ctx.template_usage[usage_key]
        assert len(tracked) > 0, "template_usage should have recorded indices"
