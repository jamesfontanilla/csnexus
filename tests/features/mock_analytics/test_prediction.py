"""Unit tests for mock analytics prediction module.

Tests compute_predicted_score and generate_recommendations pure functions.
"""

import pytest

from app.features.mock_analytics.algorithms.diagnostics import SubtopicDiagnostic
from app.features.mock_analytics.algorithms.prediction import (
    ActionableRecommendation,
    PredictedRange,
    compute_predicted_score,
    generate_recommendations,
)


# --- compute_predicted_score tests ---


class TestComputePredictedScore:
    """Tests for compute_predicted_score."""

    def test_returns_none_for_fewer_than_2_exams(self) -> None:
        result = compute_predicted_score([], avg_retention=0.9)
        assert result is None

        result = compute_predicted_score([(75.0, 5)], avg_retention=0.9)
        assert result is None

    def test_returns_predicted_range_for_2_exams(self) -> None:
        scores = [(70.0, 5), (80.0, 10)]
        result = compute_predicted_score(scores, avg_retention=1.0)

        assert result is not None
        assert isinstance(result, PredictedRange)
        # Both within 14 days -> weight 1.0 each
        # Weighted avg = (70*1 + 80*1) / (1+1) = 75
        # retention=1.0 -> midpoint = 75 * 1.0 = 75
        assert result.midpoint == 75.0

    def test_recency_weighting_recent(self) -> None:
        # All exams within 14 days, weight = 1.0
        scores = [(60.0, 1), (80.0, 10)]
        result = compute_predicted_score(scores, avg_retention=1.0)

        assert result is not None
        # (60*1 + 80*1) / 2 = 70, adjusted by retention 1.0 = 70
        assert result.midpoint == 70.0

    def test_recency_weighting_mixed(self) -> None:
        # 80% at 5 days (weight 1.0), 60% at 20 days (weight 0.7)
        scores = [(80.0, 5), (60.0, 20)]
        result = compute_predicted_score(scores, avg_retention=1.0)

        assert result is not None
        # (80*1.0 + 60*0.7) / (1.0 + 0.7) = (80 + 42) / 1.7 = 71.76...
        expected_midpoint = (80.0 * 1.0 + 60.0 * 0.7) / (1.0 + 0.7)
        assert result.midpoint == pytest.approx(expected_midpoint, rel=1e-1)

    def test_recency_weighting_old(self) -> None:
        # Exam > 30 days old, weight 0.4
        scores = [(90.0, 5), (50.0, 45)]
        result = compute_predicted_score(scores, avg_retention=1.0)

        assert result is not None
        expected = (90.0 * 1.0 + 50.0 * 0.4) / (1.0 + 0.4)
        assert result.midpoint == pytest.approx(expected, rel=1e-1)

    def test_retention_adjustment(self) -> None:
        scores = [(80.0, 5), (80.0, 10)]
        result = compute_predicted_score(scores, avg_retention=0.8)

        assert result is not None
        # Weighted avg = 80, adjusted by 0.8 -> midpoint = 64
        assert result.midpoint == 64.0

    def test_bounds_clamping_lower(self) -> None:
        # Very low scores with high stddev -> lower bound clamped to 0
        scores = [(5.0, 5), (15.0, 10)]
        result = compute_predicted_score(scores, avg_retention=0.5)

        assert result is not None
        assert result.lower_bound >= 0.0

    def test_bounds_clamping_upper(self) -> None:
        # Very high scores -> upper bound clamped to 100
        scores = [(95.0, 5), (99.0, 10)]
        result = compute_predicted_score(scores, avg_retention=1.0)

        assert result is not None
        assert result.upper_bound <= 100.0

    def test_confidence_low_2_exams(self) -> None:
        scores = [(70.0, 5), (80.0, 10)]
        result = compute_predicted_score(scores, avg_retention=0.9)

        assert result is not None
        assert result.confidence_level == "low"

    def test_confidence_low_3_exams(self) -> None:
        scores = [(70.0, 5), (80.0, 10), (75.0, 12)]
        result = compute_predicted_score(scores, avg_retention=0.9)

        assert result is not None
        assert result.confidence_level == "low"

    def test_confidence_medium_4_exams(self) -> None:
        scores = [(70.0, 5), (80.0, 10), (75.0, 12), (72.0, 14)]
        result = compute_predicted_score(scores, avg_retention=0.9)

        assert result is not None
        assert result.confidence_level == "medium"

    def test_confidence_medium_6_exams(self) -> None:
        scores = [(i * 10.0 + 40, i * 3) for i in range(6)]
        result = compute_predicted_score(scores, avg_retention=0.9)

        assert result is not None
        assert result.confidence_level == "medium"

    def test_confidence_high_7_exams(self) -> None:
        scores = [(70.0 + i, i * 5) for i in range(7)]
        result = compute_predicted_score(scores, avg_retention=0.9)

        assert result is not None
        assert result.confidence_level == "high"

    def test_stddev_affects_bounds(self) -> None:
        # Same average but different spread
        uniform_scores = [(75.0, 5), (75.0, 10)]
        result_uniform = compute_predicted_score(uniform_scores, avg_retention=1.0)

        varied_scores = [(60.0, 5), (90.0, 10)]
        result_varied = compute_predicted_score(varied_scores, avg_retention=1.0)

        assert result_uniform is not None
        assert result_varied is not None
        # Uniform: stddev=0, so bounds collapse toward midpoint
        assert result_uniform.lower_bound == result_uniform.midpoint
        # Varied: stddev=15, so bounds spread
        assert result_varied.lower_bound < result_varied.midpoint


