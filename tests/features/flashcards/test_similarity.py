"""Unit tests for the similarity engine (Levenshtein-based typed answer comparison)."""

from app.features.flashcards.algorithms.similarity import (
    AnswerComparison,
    Strictness,
    compare_typed_answer,
    _levenshtein_distance,
    _levenshtein_ratio,
)


# --- Levenshtein distance tests ---


class TestLevenshteinDistance:
    def test_identical_strings(self):
        assert _levenshtein_distance("hello", "hello") == 0

    def test_empty_strings(self):
        assert _levenshtein_distance("", "") == 0

    def test_one_empty(self):
        assert _levenshtein_distance("abc", "") == 3
        assert _levenshtein_distance("", "abc") == 3

    def test_single_substitution(self):
        assert _levenshtein_distance("cat", "bat") == 1

    def test_single_insertion(self):
        assert _levenshtein_distance("cat", "cats") == 1

    def test_single_deletion(self):
        assert _levenshtein_distance("cats", "cat") == 1

    def test_completely_different(self):
        assert _levenshtein_distance("abc", "xyz") == 3


# --- Levenshtein ratio tests ---


class TestLevenshteinRatio:
    def test_identical_strings(self):
        assert _levenshtein_ratio("hello", "hello") == 1.0

    def test_both_empty(self):
        assert _levenshtein_ratio("", "") == 1.0

    def test_completely_different(self):
        assert _levenshtein_ratio("abc", "xyz") == 0.0

    def test_one_edit_away(self):
        # "cat" vs "bat" → distance 1, max_len 3 → ratio = 1 - 1/3 ≈ 0.667
        ratio = _levenshtein_ratio("cat", "bat")
        assert abs(ratio - (2 / 3)) < 1e-9


# --- EXACT mode tests ---


class TestExactMode:
    def test_exact_match(self):
        result = compare_typed_answer("Photosynthesis", "Photosynthesis", Strictness.EXACT)
        assert result.is_correct is True
        assert result.similarity_score == 1.0

    def test_case_insensitive(self):
        result = compare_typed_answer("photosynthesis", "Photosynthesis", Strictness.EXACT)
        assert result.is_correct is True

    def test_strips_whitespace(self):
        result = compare_typed_answer("  hello  ", "hello", Strictness.EXACT)
        assert result.is_correct is True

    def test_mismatch(self):
        result = compare_typed_answer("wrong", "correct", Strictness.EXACT)
        assert result.is_correct is False

    def test_partial_match_not_accepted(self):
        result = compare_typed_answer("photo", "Photosynthesis", Strictness.EXACT)
        assert result.is_correct is False


# --- CONTAINS mode tests ---


class TestContainsMode:
    def test_exact_match(self):
        result = compare_typed_answer("Mitosis", "Mitosis", Strictness.CONTAINS)
        assert result.is_correct is True

    def test_correct_answer_within_user_answer(self):
        result = compare_typed_answer(
            "The answer is mitosis I think", "mitosis", Strictness.CONTAINS
        )
        assert result.is_correct is True

    def test_case_insensitive(self):
        result = compare_typed_answer("MITOSIS", "mitosis", Strictness.CONTAINS)
        assert result.is_correct is True

    def test_not_contained(self):
        result = compare_typed_answer("meiosis", "mitosis", Strictness.CONTAINS)
        assert result.is_correct is False

    def test_strips_whitespace(self):
        result = compare_typed_answer("  mitosis  ", "mitosis", Strictness.CONTAINS)
        assert result.is_correct is True


# --- FUZZY mode tests ---


class TestFuzzyMode:
    def test_exact_match(self):
        result = compare_typed_answer("algorithm", "algorithm", Strictness.FUZZY)
        assert result.is_correct is True
        assert result.similarity_score == 1.0

    def test_minor_typo_accepted(self):
        # "algoritm" vs "algorithm" → distance 1, max_len 9 → ratio ≈ 0.889 >= 0.8
        result = compare_typed_answer("algoritm", "algorithm", Strictness.FUZZY)
        assert result.is_correct is True
        assert result.similarity_score >= 0.8

    def test_major_difference_rejected(self):
        # "xyz" vs "algorithm" → very low ratio
        result = compare_typed_answer("xyz", "algorithm", Strictness.FUZZY)
        assert result.is_correct is False
        assert result.similarity_score < 0.8

    def test_threshold_boundary(self):
        # "abcde" vs "abcdf" → distance 1, max_len 5 → ratio = 0.8 (exactly at threshold)
        result = compare_typed_answer("abcde", "abcdf", Strictness.FUZZY)
        assert result.is_correct is True
        assert result.similarity_score >= 0.8


# --- General behavior tests ---


class TestGeneralBehavior:
    def test_returns_correct_answer_unchanged(self):
        result = compare_typed_answer("anything", "Original Answer", Strictness.EXACT)
        assert result.correct_answer == "Original Answer"

    def test_similarity_score_always_between_0_and_1(self):
        result = compare_typed_answer("abc", "xyz", Strictness.EXACT)
        assert 0.0 <= result.similarity_score <= 1.0

    def test_result_is_frozen_dataclass(self):
        result = compare_typed_answer("a", "b", Strictness.EXACT)
        assert isinstance(result, AnswerComparison)

    def test_default_strictness_is_contains(self):
        result = compare_typed_answer("The answer is hello world", "hello world")
        assert result.is_correct is True
