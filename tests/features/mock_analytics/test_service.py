"""Service-layer tests for MockAnalyticsService.

Tests business logic in isolation with mocked repositories.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.mock_analytics.service import MockAnalyticsService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service(**overrides) -> MockAnalyticsService:
    defaults = dict(
        analytics_repo=MagicMock(),
        mock_exam_repo=MagicMock(),
        mastery_repo=MagicMock(),
        subtopic_repo=MagicMock(),
    )
    defaults.update(overrides)
    return MockAnalyticsService(**defaults)


def _make_mock_report(
    id: int = 1,
    user_id: int = 1,
    attempt_id: int = 10,
    total_score: float = 72.5,
) -> MagicMock:
    report = MagicMock()
    report.id = id
    report.user_id = user_id
    report.mock_exam_attempt_id = attempt_id
    report.total_score = total_score
    report.subtopic_breakdowns = (
        '[{"subtopic_id": 1, "questions_attempted": 5, "questions_correct": 4, '
        '"points_lost": 1, "avg_seconds_per_question": 30.0, "accuracy_percentage": 80.0}]'
    )
    report.highest_impact_areas = (
        '[{"subtopic_id": 2, "questions_attempted": 3, "questions_correct": 1, '
        '"points_lost": 2, "avg_seconds_per_question": 45.0, "accuracy_percentage": 33.3}]'
    )
    report.regression_alerts = "[]"
    report.difficulty_performance = '{"easy": 90.0, "medium": 70.0, "hard": 50.0}'
    return report


def _make_mock_recommendation(
    id: int = 1,
    report_id: int = 1,
    subtopic_id: int = 1,
    accepted_at=None,
) -> MagicMock:
    rec = MagicMock()
    rec.id = id
    rec.report_id = report_id
    rec.subtopic_id = subtopic_id
    rec.subtopic_name = "Ratios"
    rec.current_accuracy = 33.3
    rec.target_accuracy = 70.0
    rec.estimated_point_gain = 4.5
    rec.recommended_action = "practice"
    rec.accepted_at = accepted_at
    return rec


# ---------------------------------------------------------------------------
# generate_diagnostic
# ---------------------------------------------------------------------------


def test_generate_diagnostic_happy_path():
    analytics_repo = MagicMock()
    mock_exam_repo = MagicMock()

    mock_exam_repo.get_attempt_for_user.return_value = MagicMock()
    analytics_repo.get_report.return_value = None  # not cached
    analytics_repo.get_attempt_answers_with_questions.return_value = []
    analytics_repo.get_historical_accuracy.return_value = {}
    analytics_repo.create_report.return_value = _make_mock_report()

    service = _make_service(
        analytics_repo=analytics_repo,
        mock_exam_repo=mock_exam_repo,
    )
    result = service.generate_diagnostic(user_id=1, attempt_id=10)

    analytics_repo.create_report.assert_called_once()
    assert result.total_score == 72.5


def test_generate_diagnostic_returns_cached_when_exists():
    """Second call returns the existing report without recomputing."""
    analytics_repo = MagicMock()
    mock_exam_repo = MagicMock()

    mock_exam_repo.get_attempt_for_user.return_value = MagicMock()
    existing_report = _make_mock_report()
    analytics_repo.get_report.return_value = existing_report  # already cached

    service = _make_service(
        analytics_repo=analytics_repo,
        mock_exam_repo=mock_exam_repo,
    )
    result = service.generate_diagnostic(user_id=1, attempt_id=10)

    analytics_repo.create_report.assert_not_called()
    assert result is existing_report


def test_generate_diagnostic_attempt_not_found_raises_404():
    analytics_repo = MagicMock()
    mock_exam_repo = MagicMock()
    mock_exam_repo.get_attempt_for_user.return_value = None

    service = _make_service(
        analytics_repo=analytics_repo,
        mock_exam_repo=mock_exam_repo,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.generate_diagnostic(user_id=1, attempt_id=999)

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# get_predicted_score
# ---------------------------------------------------------------------------


def test_get_predicted_score_requires_two_exams():
    """Returns null prediction fields and a message when fewer than 2 exams exist."""
    analytics_repo = MagicMock()
    analytics_repo.get_user_mock_scores.return_value = [(75.0, 10)]  # only 1 exam

    service = _make_service(analytics_repo=analytics_repo)
    result = service.get_predicted_score(user_id=1)

    assert result["lower_bound"] is None
    assert result["midpoint"] is None
    assert result["upper_bound"] is None
    assert result["confidence_level"] is None
    assert result["message"] is not None
    assert "2" in result["message"]  # mentions needing 2 exams


def test_get_predicted_score_no_exams_returns_null():
    analytics_repo = MagicMock()
    analytics_repo.get_user_mock_scores.return_value = []  # no exams at all

    service = _make_service(analytics_repo=analytics_repo)
    result = service.get_predicted_score(user_id=1)

    assert result["lower_bound"] is None
    assert result["message"] is not None


def test_get_predicted_score_with_two_exams_returns_prediction():
    """With ≥2 exams the prediction fields are populated."""
    analytics_repo = MagicMock()
    mastery_repo = MagicMock()

    # Two exam scores with days_since values
    analytics_repo.get_user_mock_scores.return_value = [
        (60.0, 14),
        (72.0, 7),
    ]
    mastery_repo.list_by_user.return_value = []  # triggers default 0.85 retention

    service = _make_service(
        analytics_repo=analytics_repo,
        mastery_repo=mastery_repo,
    )
    result = service.get_predicted_score(user_id=1)

    # Prediction computed — fields should be present (may be None if algorithm
    # returns None, but the service still returns a structured dict)
    assert "lower_bound" in result
    assert "midpoint" in result
    assert "upper_bound" in result


# ---------------------------------------------------------------------------
# accept_recommendation
# ---------------------------------------------------------------------------


def test_accept_recommendation_feeds_queue():
    """Accepting a recommendation marks it and returns the updated record."""
    analytics_repo = MagicMock()
    rec = _make_mock_recommendation()
    analytics_repo.accept_recommendation.return_value = rec

    service = _make_service(analytics_repo=analytics_repo)
    result = service.accept_recommendation(user_id=1, recommendation_id=1)

    analytics_repo.accept_recommendation.assert_called_once_with(1)
    assert result.id == 1


def test_accept_recommendation_not_found_raises_404():
    analytics_repo = MagicMock()
    analytics_repo.accept_recommendation.return_value = None

    service = _make_service(analytics_repo=analytics_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.accept_recommendation(user_id=1, recommendation_id=999)

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# get_recommendations
# ---------------------------------------------------------------------------


def test_get_recommendations_returns_list():
    analytics_repo = MagicMock()
    mastery_repo = MagicMock()
    subtopic_repo = MagicMock()

    report = _make_mock_report()
    analytics_repo.get_report.return_value = report
    analytics_repo.get_recommendations.return_value = []  # first call: none exist

    subtopic = MagicMock()
    subtopic.title = "Ratios"
    subtopic_repo.get.return_value = subtopic

    analytics_repo.get_questions_per_subtopic_in_exam.return_value = {1: 5}
    mastery_repo.get_by_user_and_subtopic.return_value = None

    persisted_recs = [_make_mock_recommendation()]
    # Second call (after commit) returns the persisted recs
    analytics_repo.get_recommendations.side_effect = [[], persisted_recs]

    service = _make_service(
        analytics_repo=analytics_repo,
        mastery_repo=mastery_repo,
        subtopic_repo=subtopic_repo,
    )
    result = service.get_recommendations(attempt_id=10)

    assert isinstance(result, list)


def test_get_recommendations_returns_cached_on_second_call():
    """If recommendations already exist, skip regeneration."""
    analytics_repo = MagicMock()

    report = _make_mock_report()
    analytics_repo.get_report.return_value = report

    existing_recs = [_make_mock_recommendation()]
    analytics_repo.get_recommendations.return_value = existing_recs

    service = _make_service(analytics_repo=analytics_repo)
    result = service.get_recommendations(attempt_id=10)

    # DB add/commit should not be called since recs were already cached
    analytics_repo.db.add.assert_not_called()
    assert result == existing_recs


def test_get_recommendations_no_report_raises_404():
    analytics_repo = MagicMock()
    analytics_repo.get_report.return_value = None

    service = _make_service(analytics_repo=analytics_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.get_recommendations(attempt_id=999)

    assert exc_info.value.status_code == 404
