"""Unit tests for readiness score pure scoring functions."""

from app.features.readiness.algorithms.scorer import (
    ComponentWeights,
    ReadinessComponents,
    ReadinessResult,
    compute_coverage_component,
    compute_mastery_component,
    compute_mock_component,
    compute_readiness_score,
    compute_retention_component,
    redistribute_weights_no_mock,
)


# ---------------------------------------------------------------------------
# compute_mastery_component
# ---------------------------------------------------------------------------


class TestComputeMasteryComponent:
    def test_empty_list_returns_zero(self) -> None:
        assert compute_mastery_component([]) == 0.0

    def test_single_subtopic_full_mastery(self) -> None:
        result = compute_mastery_component([(1.0, 0.5)])
        assert result == 100.0

    def test_single_subtopic_half_mastery(self) -> None:
        result = compute_mastery_component([(0.5, 1.0)])
        assert result == 50.0

    def test_weighted_average_with_different_weights(self) -> None:
        # subtopic A: mastery 0.8, weight 0.6 (60% of exam)
        # subtopic B: mastery 0.4, weight 0.4 (40% of exam)
        # expected: (0.8*0.6 + 0.4*0.4) / (0.6+0.4) * 100 = (0.48+0.16)/1.0 * 100 = 64.0
        result = compute_mastery_component([(0.8, 0.6), (0.4, 0.4)])
        assert abs(result - 64.0) < 1e-10

    def test_zero_mastery_returns_zero(self) -> None:
        result = compute_mastery_component([(0.0, 0.5), (0.0, 0.5)])
        assert result == 0.0

    def test_all_zero_weights_returns_zero(self) -> None:
        result = compute_mastery_component([(0.8, 0.0), (0.6, 0.0)])
        assert result == 0.0


# ---------------------------------------------------------------------------
# compute_retention_component
# ---------------------------------------------------------------------------


class TestComputeRetentionComponent:
    def test_both_none_returns_zero(self) -> None:
        assert compute_retention_component(None, None, 30) == 0.0

    def test_both_empty_returns_zero(self) -> None:
        assert compute_retention_component([], [], 30) == 0.0

    def test_fsrs_retentions_used_when_available(self) -> None:
        # Average of [0.8, 0.6] = 0.7 → 70.0
        result = compute_retention_component([0.8, 0.6], [0.5], 30)
        assert abs(result - 70.0) < 1e-10

    def test_fallback_to_subtopic_when_fsrs_empty(self) -> None:
        # Average of [0.9, 0.7] = 0.8 → 80.0
        result = compute_retention_component([], [0.9, 0.7], 30)
        assert abs(result - 80.0) < 1e-10

    def test_fallback_to_subtopic_when_fsrs_none(self) -> None:
        result = compute_retention_component(None, [0.6, 0.4], 30)
        assert abs(result - 50.0) < 1e-10

    def test_perfect_retention(self) -> None:
        result = compute_retention_component([1.0, 1.0, 1.0], None, 30)
        assert result == 100.0


# ---------------------------------------------------------------------------
# compute_mock_component
# ---------------------------------------------------------------------------


