"""Property-based tests for the FSRS spaced repetition engine.

Uses Hypothesis to validate universal correctness properties across all valid inputs.
"""

from __future__ import annotations

import math
from datetime import date, timedelta

from hypothesis import given, settings
from hypothesis.strategies import (
    composite,
    dates,
    floats,
    integers,
    sampled_from,
)

from app.features.flashcards.algorithms.fsrs import (
    CardState,
    compute_mastery_percentage,
    compute_next_interval,
    compute_retention_score,
)
from app.features.flashcards.models import ConfidenceLevel, ResponseType


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_ease_factor = floats(
    min_value=1.3, max_value=3.5, allow_nan=False, allow_infinity=False
)
valid_retention_score = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)
valid_memory_stability = floats(
    min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False
)
valid_review_interval = integers(min_value=1, max_value=365)
valid_lapse_count = integers(min_value=0, max_value=50)
valid_confidence = sampled_from(list(ConfidenceLevel))


@composite
def today_and_last_review(draw):
    """Generate a (today, last_review_date) pair where today >= last_review_date
    when last_review_date is not None. This reflects real usage where today is
    always the current date and last_review_date is in the past or None."""
    today = draw(dates(min_value=date(2020, 1, 1), max_value=date(2030, 12, 31)))
    has_last_review = draw(sampled_from([True, False]))
    if has_last_review:
        days_ago = draw(integers(min_value=0, max_value=365))
        last_review_date = today - timedelta(days=days_ago)
    else:
        last_review_date = None
    return today, last_review_date


# ---------------------------------------------------------------------------
# Property 1: FSRS interval computation correctness
# Validates: Requirements 5.2, 5.3, 5.4, 5.5, 10.2
# ---------------------------------------------------------------------------


class TestFSRSIntervalComputationCorrectness:
    """For ANY valid CardState and ANY response/confidence combination,
    compute_next_interval should produce the correct interval per the formulas.

    **Validates: Requirements 5.2, 5.3, 5.4, 5.5, 10.2**
    """

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
    )
    def test_remembered_mastered_interval(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
    ) -> None:
        """Validates: Requirements 5.2

        remembered + mastered: interval = floor(review_interval * ease_factor),
        clamped to [1, 365].
        """
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.MASTERED, today
        )
        expected_raw = review_interval * ease_factor
        expected_interval = max(1, min(365, math.floor(expected_raw)))
        assert result.review_interval == expected_interval

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
    )
    def test_remembered_confident_interval(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
    ) -> None:
        """Validates: Requirements 5.3

        remembered + confident: interval = floor(review_interval * (ease_factor * 0.85)),
        clamped to [1, 365].
        """
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.CONFIDENT, today
        )
        expected_raw = review_interval * (ease_factor * 0.85)
        expected_interval = max(1, min(365, math.floor(expected_raw)))
        assert result.review_interval == expected_interval

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
    )
    def test_remembered_unsure_interval(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
    ) -> None:
        """Validates: Requirements 5.4

        remembered + unsure: interval = max(1, floor(review_interval * 0.5)).
        """
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.UNSURE, today
        )
        expected_interval = max(1, math.floor(review_interval * 0.5))
        assert result.review_interval == expected_interval

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
    )
    def test_remembered_guessed_interval(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
    ) -> None:
        """Validates: Requirements 10.2

        remembered + guessed: interval = floor(review_interval * ease_factor * 0.3),
        clamped to [1, 365].
        """
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(
            state, ResponseType.REMEMBERED, ConfidenceLevel.GUESSED, today
        )
        expected_raw = review_interval * ease_factor * 0.3
        expected_interval = max(1, min(365, math.floor(expected_raw)))
        assert result.review_interval == expected_interval

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
    )
    def test_forgot_interval_always_1(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
    ) -> None:
        """Validates: Requirements 5.5

        forgot: interval is always reset to 1 regardless of current state.
        """
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(
            state, ResponseType.FORGOT, ConfidenceLevel.UNSURE, today
        )
        assert result.review_interval == 1

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        confidence=valid_confidence,
        today_and_review=today_and_last_review(),
    )
    def test_all_results_have_interval_in_valid_range(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        confidence: ConfidenceLevel,
        today_and_review: tuple[date, date | None],
    ) -> None:
        """Validates: Requirements 5.2, 5.3, 5.4, 5.5, 10.2

        All results must have review_interval in [1, 365] regardless of inputs.
        """
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        for response in ResponseType:
            result = compute_next_interval(state, response, confidence, today)
            assert 1 <= result.review_interval <= 365, (
                f"review_interval {result.review_interval} out of range "
                f"for response={response}, confidence={confidence}"
            )


