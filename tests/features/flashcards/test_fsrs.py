"""Unit tests for the FSRS spaced repetition engine pure functions.

Tests cover all scheduling rules, clamping, retention score, and mastery percentage.
"""

from __future__ import annotations

import math
from datetime import date, timedelta

from app.features.flashcards.algorithms.fsrs import (
    CardState,
    compute_mastery_percentage,
    compute_next_interval,
    compute_retention_score,
)
from app.features.flashcards.models import ConfidenceLevel, ResponseType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _default_state(**kwargs) -> CardState:
    defaults = {
        "ease_factor": 2.5,
        "retention_score": 0.0,
        "memory_stability": 1.0,
        "review_interval": 1,
        "lapse_count": 0,
        "last_review_date": None,
    }
    defaults.update(kwargs)
    return CardState(**defaults)


TODAY = date(2025, 1, 15)


# ---------------------------------------------------------------------------
# compute_next_interval — remembered + mastered (Req 5.2)
# ---------------------------------------------------------------------------


class TestRememberedMastered:
    def test_interval_multiplied_by_ease_factor(self):
        state = _default_state(review_interval=10, ease_factor=2.5)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.MASTERED, TODAY
        )
        # 10 * 2.5 = 25
        assert result.review_interval == 25

    def test_memory_stability_increased_by_10_percent(self):
        state = _default_state(memory_stability=2.0)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.MASTERED, TODAY
        )
        assert math.isclose(result.memory_stability, 2.2, rel_tol=1e-9)

    def test_interval_clamped_to_365(self):
        state = _default_state(review_interval=200, ease_factor=3.0)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.MASTERED, TODAY
        )
        # 200 * 3.0 = 600 → clamped to 365
        assert result.review_interval == 365

    def test_next_review_date_set_correctly(self):
        state = _default_state(review_interval=10, ease_factor=2.0)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.MASTERED, TODAY
        )
        # 10 * 2.0 = 20
        assert result.next_review_date == TODAY + timedelta(days=20)


# ---------------------------------------------------------------------------
# compute_next_interval — remembered + confident (Req 5.3)
# ---------------------------------------------------------------------------


class TestRememberedConfident:
    def test_interval_multiplied_by_ease_times_085(self):
        state = _default_state(review_interval=10, ease_factor=2.5)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.CONFIDENT, TODAY
        )
        # 10 * (2.5 * 0.85) = 10 * 2.125 = 21.25 → floor = 21
        assert result.review_interval == 21

    def test_memory_stability_unchanged(self):
        state = _default_state(memory_stability=2.0)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.CONFIDENT, TODAY
        )
        assert math.isclose(result.memory_stability, 2.0, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# compute_next_interval — remembered + unsure (Req 5.4)
# ---------------------------------------------------------------------------


class TestRememberedUnsure:
    def test_interval_halved(self):
        state = _default_state(review_interval=10)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.UNSURE, TODAY
        )
        # max(1, floor(10 * 0.5)) = 5
        assert result.review_interval == 5

    def test_interval_minimum_1(self):
        state = _default_state(review_interval=1)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.UNSURE, TODAY
        )
        # max(1, floor(1 * 0.5)) = max(1, 0) = 1
        assert result.review_interval == 1

    def test_memory_stability_decreased_by_10_percent(self):
        state = _default_state(memory_stability=2.0)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.UNSURE, TODAY
        )
        assert math.isclose(result.memory_stability, 1.8, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# compute_next_interval — remembered + guessed (Req 10.2)
# ---------------------------------------------------------------------------


class TestRememberedGuessed:
    def test_interval_uses_03_multiplier(self):
        state = _default_state(review_interval=10, ease_factor=2.5)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.GUESSED, TODAY
        )
        # 10 * 2.5 * 0.3 = 7.5 → floor = 7
        assert result.review_interval == 7

    def test_small_interval_clamped_to_1(self):
        state = _default_state(review_interval=1, ease_factor=1.3)
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.GUESSED, TODAY
        )
        # 1 * 1.3 * 0.3 = 0.39 → floor = 0 → max(1, 0) = 1
        assert result.review_interval == 1


# ---------------------------------------------------------------------------
# compute_next_interval — forgot (Req 5.5)
# ---------------------------------------------------------------------------