class TestComputeMockComponent:
    def test_empty_returns_zero(self) -> None:
        assert compute_mock_component([]) == 0.0

    def test_single_recent_exam(self) -> None:
        # 80% correct, 7 days ago → weight 1.0
        result = compute_mock_component([(80.0, 7)])
        assert result == 80.0

    def test_recency_weighting(self) -> None:
        # Exam 1: 90%, 10 days ago → weight 1.0
        # Exam 2: 60%, 20 days ago → weight 0.7
        # weighted avg = (90*1.0 + 60*0.7) / (1.0 + 0.7) = (90+42)/1.7 ≈ 77.647
        result = compute_mock_component([(90.0, 10), (60.0, 20)])
        expected = (90.0 * 1.0 + 60.0 * 0.7) / (1.0 + 0.7)
        assert abs(result - expected) < 1e-10

    def test_old_exam_gets_low_weight(self) -> None:
        # Exam 1: 70%, 50 days ago → weight 0.4
        result = compute_mock_component([(70.0, 50)])
        assert result == 70.0  # single exam, weight cancels out

    def test_all_weight_brackets(self) -> None:
        # Recent (14 days): 100%, weight 1.0
        # Mid (30 days): 50%, weight 0.7
        # Old (60 days): 25%, weight 0.4
        # weighted = (100*1.0 + 50*0.7 + 25*0.4) / (1.0+0.7+0.4) = (100+35+10)/2.1 ≈ 69.048
        result = compute_mock_component([(100.0, 14), (50.0, 30), (25.0, 60)])
        expected = (100.0 * 1.0 + 50.0 * 0.7 + 25.0 * 0.4) / (1.0 + 0.7 + 0.4)
        assert abs(result - expected) < 1e-10

    def test_boundary_14_days_gets_weight_1(self) -> None:
        result = compute_mock_component([(80.0, 14)])
        assert result == 80.0

    def test_boundary_15_days_gets_weight_07(self) -> None:
        # Single exam at exactly 15 days → weight 0.7, but single item so avg = score
        result = compute_mock_component([(80.0, 15)])
        assert result == 80.0

    def test_boundary_30_days_gets_weight_07(self) -> None:
        result = compute_mock_component([(80.0, 30)])
        assert result == 80.0

    def test_boundary_31_days_gets_weight_04(self) -> None:
        result = compute_mock_component([(80.0, 31)])
        assert result == 80.0


# ---------------------------------------------------------------------------
# compute_coverage_component
# ---------------------------------------------------------------------------


class TestComputeCoverageComponent:
    def test_empty_returns_zero(self) -> None:
        assert compute_coverage_component([]) == 0.0

    def test_all_subtopics_meeting_threshold(self) -> None:
        # 3 subtopics, all with >= 10% attempted
        coverage = [(10, 60), (8, 60), (6, 60)]
        result = compute_coverage_component(coverage)
        # 10/60=0.167, 8/60=0.133, 6/60=0.10 — all meet threshold
        assert result == 100.0

    def test_no_subtopics_meeting_threshold(self) -> None:
        # 3 subtopics, all below threshold
        coverage = [(5, 60), (3, 60), (0, 60)]
        result = compute_coverage_component(coverage)
        assert result == 0.0

    def test_partial_coverage(self) -> None:
        # 4 subtopics, 2 meeting threshold
        coverage = [(6, 60), (7, 60), (3, 60), (2, 60)]
        result = compute_coverage_component(coverage)
        # 6/60=0.10 (meets), 7/60=0.117 (meets), 3/60=0.05 (no), 2/60=0.033 (no)
        assert abs(result - 50.0) < 1e-10

    def test_exact_threshold_meets(self) -> None:
        # exactly 10% of 60 = 6 attempted
        coverage = [(6, 60)]
        result = compute_coverage_component(coverage)
        assert result == 100.0

    def test_below_threshold_does_not_meet(self) -> None:
        # 5 out of 60 = 8.3% < 10%
        coverage = [(5, 60)]
        result = compute_coverage_component(coverage)
        assert result == 0.0

    def test_custom_threshold(self) -> None:
        coverage = [(3, 60)]  # 3/60 = 5%
        assert compute_coverage_component(coverage, threshold=0.05) == 100.0
        assert compute_coverage_component(coverage, threshold=0.10) == 0.0


# ---------------------------------------------------------------------------
# compute_readiness_score
# ---------------------------------------------------------------------------