# ---------------------------------------------------------------------------
# Property 3: FSRS determinism
# Validates: Requirements 5.10
# ---------------------------------------------------------------------------


class TestFSRSDeterminism:
    """**Validates: Requirements 5.10**

    For ANY valid CardState, response, confidence, and today date:
    calling compute_next_interval twice with the same arguments produces
    EXACTLY the same SchedulingResult.
    """

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
        confidence=valid_confidence,
    )
    def test_identical_inputs_produce_identical_outputs(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple,
        confidence: ConfidenceLevel,
    ) -> None:
        """Same inputs always produce same outputs -- no hidden state or randomness."""
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )

        for response in ResponseType:
            result1 = compute_next_interval(state, response, confidence, today)
            result2 = compute_next_interval(state, response, confidence, today)

            assert result1.ease_factor == result2.ease_factor
            assert result1.retention_score == result2.retention_score
            assert result1.memory_stability == result2.memory_stability
            assert result1.review_interval == result2.review_interval
            assert result1.lapse_count == result2.lapse_count
            assert result1.next_review_date == result2.next_review_date


# ---------------------------------------------------------------------------
# Property 2: FSRS parameter invariants
# Validates: Requirements 5.1, 5.8, 5.9
# ---------------------------------------------------------------------------


class TestFSRSParameterInvariants:
    """For ANY valid CardState and ANY response/confidence combination,
    the output SchedulingResult always satisfies parameter bounds.

    **Validates: Requirements 5.1, 5.8, 5.9**
    """

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
        confidence=valid_confidence,
        response=sampled_from(list(ResponseType)),
    )
    def test_ease_factor_always_in_bounds(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
        confidence: ConfidenceLevel,
        response: ResponseType,
    ) -> None:
        """ease_factor is always clamped to [1.3, 3.5] (Req 5.8)."""
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(state, response, confidence, today)
        assert 1.3 <= result.ease_factor <= 3.5, (
            f"ease_factor {result.ease_factor} out of [1.3, 3.5]"
        )

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
        confidence=valid_confidence,
        response=sampled_from(list(ResponseType)),
    )
    def test_memory_stability_always_at_least_01(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
        confidence: ConfidenceLevel,
        response: ResponseType,
    ) -> None:
        """memory_stability is always >= 0.1 (Req 5.9)."""
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(state, response, confidence, today)
        assert result.memory_stability >= 0.1, (
            f"memory_stability {result.memory_stability} < 0.1"
        )

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
        confidence=valid_confidence,
        response=sampled_from(list(ResponseType)),
    )
    def test_retention_score_always_in_0_1(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
        confidence: ConfidenceLevel,
        response: ResponseType,
    ) -> None:
        """retention_score is always in [0.0, 1.0] (Req 5.1)."""
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(state, response, confidence, today)
        assert 0.0 <= result.retention_score <= 1.0, (
            f"retention_score {result.retention_score} out of [0.0, 1.0]"
        )

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
        confidence=valid_confidence,
        response=sampled_from(list(ResponseType)),
    )
    def test_lapse_count_never_negative(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
        confidence: ConfidenceLevel,
        response: ResponseType,
    ) -> None:
        """lapse_count never decreases below 0."""
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(state, response, confidence, today)
        assert result.lapse_count >= 0


# ---------------------------------------------------------------------------
# Property 4: FSRS round-trip scheduling
# Validates: Requirements 5.11
# ---------------------------------------------------------------------------


class TestFSRSRoundTripScheduling:
    """For ANY valid CardState, the next_review_date is always
    today + review_interval days.

    **Validates: Requirements 5.11**
    """

    @settings(max_examples=100)
    @given(
        ease_factor=valid_ease_factor,
        retention_score=valid_retention_score,
        memory_stability=valid_memory_stability,
        review_interval=valid_review_interval,
        lapse_count=valid_lapse_count,
        today_and_review=today_and_last_review(),
        confidence=valid_confidence,
        response=sampled_from(list(ResponseType)),
    )
    def test_next_review_date_equals_today_plus_interval(
        self,
        ease_factor: float,
        retention_score: float,
        memory_stability: float,
        review_interval: int,
        lapse_count: int,
        today_and_review: tuple[date, date | None],
        confidence: ConfidenceLevel,
        response: ResponseType,
    ) -> None:
        """next_review_date == today + timedelta(days=result.review_interval)."""
        today, last_review_date = today_and_review
        state = CardState(
            ease_factor=ease_factor,
            retention_score=retention_score,
            memory_stability=memory_stability,
            review_interval=review_interval,
            lapse_count=lapse_count,
            last_review_date=last_review_date,
        )
        result = compute_next_interval(state, response, confidence, today)
        expected_date = today + timedelta(days=result.review_interval)
        assert result.next_review_date == expected_date


