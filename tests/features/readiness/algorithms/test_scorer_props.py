"""Property-based tests for the readiness score pure scoring functions.

Uses Hypothesis to validate universal correctness properties across all valid inputs.
"""

from __future__ import annotations

import math

from hypothesis import given, settings, assume
from hypothesis.strategies import (
    composite,
    floats,
    integers,
    lists,
    sampled_from,
    tuples,
)

from app.features.readiness.algorithms.scorer import (
    ComponentWeights,
    ReadinessComponents,
    compute_coverage_component,
    compute_mastery_component,
    compute_mock_component,
    compute_readiness_score,
    compute_retention_component,
    redistribute_weights_no_mock,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_component_score = floats(
    min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
)

valid_mastery_score = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)

valid_exam_weight = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)

valid_retention = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)

valid_mock_percentage = floats(
    min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False
)

valid_days_since = integers(min_value=0, max_value=365)

valid_days_until_exam = integers(min_value=1, max_value=365)

valid_attempted = integers(min_value=0, max_value=200)

valid_available = integers(min_value=1, max_value=200)


@composite
def mastery_scores_with_positive_weight(draw):
    """Generate a non-empty list of (mastery_score, exam_weight) tuples
    where at least one weight is positive."""
    n = draw(integers(min_value=1, max_value=20))
    pairs = []
    for _ in range(n):
        score = draw(valid_mastery_score)
        weight = draw(valid_exam_weight)
        pairs.append((score, weight))
    # Ensure at least one positive weight
    total_weight = sum(w for _, w in pairs)
    assume(total_weight > 0.0)
    return pairs


@composite
def valid_weight_configs(draw):
    """Generate either standard or redistributed-no-mock weights."""
    use_standard = draw(sampled_from([True, False]))
    if use_standard:
        return ComponentWeights()
    else:
        return redistribute_weights_no_mock()


# ---------------------------------------------------------------------------
# Property 1: Readiness score is a valid weighted composite
# Validates: Requirements 1.1, 1.6, 1.8
# ---------------------------------------------------------------------------


class TestReadinessScoreValidWeightedComposite:
    """For any set of component values (mastery, retention, mock, coverage each in
    [0, 100]) and any valid weight configuration (standard or redistributed-no-mock),
    the computed readiness score SHALL equal the weighted sum of components, rounded
    to the nearest integer using half-up rounding, and clamped to the range [0, 100]
    inclusive.

    **Validates: Requirements 1.1, 1.6, 1.8**
    """

    @settings(max_examples=50)
    @given(
        mastery=valid_component_score,
        retention=valid_component_score,
        mock=valid_component_score,
        coverage=valid_component_score,
        weights=valid_weight_configs(),
    )
    def test_score_equals_weighted_sum_rounded_clamped(
        self,
        mastery: float,
        retention: float,
        mock: float,
        coverage: float,
        weights: ComponentWeights,
    ) -> None:
        """Score equals weighted sum, rounded half-up, clamped to [0, 100]."""
        components = ReadinessComponents(
            mastery_component=mastery,
            retention_component=retention,
            mock_component=mock,
            coverage_component=coverage,
        )
        result = compute_readiness_score(components, weights)

        raw = (
            mastery * weights.mastery
            + retention * weights.retention
            + mock * weights.mock_exam
            + coverage * weights.coverage
        )
        expected = max(0, min(100, int(math.floor(raw + 0.5))))

        assert result == expected

    @settings(max_examples=50)
    @given(
        mastery=valid_component_score,
        retention=valid_component_score,
        mock=valid_component_score,
        coverage=valid_component_score,
        weights=valid_weight_configs(),
    )
    def test_score_always_in_0_100(
        self,
        mastery: float,
        retention: float,
        mock: float,
        coverage: float,
        weights: ComponentWeights,
    ) -> None:
        """Score is always an integer in [0, 100] regardless of inputs."""
        components = ReadinessComponents(
            mastery_component=mastery,
            retention_component=retention,
            mock_component=mock,
            coverage_component=coverage,
        )
        result = compute_readiness_score(components, weights)
        assert isinstance(result, int)
        assert 0 <= result <= 100


# ---------------------------------------------------------------------------
# Property 2: Mastery component is a weighted average by exam proportion
# Validates: Requirements 1.2
# ---------------------------------------------------------------------------


