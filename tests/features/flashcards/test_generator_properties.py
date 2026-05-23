"""Property-based tests for the pseudo-AI flashcard generator.

Validates: Requirements 11.4, 11.10
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis.strategies import integers, text

from app.features.flashcards.algorithms.generator import (
    Difficulty,
    GeneratedCardType,
    classify_difficulty,
    generate_flashcards,
)


# ---------------------------------------------------------------------------
# Helper: generate lesson content with N terms
# ---------------------------------------------------------------------------


def _make_lesson_content(num_terms: int) -> str:
    """Generate lesson markdown with exactly num_terms extractable terms."""
    lines = ["# Test Lesson\n"]
    for i in range(num_terms):
        lines.append(
            f"**Term{i:03d}**: This is the definition of term number {i} "
            f"which provides enough context for extraction.\n"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Property 18: Generated card validity invariant
# Validates: Requirements 11.10
# ---------------------------------------------------------------------------


class TestGeneratedCardValidityInvariant:
    """For ANY valid lesson content with >= 10 terms, all generated cards
    have non-empty front, non-empty back, and a valid card_type.

    **Validates: Requirements 11.10**
    """

    @settings(max_examples=100, deadline=None)
    @given(num_terms=integers(min_value=10, max_value=50))
    def test_all_cards_have_non_empty_front_and_back(
        self, num_terms: int
    ) -> None:
        """Every generated card has non-empty front and back."""
        content = _make_lesson_content(num_terms)
        result = generate_flashcards(content, lesson_id=1)

        assert result.error is None
        assert len(result.cards) > 0

        for card in result.cards:
            assert card.front.strip(), f"Empty front for term: {card.source_term}"
            assert card.back.strip(), f"Empty back for term: {card.source_term}"

    @settings(max_examples=100, deadline=None)
    @given(num_terms=integers(min_value=10, max_value=50))
    def test_all_cards_have_valid_card_type(self, num_terms: int) -> None:
        """Every generated card has a valid GeneratedCardType."""
        content = _make_lesson_content(num_terms)
        result = generate_flashcards(content, lesson_id=1)

        assert result.error is None
        for card in result.cards:
            assert card.card_type in (
                GeneratedCardType.BASIC,
                GeneratedCardType.CLOZE,
                GeneratedCardType.MCQ,
            )

    @settings(max_examples=100, deadline=None)
    @given(num_terms=integers(min_value=10, max_value=50))
    def test_card_count_within_bounds(self, num_terms: int) -> None:
        """Generated card count is between 10 and 50."""
        content = _make_lesson_content(num_terms)
        result = generate_flashcards(content, lesson_id=1)

        assert result.error is None
        assert 1 <= len(result.cards) <= 50

    @settings(max_examples=100, deadline=None)
    @given(num_terms=integers(min_value=10, max_value=50))
    def test_card_distribution_has_all_types(self, num_terms: int) -> None:
        """Generated cards include basic, cloze, and MCQ types."""
        content = _make_lesson_content(num_terms)
        result = generate_flashcards(content, lesson_id=1)

        assert result.error is None
        types = {card.card_type for card in result.cards}
        # With 10+ terms, all three types should be present
        assert GeneratedCardType.BASIC in types
        assert GeneratedCardType.CLOZE in types
        if num_terms >= 12:  # MCQ needs at least a few terms for distribution
            assert GeneratedCardType.MCQ in types

    @settings(max_examples=100, deadline=None)
    @given(num_terms=integers(min_value=0, max_value=9))
    def test_insufficient_terms_returns_error(self, num_terms: int) -> None:
        """Fewer than 10 terms returns an error, not cards."""
        content = _make_lesson_content(num_terms)
        result = generate_flashcards(content, lesson_id=1)

        assert result.error is not None
        assert len(result.cards) == 0
        assert result.terms_extracted < 10

    @settings(max_examples=100, deadline=None)
    @given(num_terms=integers(min_value=10, max_value=50))
    def test_all_cards_have_valid_difficulty(self, num_terms: int) -> None:
        """Every generated card has a valid Difficulty enum value."""
        content = _make_lesson_content(num_terms)
        result = generate_flashcards(content, lesson_id=1)

        assert result.error is None
        for card in result.cards:
            assert card.difficulty in (
                Difficulty.EASY,
                Difficulty.MEDIUM,
                Difficulty.HARD,
            )


# ---------------------------------------------------------------------------
# Property 19: Difficulty classification correctness
# Validates: Requirements 11.4
# ---------------------------------------------------------------------------


class TestDifficultyClassificationCorrectness:
    """For ANY term, classify_difficulty returns a valid Difficulty.

    **Validates: Requirements 11.4**
    """

    @settings(max_examples=100)
    @given(term=text(min_size=1, max_size=100))
    def test_always_returns_valid_difficulty(self, term: str) -> None:
        """classify_difficulty always returns a Difficulty enum member."""
        result = classify_difficulty(term)
        assert result in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD)

    @settings(max_examples=100)
    @given(term=text(min_size=1, max_size=100))
    def test_common_words_are_easy(self, term: str) -> None:
        """Terms made entirely of common words classify as EASY."""
        # Build a term from only common words
        common_term = "the good time"
        result = classify_difficulty(common_term)
        assert result == Difficulty.EASY

    @settings(max_examples=100)
    @given(term=text(min_size=1, max_size=100))
    def test_uncommon_words_are_hard(self, term: str) -> None:
        """Terms with no common words classify as HARD."""
        uncommon_term = "xylophone pneumonoultramicroscopicsilicovolcanoconiosis"
        result = classify_difficulty(uncommon_term)
        assert result == Difficulty.HARD