# ---------------------------------------------------------------------------
# Property 5: Retention score formula
# Validates: Requirements 5.6
# ---------------------------------------------------------------------------


class TestRetentionScoreFormula:
    """For ANY valid memory_stability and elapsed_days,
    compute_retention_score returns e^(-elapsed_days / memory_stability).

    **Validates: Requirements 5.6**
    """

    @settings(max_examples=100)
    @given(
        memory_stability=floats(
            min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False
        ),
        elapsed_days=floats(
            min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_formula_matches_exponential_decay(
        self, memory_stability: float, elapsed_days: float
    ) -> None:
        """retention_score == e^(-elapsed_days / memory_stability)."""
        result = compute_retention_score(memory_stability, elapsed_days)
        expected = math.exp(-elapsed_days / memory_stability)
        assert abs(result - expected) < 1e-10

    @settings(max_examples=100)
    @given(
        memory_stability=floats(
            min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False
        ),
        elapsed_days=floats(
            min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_result_always_in_0_1(
        self, memory_stability: float, elapsed_days: float
    ) -> None:
        """Result is always in [0.0, 1.0]."""
        result = compute_retention_score(memory_stability, elapsed_days)
        assert 0.0 <= result <= 1.0

    @settings(max_examples=100)
    @given(
        memory_stability=floats(
            min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_zero_elapsed_returns_1(self, memory_stability: float) -> None:
        """When elapsed_days == 0, retention is 1.0 (perfect recall)."""
        result = compute_retention_score(memory_stability, 0.0)
        assert abs(result - 1.0) < 1e-10

    @settings(max_examples=100)
    @given(
        memory_stability=floats(
            min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False
        ),
        elapsed_a=floats(
            min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False
        ),
        elapsed_b=floats(
            min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_monotonically_decreasing(
        self, memory_stability: float, elapsed_a: float, elapsed_b: float
    ) -> None:
        """More elapsed days → lower retention (monotonically decreasing)."""
        result_a = compute_retention_score(memory_stability, elapsed_a)
        result_b = compute_retention_score(memory_stability, elapsed_b)
        if elapsed_a < elapsed_b:
            assert result_a >= result_b
        elif elapsed_a > elapsed_b:
            assert result_a <= result_b


# ---------------------------------------------------------------------------
# Property 6: Mastery percentage formula
# Validates: Requirements 5.7
# ---------------------------------------------------------------------------


class TestMasteryPercentageFormula:
    """For ANY valid inputs, compute_mastery_percentage returns
    (successful / total) * retention_score * 100, capped at 100.

    **Validates: Requirements 5.7**
    """

    @settings(max_examples=100)
    @given(
        successful=integers(min_value=0, max_value=1000),
        total=integers(min_value=1, max_value=1000),
        retention_score=floats(
            min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_formula_correctness(
        self, successful: int, total: int, retention_score: float
    ) -> None:
        """mastery == min(100, (successful / total) * retention_score * 100)."""
        # Ensure successful <= total for realistic inputs
        successful = min(successful, total)
        result = compute_mastery_percentage(successful, total, retention_score)
        expected = min(100.0, (successful / total) * retention_score * 100.0)
        assert abs(result - expected) < 1e-10

    @settings(max_examples=100)
    @given(
        successful=integers(min_value=0, max_value=1000),
        total=integers(min_value=1, max_value=1000),
        retention_score=floats(
            min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_result_capped_at_100(
        self, successful: int, total: int, retention_score: float
    ) -> None:
        """Result is always <= 100.0."""
        result = compute_mastery_percentage(successful, total, retention_score)
        assert result <= 100.0

    @settings(max_examples=100)
    @given(
        successful=integers(min_value=0, max_value=1000),
        total=integers(min_value=1, max_value=1000),
        retention_score=floats(
            min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_result_non_negative(
        self, successful: int, total: int, retention_score: float
    ) -> None:
        """Result is always >= 0.0."""
        successful = min(successful, total)
        result = compute_mastery_percentage(successful, total, retention_score)
        assert result >= 0.0

    @settings(max_examples=100)
    @given(
        retention_score=floats(
            min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
        ),
    )
    def test_zero_total_returns_zero(self, retention_score: float) -> None:
        """When total_reviews == 0, mastery is 0.0."""
        result = compute_mastery_percentage(0, 0, retention_score)
        assert result == 0.0