class TestMasteryComponentWeightedAverage:
    """For any list of (mastery_score, exam_weight) pairs where mastery_score ∈
    [0.0, 1.0] and exam_weights have at least one positive value, the mastery
    component SHALL equal the weighted average scaled to 0–100.

    **Validates: Requirements 1.2**
    """

    @settings(max_examples=50)
    @given(mastery_scores=mastery_scores_with_positive_weight())
    def test_result_equals_weighted_average_scaled(
        self, mastery_scores: list[tuple[float, float]]
    ) -> None:
        """Mastery component equals weighted average × 100."""
        result = compute_mastery_component(mastery_scores)

        total_weight = sum(w for _, w in mastery_scores)
        weighted_sum = sum(s * w for s, w in mastery_scores)
        expected = (weighted_sum / total_weight) * 100.0

        assert abs(result - expected) < 1e-9

    @settings(max_examples=50)
    @given(mastery_scores=mastery_scores_with_positive_weight())
    def test_result_in_0_100(
        self, mastery_scores: list[tuple[float, float]]
    ) -> None:
        """Mastery component is always in [0, 100]."""
        result = compute_mastery_component(mastery_scores)
        assert 0.0 <= result <= 100.0 + 1e-9

    @settings(max_examples=50)
    @given(
        n=integers(min_value=1, max_value=20),
        weight=floats(min_value=0.01, max_value=1.0, allow_nan=False, allow_infinity=False),
    )
    def test_zero_mastery_reduces_average(self, n: int, weight: float) -> None:
        """Subtopics with mastery 0.0 reduce the weighted average proportionally."""
        # All zero mastery → result should be 0
        scores = [(0.0, weight) for _ in range(n)]
        result = compute_mastery_component(scores)
        assert abs(result - 0.0) < 1e-9

    def test_empty_input_returns_zero(self) -> None:
        """Empty input returns 0.0."""
        assert compute_mastery_component([]) == 0.0


# ---------------------------------------------------------------------------
# Property 3: Retention component uses FSRS with subtopic fallback
# Validates: Requirements 1.3
# ---------------------------------------------------------------------------


class TestRetentionComponentFSRSWithFallback:
    """When FSRS data exists, it's used; when empty/None, falls back to subtopic
    retention scores.

    **Validates: Requirements 1.3**
    """

    @settings(max_examples=50)
    @given(
        fsrs_retentions=lists(valid_retention, min_size=1, max_size=60),
        subtopic_scores=lists(valid_retention, min_size=1, max_size=60),
        days_until_exam=valid_days_until_exam,
    )
    def test_fsrs_used_when_available(
        self,
        fsrs_retentions: list[float],
        subtopic_scores: list[float],
        days_until_exam: int,
    ) -> None:
        """When FSRS retentions exist, result equals their average × 100."""
        result = compute_retention_component(
            fsrs_retentions, subtopic_scores, days_until_exam
        )
        expected = (sum(fsrs_retentions) / len(fsrs_retentions)) * 100.0
        assert abs(result - expected) < 1e-9

    @settings(max_examples=50)
    @given(
        subtopic_scores=lists(valid_retention, min_size=1, max_size=60),
        days_until_exam=valid_days_until_exam,
    )
    def test_fallback_to_subtopic_when_fsrs_empty(
        self, subtopic_scores: list[float], days_until_exam: int
    ) -> None:
        """When FSRS is empty list, subtopic retention average × 100 is used."""
        result = compute_retention_component([], subtopic_scores, days_until_exam)
        expected = (sum(subtopic_scores) / len(subtopic_scores)) * 100.0
        assert abs(result - expected) < 1e-9

    @settings(max_examples=50)
    @given(
        subtopic_scores=lists(valid_retention, min_size=1, max_size=60),
        days_until_exam=valid_days_until_exam,
    )
    def test_fallback_to_subtopic_when_fsrs_none(
        self, subtopic_scores: list[float], days_until_exam: int
    ) -> None:
        """When FSRS is None, subtopic retention average × 100 is used."""
        result = compute_retention_component(None, subtopic_scores, days_until_exam)
        expected = (sum(subtopic_scores) / len(subtopic_scores)) * 100.0
        assert abs(result - expected) < 1e-9

    @settings(max_examples=50)
    @given(days_until_exam=valid_days_until_exam)
    def test_both_empty_returns_zero(self, days_until_exam: int) -> None:
        """When both FSRS and subtopic scores are empty/None, returns 0."""
        assert compute_retention_component(None, None, days_until_exam) == 0.0
        assert compute_retention_component([], None, days_until_exam) == 0.0
        assert compute_retention_component(None, [], days_until_exam) == 0.0
        assert compute_retention_component([], [], days_until_exam) == 0.0

    @settings(max_examples=50)
    @given(
        fsrs_retentions=lists(valid_retention, min_size=0, max_size=60),
        subtopic_scores=lists(valid_retention, min_size=0, max_size=60),
        days_until_exam=valid_days_until_exam,
    )
    def test_result_in_0_100(
        self,
        fsrs_retentions: list[float],
        subtopic_scores: list[float],
        days_until_exam: int,
    ) -> None:
        """Result is always in [0, 100]."""
        fsrs = fsrs_retentions if fsrs_retentions else None
        sub = subtopic_scores if subtopic_scores else None
        result = compute_retention_component(fsrs, sub, days_until_exam)
        assert 0.0 <= result <= 100.0 + 1e-9


# ---------------------------------------------------------------------------
# Property 4: Mock component applies recency weighting
# Validates: Requirements 1.4
# ---------------------------------------------------------------------------


