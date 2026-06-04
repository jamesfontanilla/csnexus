"""Router-layer tests for the mock analytics slice.

Uses TestClient with mocked MockAnalyticsService. No DB is hit here.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from app.common.deps import get_current_user
from app.common.middlewares.auth import AuthMiddleware
from app.common.middlewares.error_handler import register_exception_handlers
from app.common.middlewares.logging import RequestLoggingMiddleware
from app.features.mock_analytics.router import (
    get_mock_analytics_service,
    router as analytics_router,
)
from app.features.mock_analytics.service import MockAnalyticsService
from app.features.users.models import AccountState, Category, Role, User


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def _make_user(**overrides: object) -> User:
    defaults: dict[str, object] = {
        "id": 1,
        "email": "alice@cse.local",
        "display_name": "Alice",
        "age": 25,
        "category": Category.PROFESSIONAL.value,
        "role": Role.LEARNER.value,
        "account_state": AccountState.VERIFIED.value,
        "is_banned": False,
        "tz_name": "UTC",
        "password_hash": "x",
        "cross_category_preview": False,
    }
    return User(**{**defaults, **overrides})


def _make_mock_report_model(
    id: int = 1,
    user_id: int = 1,
    attempt_id: int = 10,
    total_score: float = 72.5,
) -> MagicMock:
    """Build a mock ORM DiagnosticReport object."""
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
    subtopic_id: int = 1,
    accepted_at=None,
) -> MagicMock:
    rec = MagicMock()
    rec.id = id
    rec.subtopic_id = subtopic_id
    rec.subtopic_name = "Ratios"
    rec.current_accuracy = 33.3
    rec.target_accuracy = 70.0
    rec.estimated_point_gain = 4.5
    rec.recommended_action = "practice"
    rec.accepted_at = accepted_at
    return rec


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=MockAnalyticsService)


@pytest.fixture
def authed_user() -> User:
    return _make_user()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(analytics_router)

    fastapi_app.dependency_overrides[get_mock_analytics_service] = lambda: mock_service
    fastapi_app.dependency_overrides[get_current_user] = lambda: authed_user

    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def _raise_401() -> None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_credentials")


@pytest.fixture
def unauthenticated_client(app: FastAPI) -> TestClient:
    app.dependency_overrides[get_current_user] = _raise_401
    return TestClient(app)


# ---------------------------------------------------------------------------
# GET /v1/mock-analytics/{attempt_id}
# ---------------------------------------------------------------------------


def test_get_diagnostic_returns_200(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_diagnostic.return_value = _make_mock_report_model()

    response = client.get("/v1/mock-analytics/10")

    assert response.status_code == 200
    body = response.json()
    assert "total_score" in body
    assert body["total_score"] == 72.5
    assert "subtopic_breakdowns" in body
    assert "highest_impact_areas" in body
    assert "regression_alerts" in body
    assert "difficulty_performance" in body
    mock_service.get_diagnostic.assert_called_once_with(10)


def test_get_diagnostic_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_diagnostic.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Diagnostic report not found for this attempt",
    )

    response = client.get("/v1/mock-analytics/999")

    assert response.status_code == 404


def test_get_diagnostic_422_for_non_int_id(client: TestClient) -> None:
    response = client.get("/v1/mock-analytics/abc")
    assert response.status_code == 422


def test_get_diagnostic_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/mock-analytics/10")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/mock-analytics/{attempt_id}/recommendations
# ---------------------------------------------------------------------------


def test_get_recommendations_returns_list(
    client: TestClient, mock_service: MagicMock
) -> None:
    recs = [_make_mock_recommendation(id=1), _make_mock_recommendation(id=2)]
    mock_service.get_recommendations.return_value = recs

    response = client.get("/v1/mock-analytics/10/recommendations")

    assert response.status_code == 200
    body = response.json()
    assert "recommendations" in body
    assert len(body["recommendations"]) == 2
    # Each recommendation has expected fields
    first = body["recommendations"][0]
    assert "subtopic_name" in first
    assert "estimated_point_gain" in first
    assert "recommended_action" in first
    assert "formatted_string" in first


def test_get_recommendations_empty_list(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_recommendations.return_value = []

    response = client.get("/v1/mock-analytics/10/recommendations")

    assert response.status_code == 200
    assert response.json()["recommendations"] == []


def test_get_recommendations_no_report_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_recommendations.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Diagnostic report not found for this attempt",
    )

    response = client.get("/v1/mock-analytics/999/recommendations")

    assert response.status_code == 404


def test_get_recommendations_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/mock-analytics/10/recommendations")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/mock-analytics/{attempt_id}/recommendations/:accept
# ---------------------------------------------------------------------------


def test_accept_recommendation_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    unaccepted = _make_mock_recommendation(accepted_at=None)
    accepted = _make_mock_recommendation(
        accepted_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc)
    )
    mock_service.get_recommendations.return_value = [unaccepted]
    mock_service.accept_recommendation.return_value = accepted

    response = client.post("/v1/mock-analytics/10/recommendations/:accept")

    assert response.status_code == 200
    body = response.json()
    assert body["accepted_at"] is not None
    mock_service.accept_recommendation.assert_called_once_with(1, unaccepted.id)


def test_accept_recommendation_no_unaccepted_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    """If all recommendations are already accepted, the endpoint returns 404."""
    already_accepted = _make_mock_recommendation(
        accepted_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc)
    )
    mock_service.get_recommendations.return_value = [already_accepted]

    response = client.post("/v1/mock-analytics/10/recommendations/:accept")

    assert response.status_code == 404


def test_accept_recommendation_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.post(
        "/v1/mock-analytics/10/recommendations/:accept"
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/mock-analytics/prediction
# ---------------------------------------------------------------------------


def test_get_prediction_returns_200(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_predicted_score.return_value = {
        "lower_bound": 68.0,
        "midpoint": 75.0,
        "upper_bound": 82.0,
        "confidence_level": "medium",
        "message": None,
    }

    response = client.get("/v1/mock-analytics/prediction")

    assert response.status_code == 200
    body = response.json()
    assert body["midpoint"] == 75.0
    assert body["confidence_level"] == "medium"
    assert body["message"] is None
    mock_service.get_predicted_score.assert_called_once_with(1)


def test_get_prediction_insufficient_data_returns_null_fields(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_predicted_score.return_value = {
        "lower_bound": None,
        "midpoint": None,
        "upper_bound": None,
        "confidence_level": None,
        "message": "At least 2 completed mock exams are needed for score prediction.",
    }

    response = client.get("/v1/mock-analytics/prediction")

    assert response.status_code == 200
    body = response.json()
    assert body["midpoint"] is None
    assert body["message"] is not None


def test_get_prediction_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/mock-analytics/prediction")
    assert response.status_code == 401
