"""Router-layer tests for the readiness slice.

Uses TestClient with mocked ReadinessService. No DB is hit here.

Endpoints under test:
  GET   /v1/readiness
  GET   /v1/readiness/dashboard
  GET   /v1/readiness/trend
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
from app.features.readiness.router import get_readiness_service, router as readiness_router
from app.features.readiness.schemas import (
    DashboardResponse,
    ReadinessComponentsSchema,
    ReadinessResponse,
    TopImpactSubtopic,
    TrendPoint,
    TrendResponse,
)
from app.features.readiness.service import ReadinessService
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


def _make_components(
    mastery: float = 55.0,
    retention: float = 60.0,
    mock: float = 70.0,
    coverage: float = 50.0,
) -> ReadinessComponentsSchema:
    return ReadinessComponentsSchema(
        mastery_component=mastery,
        retention_component=retention,
        mock_component=mock,
        coverage_component=coverage,
    )


def _make_readiness_response(score: int = 62, delta: int | None = 5) -> ReadinessResponse:
    return ReadinessResponse(
        score=score,
        components=_make_components(),
        delta=delta,
        stale_score=False,
    )


def _make_dashboard_response(score: int = 62) -> DashboardResponse:
    return DashboardResponse(
        score=score,
        components=_make_components(),
        delta=5,
        top_impact_subtopics=[
            TopImpactSubtopic(subtopic_id=1, subtopic_name="Ratios", point_impact=4.5),
            TopImpactSubtopic(subtopic_id=2, subtopic_name="Verb Tenses", point_impact=3.2),
        ],
        readiness_level="Getting There",
        score_change_summary=None,
        stale_data=False,
        computed_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc),
    )


def _make_trend_response(days: int = 5) -> TrendResponse:
    points = [
        TrendPoint(date=f"2025-06-0{i+1}", score=55 + i)
        for i in range(days)
    ]
    return TrendResponse(trend=points)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=ReadinessService)


@pytest.fixture
def authed_user() -> User:
    return _make_user()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(readiness_router)

    fastapi_app.dependency_overrides[get_readiness_service] = lambda: mock_service
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
# GET /v1/readiness
# ---------------------------------------------------------------------------


def test_get_current_readiness_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_current.return_value = _make_readiness_response()

    response = client.get("/v1/readiness")

    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "components" in body
    assert "delta" in body
    assert "stale_score" in body
    mock_service.get_current.assert_called_once_with(1)


def test_get_current_readiness_score_is_integer(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_current.return_value = _make_readiness_response(score=62)

    response = client.get("/v1/readiness")

    assert response.status_code == 200
    assert response.json()["score"] == 62


def test_get_current_readiness_has_component_breakdown(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_current.return_value = _make_readiness_response()

    response = client.get("/v1/readiness")

    assert response.status_code == 200
    components = response.json()["components"]
    assert "mastery_component" in components
    assert "retention_component" in components
    assert "mock_component" in components
    assert "coverage_component" in components


def test_get_current_readiness_null_delta_for_new_user(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_current.return_value = _make_readiness_response(score=0, delta=None)

    response = client.get("/v1/readiness")

    assert response.status_code == 200
    assert response.json()["delta"] is None


def test_get_current_readiness_stale_flag_when_compute_fails(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_current.return_value = ReadinessResponse(
        score=55,
        components=_make_components(),
        delta=None,
        stale_score=True,
    )

    response = client.get("/v1/readiness")

    assert response.status_code == 200
    assert response.json()["stale_score"] is True


def test_get_current_readiness_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.get("/v1/readiness")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/readiness/dashboard
# ---------------------------------------------------------------------------


def test_get_dashboard_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_dashboard.return_value = _make_dashboard_response()

    response = client.get("/v1/readiness/dashboard")

    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "readiness_level" in body
    assert "top_impact_subtopics" in body
    assert "components" in body
    mock_service.get_dashboard.assert_called_once_with(1)


def test_get_dashboard_readiness_level_present(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_dashboard.return_value = _make_dashboard_response(score=62)

    response = client.get("/v1/readiness/dashboard")

    assert response.status_code == 200
    level = response.json()["readiness_level"]
    assert level in ("Not Ready", "Getting There", "Almost Ready", "Exam Ready")


def test_get_dashboard_top_impact_subtopics_shape(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_dashboard.return_value = _make_dashboard_response()

    response = client.get("/v1/readiness/dashboard")

    assert response.status_code == 200
    subtopics = response.json()["top_impact_subtopics"]
    assert isinstance(subtopics, list)
    assert len(subtopics) <= 3
    if subtopics:
        first = subtopics[0]
        assert "subtopic_id" in first
        assert "subtopic_name" in first
        assert "point_impact" in first


def test_get_dashboard_empty_impact_subtopics_for_new_user(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_dashboard.return_value = DashboardResponse(
        score=0,
        components=_make_components(0, 0, 0, 0),
        delta=None,
        top_impact_subtopics=[],
        readiness_level="Not Ready",
        score_change_summary=None,
        stale_data=False,
        computed_at=None,
    )

    response = client.get("/v1/readiness/dashboard")

    assert response.status_code == 200
    assert response.json()["top_impact_subtopics"] == []
    assert response.json()["readiness_level"] == "Not Ready"


def test_get_dashboard_stale_data_flag(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_dashboard.return_value = DashboardResponse(
        score=50,
        components=_make_components(),
        delta=None,
        top_impact_subtopics=[],
        readiness_level="Getting There",
        score_change_summary=None,
        stale_data=True,
        computed_at=datetime(2025, 5, 28, 10, 0, tzinfo=timezone.utc),
    )

    response = client.get("/v1/readiness/dashboard")

    assert response.status_code == 200
    assert response.json()["stale_data"] is True


def test_get_dashboard_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.get("/v1/readiness/dashboard")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/readiness/trend
# ---------------------------------------------------------------------------


def test_get_trend_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_trend.return_value = _make_trend_response(days=5).trend

    response = client.get("/v1/readiness/trend")

    assert response.status_code == 200
    body = response.json()
    assert "trend" in body
    assert isinstance(body["trend"], list)
    mock_service.get_trend.assert_called_once_with(1, days=30)


def test_get_trend_points_have_date_and_score(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_trend.return_value = _make_trend_response(days=3).trend

    response = client.get("/v1/readiness/trend")

    assert response.status_code == 200
    points = response.json()["trend"]
    assert len(points) == 3
    for point in points:
        assert "date" in point
        assert "score" in point
        assert 0 <= point["score"] <= 100


def test_get_trend_empty_for_new_user(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_trend.return_value = []

    response = client.get("/v1/readiness/trend")

    assert response.status_code == 200
    assert response.json()["trend"] == []


def test_get_trend_thirty_day_carry_forward(
    client: TestClient, mock_service: MagicMock
) -> None:
    """Service should be called with days=30 for carry-forward trend."""
    mock_service.get_trend.return_value = [
        TrendPoint(date=f"2025-05-{i+5:02d}", score=60) for i in range(30)
    ]

    response = client.get("/v1/readiness/trend")

    assert response.status_code == 200
    assert len(response.json()["trend"]) == 30
    mock_service.get_trend.assert_called_once_with(1, days=30)


def test_get_trend_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.get("/v1/readiness/trend")
    assert response.status_code == 401