class TestMockComponentRecencyWeighting:
    """Recent exams (≤14d) get weight 1.0, mid (15-30d) get 0.7, old (>30d) get 0.4.

    **Validates: Requirements 1.4**
    """

    @settings(max_examples=50)
    @given(
        mock_scores=lists(
            tuples(valid_mock_percentage, valid_days_since),
            min_size=1,
            max_size=20,
        ),
    )
    def test_result_equals_recency_weighted_average(
        self, mock_scores: list[tuple[float, int]]
    ) -> None:
        """Mock component equals weighted average with recency weights."""
        result = compute_mock_component(mock_scores)

        total_weight = 0.0
        weighted_sum = 0.0
        for pct, days in mock_scores:
            if days <= 14:
                w = 1.0
            elif days <= 30:
                w = 0.7
            else:
                w = 0.4
            weighted_sum += pct * w
            total_weight += w

        expected = weighted_sum / total_weight if total_weight > 0 else 0.0
        assert abs(result - expected) < 1e-9

    @settings(max_examples=50)
    @given(
        mock_scores=lists(
            tuples(valid_mock_percentage, valid_days_since),
            min_size=1,
            max_size=20,
        ),
    )
    def test_result_in_0_100(
        self, mock_scores: list[tuple[float, int]]
    ) -> None:
        """Mock component is always in [0, 100]."""
        result = compute_mock_component(mock_scores)
        assert 0.0 <= result <= 100.0 + 1e-9

    @settings(max_examples=50)
    @given(pct=valid_mock_percentage)
    def test_recent_exam_weight_1(self, pct: float) -> None:
        """Exam at exactly 14 days gets weight 1.0 (single exam = raw score)."""
        result = compute_mock_component([(pct, 14)])
        assert abs(result - pct) < 1e-9

    @settings(max_examples=50)
    @given(pct=valid_mock_percentage)
    def test_mid_exam_weight_07(self, pct: float) -> None:
        """Exam at exactly 15 days gets weight 0.7 (single exam = raw score)."""
        result = compute_mock_component([(pct, 15)])
        # Single exam: weighted_sum = pct * 0.7, total_weight = 0.7 → result = pct
        assert abs(result - pct) < 1e-9

    @settings(max_examples=50)
    @given(pct=valid_mock_percentage)
    def test_old_exam_weight_04(self, pct: float) -> None:
        """Exam at exactly 31 days gets weight 0.4 (single exam = raw score)."""
        result = compute_mock_component([(pct, 31)])
        assert abs(result - pct) < 1e-9

    def test_empty_returns_zero(self) -> None:
        """Empty input returns 0."""
        assert compute_mock_component([]) == 0.0


# ---------------------------------------------------------------------------
# Property 5: Coverage component counts threshold-meeting subtopics
# Validates: Requirements 1.5
# ---------------------------------------------------------------------------


class TestCoverageComponentThresholdCounting:
    """Percentage of subtopics meeting the 10% attempted threshold.

    **Validates: Requirements 1.5**
    """

    @settings(max_examples=50)
    @given(
        coverage=lists(
            tuples(valid_attempted, valid_available),
            min_size=1,
            max_size=60,
        ),
    )
    def test_result_equals_threshold_meeting_percentage(
        self, coverage: list[tuple[int, int]]
    ) -> None:
        """Coverage equals (count meeting threshold / total subtopics) × 100."""
        result = compute_coverage_component(coverage)

        meeting = 0
        for attempted, available in coverage:
            if available > 0 and attempted >= 0.10 * available:
                meeting += 1

        expected = (meeting / len(coverage)) * 100.0
        assert abs(result - expected) < 1e-9

    @settings(max_examples=50)
    @given(
        coverage=lists(
            tuples(valid_attempted, valid_available),
            min_size=1,
            max_size=60,
        ),
    )
    def test_result_in_0_100(
        self, coverage: list[tuple[int, int]]
    ) -> None:
        """Coverage component is always in [0, 100]."""
        result = compute_coverage_component(coverage)
        assert 0.0 <= result <= 100.0 + 1e-9

    @settings(max_examples=50)
    @given(
        available=integers(min_value=1, max_value=200),
    )
    def test_exact_threshold_meets(self, available: int) -> None:
        """A subtopic with exactly 10% attempted meets the threshold."""
        attempted = math.ceil(0.10 * available)
        result = compute_coverage_component([(attempted, available)])
        assert result == 100.0

    @settings(max_examples=50)
    @given(
        available=integers(min_value=11, max_value=200),
    )
    def test_below_threshold_does_not_meet(self, available: int) -> None:
        """A subtopic with strictly less than 10% attempted fails the threshold."""
        attempted = int(0.10 * available) - 1
        assume(attempted >= 0)
        # Verify this is indeed below threshold
        assume(attempted < 0.10 * available)
        result = compute_coverage_component([(attempted, available)])
        assert result == 0.0

    def test_empty_returns_zero(self) -> None:
        """Empty input returns 0."""
        assert compute_coverage_component([]) == 0.0