class TestComputeReadinessScore:
    def test_all_zeros(self) -> None:
        components = ReadinessComponents(0.0, 0.0, 0.0, 0.0)
        weights = ComponentWeights()
        assert compute_readiness_score(components, weights) == 0

    def test_all_hundreds(self) -> None:
        components = ReadinessComponents(100.0, 100.0, 100.0, 100.0)
        weights = ComponentWeights()
        assert compute_readiness_score(components, weights) == 100

    def test_weighted_combination(self) -> None:
        components = ReadinessComponents(
            mastery_component=80.0,
            retention_component=60.0,
            mock_component=70.0,
            coverage_component=50.0,
        )
        weights = ComponentWeights()
        # 80*0.40 + 60*0.25 + 70*0.25 + 50*0.10 = 32 + 15 + 17.5 + 5 = 69.5
        # half-up rounding: 70
        assert compute_readiness_score(components, weights) == 70

    def test_half_up_rounding(self) -> None:
        # Create a case where raw score is exactly X.5
        # 50*0.40 + 50*0.25 + 50*0.25 + 50*0.10 = 50.0 → rounds to 50
        components = ReadinessComponents(50.0, 50.0, 50.0, 50.0)
        weights = ComponentWeights()
        assert compute_readiness_score(components, weights) == 50

    def test_half_up_rounding_exact_half(self) -> None:
        # Need raw = X.5 → rounds up
        # 75*0.40 + 50*0.25 + 50*0.25 + 50*0.10 = 30 + 12.5 + 12.5 + 5 = 60.0
        # Let's try: mastery=81, ret=50, mock=50, cov=50
        # 81*0.40 + 50*0.25 + 50*0.25 + 50*0.10 = 32.4+12.5+12.5+5 = 62.4 → 62
        # Try: mastery=81.25, others=50
        # 81.25*0.40 = 32.5, rest = 30 → 62.5 → rounds to 63
        components = ReadinessComponents(81.25, 50.0, 50.0, 50.0)
        weights = ComponentWeights()
        assert compute_readiness_score(components, weights) == 63

    def test_clamp_above_100(self) -> None:
        # With extreme component values (shouldn't happen but we clamp anyway)
        components = ReadinessComponents(150.0, 150.0, 150.0, 150.0)
        weights = ComponentWeights()
        assert compute_readiness_score(components, weights) == 100

    def test_clamp_below_zero(self) -> None:
        components = ReadinessComponents(-10.0, -10.0, -10.0, -10.0)
        weights = ComponentWeights()
        assert compute_readiness_score(components, weights) == 0

    def test_no_mock_weights(self) -> None:
        components = ReadinessComponents(
            mastery_component=80.0,
            retention_component=60.0,
            mock_component=0.0,
            coverage_component=50.0,
        )
        weights = redistribute_weights_no_mock()
        # 80*0.525 + 60*0.375 + 0*0.0 + 50*0.10 = 42 + 22.5 + 0 + 5 = 69.5 → 70
        assert compute_readiness_score(components, weights) == 70


# ---------------------------------------------------------------------------
# redistribute_weights_no_mock
# ---------------------------------------------------------------------------


class TestRedistributeWeightsNoMock:
    def test_returns_correct_weights(self) -> None:
        weights = redistribute_weights_no_mock()
        assert weights.mastery == 0.525
        assert weights.retention == 0.375
        assert weights.mock_exam == 0.0
        assert weights.coverage == 0.10

    def test_weights_sum_to_one(self) -> None:
        weights = redistribute_weights_no_mock()
        total = weights.mastery + weights.retention + weights.mock_exam + weights.coverage
        assert abs(total - 1.0) < 1e-10


# ---------------------------------------------------------------------------
# Dataclass structure tests
# ---------------------------------------------------------------------------


class TestDataclasses:
    def test_component_weights_defaults(self) -> None:
        w = ComponentWeights()
        assert w.mastery == 0.40
        assert w.retention == 0.25
        assert w.mock_exam == 0.25
        assert w.coverage == 0.10

    def test_component_weights_frozen(self) -> None:
        w = ComponentWeights()
        try:
            w.mastery = 0.5  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass

    def test_readiness_components_frozen(self) -> None:
        c = ReadinessComponents(50.0, 50.0, 50.0, 50.0)
        try:
            c.mastery_component = 60.0  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass

    def test_readiness_result_structure(self) -> None:
        components = ReadinessComponents(80.0, 60.0, 70.0, 50.0)
        weights = ComponentWeights()
        result = ReadinessResult(score=70, components=components, weights=weights)
        assert result.score == 70
        assert result.components.mastery_component == 80.0
        assert result.weights.mastery == 0.40
