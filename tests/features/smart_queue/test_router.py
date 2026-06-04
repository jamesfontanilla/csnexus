"""Router-layer tests for the smart queue slice.

Uses TestClient with mocked QueueService. No DB is hit here.
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
from app.features.smart_queue.router import get_queue_service, router as queue_router
from app.features.smart_queue.schemas import (
    QueueItemSchema,
    QueuePreferencesResponse,
    QueueResponse,
)
from app.features.smart_queue.service import QueueService
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


def _make_queue_item(id: int = 1, item_type: str = "new_content") -> QueueItemSchema:
    return QueueItemSchema(
        id=id,
        position=0,
        item_type=item_type,
        payload={"subtopic_id": 1, "lesson_id": 1, "section_index": 0},
        estimated_seconds=300,
        completed_at=None,
    )


def _make_queue_response(items: list[QueueItemSchema] | None = None) -> QueueResponse:
    items = items or [_make_queue_item()]
    return QueueResponse(
        items=items,
        total_estimated_seconds=300,
        items_remaining=len(items),
        items_completed=0,
        time_budget_minutes=30,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=QueueService)


@pytest.fixture
def authed_user() -> User:
    return _make_user()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(queue_router)

    fastapi_app.dependency_overrides[get_queue_service] = lambda: mock_service
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
# GET /v1/queue
# ---------------------------------------------------------------------------


def test_get_daily_queue_returns_200(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_daily_queue.return_value = _make_queue_response()

    response = client.get("/v1/queue")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert body["time_budget_minutes"] == 30
    assert body["items_remaining"] >= 0
    mock_service.get_daily_queue.assert_called_once_with(1)


def test_get_daily_queue_returns_empty_items_when_all_done(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_daily_queue.return_value = QueueResponse(
        items=[],
        total_estimated_seconds=0,
        items_remaining=0,
        items_completed=3,
        time_budget_minutes=30,
    )

    response = client.get("/v1/queue")

    assert response.status_code == 200
    assert response.json()["items_completed"] == 3
    assert response.json()["items_remaining"] == 0


def test_get_daily_queue_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/queue")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/queue/items/{id}/:complete
# ---------------------------------------------------------------------------


def test_complete_item_returns_updated_queue(
    client: TestClient, mock_service: MagicMock
) -> None:
    completed_item = QueueItemSchema(
        id=1,
        position=0,
        item_type="new_content",
        payload={"subtopic_id": 1, "lesson_id": 1, "section_index": 0},
        estimated_seconds=300,
        completed_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc),
    )
    mock_service.complete_item.return_value = QueueResponse(
        items=[completed_item],
        total_estimated_seconds=300,
        items_remaining=0,
        items_completed=1,
        time_budget_minutes=30,
    )

    response = client.post("/v1/queue/items/1/:complete")

    assert response.status_code == 200
    body = response.json()
    assert body["items_completed"] == 1
    assert body["items_remaining"] == 0
    mock_service.complete_item.assert_called_once_with(1, 1)


def test_complete_item_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.complete_item.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Queue item not found"
    )

    response = client.post("/v1/queue/items/999/:complete")

    assert response.status_code == 404


def test_complete_item_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.post("/v1/queue/items/1/:complete")
    assert response.status_code == 401


def test_complete_item_422_for_non_int_id(client: TestClient) -> None:
    response = client.post("/v1/queue/items/abc/:complete")
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /v1/queue/:regenerate
# ---------------------------------------------------------------------------


def test_regenerate_queue_returns_new_queue(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.regenerate_queue.return_value = _make_queue_response(
        items=[
            _make_queue_item(id=10, item_type="quiz_practice"),
            _make_queue_item(id=11, item_type="new_content"),
        ]
    )

    response = client.post("/v1/queue/:regenerate")

    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 2
    mock_service.regenerate_queue.assert_called_once_with(1)


def test_regenerate_queue_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.post("/v1/queue/:regenerate")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/queue/preferences
# ---------------------------------------------------------------------------


def test_get_preferences_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_preferences.return_value = QueuePreferencesResponse(
        time_budget_minutes=60
    )

    response = client.get("/v1/queue/preferences")

    assert response.status_code == 200
    assert response.json()["time_budget_minutes"] == 60
    mock_service.get_preferences.assert_called_once_with(1)


def test_get_preferences_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/queue/preferences")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# PATCH /v1/queue/preferences
# ---------------------------------------------------------------------------


def test_update_preferences_valid_budget_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.update_preferences.return_value = QueuePreferencesResponse(
        time_budget_minutes=15
    )

    response = client.patch(
        "/v1/queue/preferences", json={"time_budget_minutes": 15}
    )

    assert response.status_code == 200
    assert response.json()["time_budget_minutes"] == 15
    mock_service.update_preferences.assert_called_once_with(1, 15)


def test_update_preferences_invalid_budget_returns_422(client: TestClient) -> None:
    """time_budget_minutes must be 15, 30, or 60 — anything else is 422."""
    response = client.patch(
        "/v1/queue/preferences", json={"time_budget_minutes": 45}
    )
    assert response.status_code == 422


def test_update_preferences_missing_field_returns_422(client: TestClient) -> None:
    response = client.patch("/v1/queue/preferences", json={})
    assert response.status_code == 422


def test_update_preferences_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.patch(
        "/v1/queue/preferences", json={"time_budget_minutes": 30}
    )
    assert response.status_code == 401
