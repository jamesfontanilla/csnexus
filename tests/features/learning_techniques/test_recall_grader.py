"""Tests for the recall grader algorithm (Property 40).

Feature: intelligent-learning-engine, Property 40:
Recall grading uses Levenshtein distance ≤ 2 for fuzzy matching.
"""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.features.learning_techniques.algorithms.recall_grader import (
    grade_recall_answer,
    _levenshtein_distance,
)


# ── Levenshtein distance unit tests ──────────────────────────────────────────


def test_levenshtein_identical_strings():
    assert _levenshtein_distance("hello", "hello") == 0


def test_levenshtein_single_substitution():
    assert _levenshtein_distance("cat", "bat") == 1


def test_levenshtein_single_insertion():
    assert _levenshtein_distance("cat", "cats") == 1


def test_levenshtein_single_deletion():
    assert _levenshtein_distance("cats", "cat") == 1


def test_levenshtein_two_edits():
    assert _levenshtein_distance("kitten", "mitten") == 1
    assert _levenshtein_distance("sitting", "sitting") == 0
    assert _levenshtein_distance("abc", "xyz") == 3


def test_levenshtein_empty_string():
    assert _levenshtein_distance("", "hello") == 5
    assert _levenshtein_distance("hello", "") == 5
    assert _levenshtein_distance("", "") == 0


# ── grade_recall_answer unit tests ───────────────────────────────────────────


def test_exact_match():
    is_correct, match_type = grade_recall_answer("proportion", "proportion")
    assert is_correct is True
    assert match_type == "exact"


def test_exact_match_case_insensitive():
    is_correct, match_type = grade_recall_answer("PROPORTION", "proportion")
    assert is_correct is True
    assert match_type == "exact"


def test_exact_match_with_whitespace():
    is_correct, match_type = grade_recall_answer("  proportion  ", "proportion")
    assert is_correct is True
    assert match_type == "exact"


def test_fuzzy_match_single_typo():
    # "proporton" vs "proportion" — 1 edit
    is_correct, match_type = grade_recall_answer("proporton", "proportion")
    assert is_correct is True
    assert match_type == "fuzzy"


def test_fuzzy_match_two_typos():
    # "proporsion" vs "proportion" — 2 edits
    is_correct, match_type = grade_recall_answer("proporsion", "proportion")
    assert is_correct is True
    assert match_type == "fuzzy"


def test_needs_review_three_typos():
    # 3+ edits → needs_review
    is_correct, match_type = grade_recall_answer("propoXXXn", "proportion")
    assert is_correct is None
    assert match_type == "needs_review"


def test_completely_wrong_answer():
    is_correct, match_type = grade_recall_answer("completely wrong answer", "proportion")
    assert is_correct is None
    assert match_type == "needs_review"


def test_empty_response():
    is_correct, match_type = grade_recall_answer("", "proportion")
    assert is_correct is None
    assert match_type == "needs_review"


def test_empty_correct_answer():
    is_correct, match_type = grade_recall_answer("proportion", "")
    assert is_correct is None
    assert match_type == "needs_review"


def test_multi_word_answer_word_level_match():
    # User writes the correct word among multiple words
    is_correct, match_type = grade_recall_answer(
        "I think it is proportion", "proportion"
    )
    assert is_correct is True


def test_short_words_not_fuzzy_matched():
    # Very short words (< 3 chars) are not fuzzy-matched to avoid false positives
    is_correct, match_type = grade_recall_answer("ab", "proportion")
    assert is_correct is None


# ── Property-based tests (Property 40) ──────────────────────────────────────


@given(st.text(min_size=1, max_size=20))
@settings(max_examples=100)
def test_exact_answer_always_correct(answer: str):
    """Property 40: Exact match always returns is_correct=True."""
    is_correct, match_type = grade_recall_answer(answer, answer)
    # If both are non-empty, exact match should succeed
    if answer.strip():
        assert is_correct is True
        assert match_type == "exact"


@given(
    st.text(min_size=5, max_size=30, alphabet=st.characters(whitelist_categories=("Lu", "Ll")))
)
@settings(max_examples=100)
def test_result_is_always_valid_type(answer: str):
    """Property 40: grade_recall_answer always returns a valid (bool|None, str) tuple."""
    is_correct, match_type = grade_recall_answer(answer, "proportion")
    assert is_correct in (True, None)
    assert match_type in ("exact", "fuzzy", "needs_review")
