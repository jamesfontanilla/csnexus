"""Predicted score range computation for mock exam analytics.

Uses recency-weighted mock exam scores and FSRS retention data
to project a predicted score range with confidence levels.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass

from app.features.mock_analytics.algorithms.diagnostics import SubtopicDiagnostic


@dataclass(frozen=True)
class PredictedRange:
    """Predicted exam score range with confidence level.

    Attributes:
        lower_bound: Midpoint minus stddev, clamped to 0.
        midpoint: Recency-weighted average of mock scores, adjusted by retention.
        upper_bound: Midpoint plus half stddev, clamped to 100.
        confidence_level: "low" (2-3 exams), "medium" (4-6), "high" (7+).
    """

    lower_bound: float
    midpoint: float
    upper_bound: float
    confidence_level: str  # "low", "medium", "high"


@dataclass(frozen=True)
class ActionableRecommendation:
    """A single actionable recommendation for post-mock improvement.

    Attributes:
        subtopic_id: ID of the subtopic to improve.
        subtopic_name: Human-readable subtopic name.
        current_accuracy: Current accuracy percentage (0-100).
        target_accuracy: Target accuracy percentage (default 80%).
        estimated_point_gain: Estimated exam points gained by reaching target.
        recommended_action: "review", "practice", or "re-learn".
    """

    subtopic_id: int
    subtopic_name: str
    current_accuracy: float
    target_accuracy: float
    estimated_point_gain: float
    recommended_action: str  # "review", "practice", "re-learn"


def compute_predicted_score(
    mock_scores: list[tuple[float, int]],
    avg_retention: float,
) -> PredictedRange | None:
    """Compute predicted score range from mock exam history.

    Uses the same recency weighting as the readiness mock component:
        - days_since <= 14: weight 1.0
        - days_since 15-30: weight 0.7
        - days_since > 30: weight 0.4

    The midpoint is the recency-weighted average, adjusted by avg_retention.
    The range uses the standard deviation of the raw scores.

    Args:
        mock_scores: List of (score_pct, days_since) tuples where score_pct
            is 0-100 and days_since is days since the exam was taken.
        avg_retention: Average FSRS retention across studied flashcards (0.0-1.0).

    Returns:
        PredictedRange with bounds and confidence, or None if < 2 exams.
    """
    if len(mock_scores) < 2:
        return None

    # Compute recency-weighted average
    total_weight = 0.0
    weighted_sum = 0.0

    for score_pct, days_since in mock_scores:
        if days_since <= 14:
            weight = 1.0
        elif days_since <= 30:
            weight = 0.7
        else:
            weight = 0.4

        weighted_sum += score_pct * weight
        total_weight += weight

    if total_weight == 0.0:
        return None

    weighted_avg = weighted_sum / total_weight

    # Adjust by retention: midpoint incorporates retention state
    midpoint = weighted_avg * avg_retention

    # Compute standard deviation of raw scores
    raw_scores = [score for score, _ in mock_scores]
    stddev = statistics.pstdev(raw_scores) if len(raw_scores) >= 2 else 0.0

    # Compute bounds with clamping
    lower_bound = max(0.0, midpoint - stddev)
    upper_bound = min(100.0, midpoint + 0.5 * stddev)

    # Determine confidence level
    exam_count = len(mock_scores)
    if exam_count <= 3:
        confidence_level = "low"
    elif exam_count <= 6:
        confidence_level = "medium"
    else:
        confidence_level = "high"

    return PredictedRange(
        lower_bound=round(lower_bound, 1),
        midpoint=round(midpoint, 1),
        upper_bound=round(upper_bound, 1),
        confidence_level=confidence_level,
    )


def generate_recommendations(
    subtopic_diagnostics: list[SubtopicDiagnostic],
    subtopic_names: dict[int, str],
    questions_per_subtopic_in_exam: dict[int, int],
    mastery_scores: dict[int, float],
    target_accuracy: float = 0.80,
) -> list[ActionableRecommendation]:
    """Generate up to 5 recommendations sorted by estimated point gain.

    Pure function — no database access.

    Args:
        subtopic_diagnostics: Diagnostic breakdowns per subtopic from the exam.
        subtopic_names: Mapping of subtopic_id to human-readable name.
        questions_per_subtopic_in_exam: Number of exam questions per subtopic.
        mastery_scores: Current mastery score (0.0-1.0) per subtopic.
        target_accuracy: Target accuracy threshold (default 0.80 = 80%).

    Returns:
        Up to 5 ActionableRecommendation objects sorted by estimated_point_gain
        descending. Only includes subtopics where current_accuracy < target_accuracy.
    """
    target_pct = target_accuracy * 100.0
    recommendations: list[ActionableRecommendation] = []

    for diag in subtopic_diagnostics:
        current_accuracy_pct = diag.accuracy_percentage

        # Only recommend subtopics below target
        if current_accuracy_pct >= target_pct:
            continue

        subtopic_id = diag.subtopic_id
        questions_in_exam = questions_per_subtopic_in_exam.get(subtopic_id, 0)

        if questions_in_exam <= 0:
            continue

        # estimated_point_gain = questions_in_exam × (target - current) / 100
        estimated_point_gain = (
            questions_in_exam * (target_pct - current_accuracy_pct) / 100.0
        )

        # Determine recommended_action based on mastery level
        mastery = mastery_scores.get(subtopic_id, 0.0)
        recommended_action = _classify_action(mastery)

        subtopic_name = subtopic_names.get(subtopic_id, f"Subtopic {subtopic_id}")

        recommendations.append(
            ActionableRecommendation(
                subtopic_id=subtopic_id,
                subtopic_name=subtopic_name,
                current_accuracy=round(current_accuracy_pct, 1),
                target_accuracy=round(target_pct, 1),
                estimated_point_gain=round(estimated_point_gain, 2),
                recommended_action=recommended_action,
            )
        )

    # Sort by estimated_point_gain descending, take top 5
    recommendations.sort(key=lambda r: r.estimated_point_gain, reverse=True)
    return recommendations[:5]


def _classify_action(mastery: float) -> str:
    """Classify recommended action based on mastery score.

    Args:
        mastery: Current mastery score (0.0-1.0).

    Returns:
        "re-learn" if mastery < 0.4,
        "practice" if 0.4 <= mastery <= 0.7,
        "review" if mastery > 0.7.
    """
    if mastery < 0.4:
        return "re-learn"
    elif mastery <= 0.7:
        return "practice"
    else:
        return "review"