# --- generate_recommendations tests ---


def _make_diagnostic(
    subtopic_id: int = 1,
    questions_attempted: int = 10,
    questions_correct: int = 5,
    accuracy_percentage: float = 50.0,
) -> SubtopicDiagnostic:
    """Helper factory for SubtopicDiagnostic."""
    return SubtopicDiagnostic(
        subtopic_id=subtopic_id,
        questions_attempted=questions_attempted,
        questions_correct=questions_correct,
        points_lost=questions_attempted - questions_correct,
        avg_seconds_per_question=30.0,
        accuracy_percentage=accuracy_percentage,
    )


class TestGenerateRecommendations:
    """Tests for generate_recommendations."""

    def test_empty_diagnostics_returns_empty(self) -> None:
        result = generate_recommendations(
            subtopic_diagnostics=[],
            subtopic_names={},
            questions_per_subtopic_in_exam={},
            mastery_scores={},
        )
        assert result == []

    def test_excludes_subtopics_above_target(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=85.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Vocabulary"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.85},
        )
        assert result == []

    def test_includes_subtopics_below_target(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Vocabulary"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.5},
        )
        assert len(result) == 1
        assert result[0].subtopic_id == 1
        assert result[0].subtopic_name == "Vocabulary"

    def test_estimated_point_gain_formula(self) -> None:
        # gain = questions_in_exam * (target_pct - current_pct) / 100
        # = 10 * (80 - 50) / 100 = 3.0
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Vocabulary"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.5},
        )
        assert len(result) == 1
        assert result[0].estimated_point_gain == 3.0

    def test_sorted_by_estimated_point_gain_descending(self) -> None:
        diags = [
            _make_diagnostic(subtopic_id=1, accuracy_percentage=70.0),
            _make_diagnostic(subtopic_id=2, accuracy_percentage=40.0),
            _make_diagnostic(subtopic_id=3, accuracy_percentage=60.0),
        ]
        result = generate_recommendations(
            subtopic_diagnostics=diags,
            subtopic_names={1: "A", 2: "B", 3: "C"},
            questions_per_subtopic_in_exam={1: 10, 2: 10, 3: 10},
            mastery_scores={1: 0.7, 2: 0.3, 3: 0.5},
        )
        # Point gains: id=1: 10*(80-70)/100=1.0, id=2: 10*(80-40)/100=4.0, id=3: 10*(80-60)/100=2.0
        assert len(result) == 3
        assert result[0].subtopic_id == 2
        assert result[1].subtopic_id == 3
        assert result[2].subtopic_id == 1

    def test_limits_to_5_recommendations(self) -> None:
        diags = [
            _make_diagnostic(subtopic_id=i, accuracy_percentage=50.0)
            for i in range(10)
        ]
        result = generate_recommendations(
            subtopic_diagnostics=diags,
            subtopic_names={i: f"Topic {i}" for i in range(10)},
            questions_per_subtopic_in_exam={i: 5 for i in range(10)},
            mastery_scores={i: 0.5 for i in range(10)},
        )
        assert len(result) == 5

    def test_action_classification_relearn(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=30.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.2},
        )
        assert result[0].recommended_action == "re-learn"

    def test_action_classification_practice(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.5},
        )
        assert result[0].recommended_action == "practice"

    def test_action_classification_review(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=60.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.75},
        )
        assert result[0].recommended_action == "review"

    def test_action_boundary_04_is_practice(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.4},
        )
        assert result[0].recommended_action == "practice"

    def test_action_boundary_07_is_practice(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.7},
        )
        assert result[0].recommended_action == "practice"

    def test_target_accuracy_default_80(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=79.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={1: 0.79},
        )
        assert len(result) == 1
        assert result[0].target_accuracy == 80.0

    def test_skips_subtopics_with_zero_questions(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 0},
            mastery_scores={1: 0.5},
        )
        assert result == []

    def test_missing_subtopic_name_uses_fallback(self) -> None:
        diag = _make_diagnostic(subtopic_id=99, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={},
            questions_per_subtopic_in_exam={99: 10},
            mastery_scores={99: 0.5},
        )
        assert len(result) == 1
        assert result[0].subtopic_name == "Subtopic 99"

    def test_missing_mastery_defaults_to_zero(self) -> None:
        diag = _make_diagnostic(subtopic_id=1, accuracy_percentage=50.0)
        result = generate_recommendations(
            subtopic_diagnostics=[diag],
            subtopic_names={1: "Math"},
            questions_per_subtopic_in_exam={1: 10},
            mastery_scores={},  # no mastery entry
        )
        assert len(result) == 1
        assert result[0].recommended_action == "re-learn"