class TestForgot:
    def test_interval_reset_to_1(self):
        state = _default_state(review_interval=30)
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, TODAY
        )
        assert result.review_interval == 1

    def test_lapse_count_incremented(self):
        state = _default_state(lapse_count=2)
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, TODAY
        )
        assert result.lapse_count == 3

    def test_ease_factor_decreased_by_02(self):
        state = _default_state(ease_factor=2.5)
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, TODAY
        )
        assert math.isclose(result.ease_factor, 2.3, rel_tol=1e-9)

    def test_ease_factor_clamped_to_13(self):
        state = _default_state(ease_factor=1.4)
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, TODAY
        )
        # 1.4 - 0.2 = 1.2 → clamped to 1.3
        assert math.isclose(result.ease_factor, 1.3, rel_tol=1e-9)

    def test_memory_stability_reduced_by_30_percent(self):
        state = _default_state(memory_stability=2.0)
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, TODAY
        )
        assert math.isclose(result.memory_stability, 1.4, rel_tol=1e-9)

    def test_memory_stability_clamped_to_01(self):
        state = _default_state(memory_stability=0.1)
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, TODAY
        )
        # 0.1 * 0.7 = 0.07 → clamped to 0.1
        assert math.isclose(result.memory_stability, 0.1, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# compute_next_interval — skipped
# ---------------------------------------------------------------------------


class TestSkipped:
    def test_interval_unchanged(self):
        state = _default_state(review_interval=10)
        result = compute_next_interval(
            state, ResponseType.SKIPPED, ConfidenceLevel.UNSURE, TODAY
        )
        assert result.review_interval == 10

    def test_ease_factor_unchanged(self):
        state = _default_state(ease_factor=2.5)
        result = compute_next_interval(
            state, ResponseType.SKIPPED, ConfidenceLevel.UNSURE, TODAY
        )
        assert math.isclose(result.ease_factor, 2.5, rel_tol=1e-9)

    def test_lapse_count_unchanged(self):
        state = _default_state(lapse_count=3)
        result = compute_next_interval(
            state, ResponseType.SKIPPED, ConfidenceLevel.UNSURE, TODAY
        )
        assert result.lapse_count == 3


# ---------------------------------------------------------------------------
# compute_next_interval — determinism (Req 5.10)
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_same_inputs_produce_same_outputs(self):
        state = _default_state(
            review_interval=10,
            ease_factor=2.5,
            memory_stability=2.0,
            last_review_date=date(2025, 1, 10),
        )
        result1 = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.CONFIDENT, TODAY
        )
        result2 = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.CONFIDENT, TODAY
        )
        assert result1 == result2


# ---------------------------------------------------------------------------
# compute_retention_score (Req 5.6)
# ---------------------------------------------------------------------------


class TestRetentionScore:
    def test_zero_elapsed_days_returns_1(self):
        score = compute_retention_score(memory_stability=5.0, elapsed_days=0.0)
        assert math.isclose(score, 1.0, rel_tol=1e-9)

    def test_formula_correctness(self):
        # e^(-7 / 10) ≈ 0.4966
        score = compute_retention_score(memory_stability=10.0, elapsed_days=7.0)
        expected = math.exp(-7.0 / 10.0)
        assert math.isclose(score, expected, rel_tol=1e-9)

    def test_large_elapsed_days_approaches_zero(self):
        score = compute_retention_score(memory_stability=1.0, elapsed_days=100.0)
        assert score < 0.001

    def test_stability_clamped_to_minimum(self):
        # Even if 0.0 is passed, should use 0.1
        score = compute_retention_score(memory_stability=0.0, elapsed_days=1.0)
        expected = math.exp(-1.0 / 0.1)
        assert math.isclose(score, expected, rel_tol=1e-9)


# ---------------------------------------------------------------------------
# compute_mastery_percentage (Req 5.7)
# ---------------------------------------------------------------------------


class TestMasteryPercentage:
    def test_basic_calculation(self):
        # (8/10) * 0.9 * 100 = 72.0
        result = compute_mastery_percentage(
            successful_reviews=8, total_reviews=10, retention_score=0.9
        )
        assert math.isclose(result, 72.0, rel_tol=1e-9)

    def test_capped_at_100(self):
        # (10/10) * 1.0 * 100 = 100.0
        result = compute_mastery_percentage(
            successful_reviews=10, total_reviews=10, retention_score=1.0
        )
        assert result == 100.0

    def test_zero_total_reviews_returns_zero(self):
        result = compute_mastery_percentage(
            successful_reviews=0, total_reviews=0, retention_score=0.9
        )
        assert result == 0.0

    def test_zero_successful_reviews(self):
        result = compute_mastery_percentage(
            successful_reviews=0, total_reviews=10, retention_score=0.9
        )
        assert result == 0.0

    def test_perfect_score_with_high_retention(self):
        # (10/10) * 0.95 * 100 = 95.0
        result = compute_mastery_percentage(
            successful_reviews=10, total_reviews=10, retention_score=0.95
        )
        assert math.isclose(result, 95.0, rel_tol=1e-9)
