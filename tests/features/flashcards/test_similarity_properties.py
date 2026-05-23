"""Property-based tests for the similarity engine (typed answer comparison).

**Validates: Requirements 8.4**

Uses Hypothesis to verify universal properties of compare_typed_answer across
all possible string inputs and strictness modes.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis.strategies import sampled_from, text

from app.features.flashcards.algorithms.similarity import (
    Strictness,
    compare_typed_answer,
)


# ---------------------------------------------------------------------------
# Property 13: Typed answer comparison
# ---------------------------------------------------------------------------


class TestSimilarityScoreRange:
    """similarity_score is always in [0.0, 1.0]."""

    @settings(max_examples=100)
    @given(
        user_answer=text(),
        correct_answer=text(),
        strictness=sampled_from(Strictness),
    )
    def test_similarity_score_bounded(
        self, user_answer: str, correct_answer: str, strictness: Strictness
    ) -> None:
        result = compare_typed_answer(user_answer, correct_answer, strictness)
        assert 0.0 <= result.similarity_score <= 1.0


class TestExactMatchSimilarity:
    """When user_answer equals correct_answer (case-insensitive, stripped), similarity_score = 1.0."""

    @settings(max_examples=100)
    @given(
        answer=text(),
        strictness=sampled_from(Strictness),
    )
    def test_identical_answers_have_perfect_similarity(
        self, answer: str, strictness: Strictness
    ) -> None:
        result = compare_typed_answer(answer, answer, strictness)
        assert result.similarity_score == 1.0


class TestExactMatchIsCorrect:
    """When user_answer equals correct_answer (case-insensitive, stripped), is_correct = True for ALL strictness modes."""

    @settings(max_examples=100)
    @given(
        answer=text(),
        strictness=sampled_from(Strictness),
    )
    def test_identical_answers_always_correct(
        self, answer: str, strictness: Strictness
    ) -> None:
        result = compare_typed_answer(answer, answer, strictness)
        assert result.is_correct is True


class TestExactModeSemantics:
    """EXACT mode: is_correct iff stripped lowercase strings are equal."""

    @settings(max_examples=100)
    @given(
        user_answer=text(),
        correct_answer=text(),
    )
    def test_exact_mode_matches_stripped_lowercase_equality(
        self, user_answer: str, correct_answer: str
    ) -> None:
        result = compare_typed_answer(user_answer, correct_answer, Strictness.EXACT)
        expected = user_answer.strip().lower() == correct_answer.strip().lower()
        assert result.is_correct is expected


class TestContainsModeSemantics:
    """CONTAINS mode: is_correct iff correct_answer (lowercase, stripped) is a substring of user_answer (lowercase, stripped)."""

    @settings(max_examples=100)
    @given(
        user_answer=text(),
        correct_answer=text(),
    )
    def test_contains_mode_checks_substring(
        self, user_answer: str, correct_answer: str
    ) -> None:
        result = compare_typed_answer(user_answer, correct_answer, Strictness.CONTAINS)
        expected = correct_answer.strip().lower() in user_answer.strip().lower()
        assert result.is_correct is expected


class TestFuzzyModeSemantics:
    """FUZZY mode: is_correct iff similarity_score >= 0.8."""

    @settings(max_examples=100)
    @given(
        user_answer=text(),
        correct_answer=text(),
    )
    def test_fuzzy_mode_uses_threshold(
        self, user_answer: str, correct_answer: str
    ) -> None:
        result = compare_typed_answer(user_answer, correct_answer, Strictness.FUZZY)
        expected = result.similarity_score >= 0.8
        assert result.is_correct is expected


class TestCorrectAnswerPreserved:
    """correct_answer in result always equals the original correct_answer passed in (unchanged)."""

    @settings(max_examples=100)
    @given(
        user_answer=text(),
        correct_answer=text(),
        strictness=sampled_from(Strictness),
    )
    def test_correct_answer_passthrough(
        self, user_answer: str, correct_answer: str, strictness: Strictness
    ) -> None:
        result = compare_typed_answer(user_answer, correct_answer, strictness)
        assert result.correct_answer == correct_answer


class TestCaseInsensitivity:
    """Comparison is case-insensitive (same result regardless of case).

    Note: Only tests ASCII strings because Unicode case folding can change
    string length (e.g., ß → SS), which affects Levenshtein distance.
    """

    @settings(max_examples=100)
    @given(
        user_answer=text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789 "),
        correct_answer=text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789 "),
        strictness=sampled_from(Strictness),
    )
    def test_case_does_not_affect_result(
        self, user_answer: str, correct_answer: str, strictness: Strictness
    ) -> None:
        result_original = compare_typed_answer(user_answer, correct_answer, strictness)
        result_upper = compare_typed_answer(
            user_answer.upper(), correct_answer.upper(), strictness
        )
        assert result_original.is_correct == result_upper.is_correct
        assert result_original.similarity_score == result_upper.similarity_score
