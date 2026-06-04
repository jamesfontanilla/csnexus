"""Router-layer tests for the pretesting slice.

Uses TestClient with mocked PretestService. No DB is hit here.

Endpoints under test:
  POST  /v1/pretests/{subtopic_id}/start
  POST  /v1/pretests/{pretest_id}/submit
  GET   /v1/pretests/{subtopic_id}/comparison
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from app.common.deps import get_current_user
from app.common.middlewares.auth import AuthMiddleware
from app.common.middlewares.error_handler import register_exception_handlers
from app.common.middlewares.logging import RequestLoggingMiddleware
from app.features.pretesting.router import get_pretest_service, router as pretest_router
from app.features.pretesting.schemas import (
    PretestComparisonResponse,
    PretestQuestion,
    PretestStartResponse,
    PretestSubmitResponse,
)
from app.features.pretesting.service import PretestService
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


def _make_pretest_question(id: int = 1) -> PretestQuestion:
    return PretestQuestion(
        id=id,
        stem="What is the ratio of 4 to 8?",
        options=["1:2", "2:1", "4:8", "1:4"],
        key_concept="types of ratios",
    )


def _make_start_response(subtopic_id: int = 1, pretest_id: int = 10) -> PretestStartResponse:
    return PretestStartResponse(
        pretest_id=pretest_id,
        subtopic_id=subtopic_id,
        questions=[_make_pretest_question(1), _make_pretest_question(2)],
    )


def _make_submit_response(pretest_id: int = 10) -> PretestSubmitResponse:
    return PretestSubmitResponse(
        pretest_id=pretest_id,
        score=50.0,
        total_questions=2,
        correct_count=1,
        weak_concepts=["types of ratios"],
    )


def _make_comparison_response(subtopic_id: int = 1) -> PretestComparisonResponse:
    return PretestComparisonResponse(
        subtopic_id=subtopic_id,
        pretest_score=50.0,
        post_lesson_score=80.0,
        improvement=30.0,
        message="Great progress! You improved by 30.0 percentage points after the lesson.",
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=PretestService)


@pytest.fixture
def authed_user() -> User:
    return _make_user()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(pretest_router)

    fastapi_app.dependency_overrides[get_pretest_service] = lambda: mock_service
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
# POST /v1/pretests/{subtopic_id}/start
# ---------------------------------------------------------------------------


def test_start_pretest_returns_201(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.start_pretest.return_value = _make_start_response()

    response = client.post("/v1/pretests/1/start")

    assert response.status_code == 201
    body = response.json()
    assert "pretest_id" in body
    assert "questions" in body
    assert len(body["questions"]) == 2
    mock_service.start_pretest.assert_called_once_with(1, 1)


def test_start_pretest_questions_have_required_fields(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.start_pretest.return_value = _make_start_response()

    response = client.post("/v1/pretests/1/start")

    assert response.status_code == 201
    first_q = response.json()["questions"][0]
    assert "id" in first_q
    assert "stem" in first_q
    assert "options" in first_q
    assert "key_concept" in first_q


def test_start_pretest_subtopic_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.start_pretest.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Subtopic not found"
    )

    response = client.post("/v1/pretests/999/start")

    assert response.status_code == 404


def test_start_pretest_lesson_already_completed_returns_409(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.start_pretest.side_effect = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Lesson already completed — pretest not applicable",
    )

    response = client.post("/v1/pretests/1/start")

    assert response.status_code == 409


def test_start_pretest_insufficient_questions_returns_422(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.start_pretest.side_effect = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Insufficient questions for pretest",
    )

    response = client.post("/v1/pretests/1/start")

    assert response.status_code == 422


def test_start_pretest_invalid_subtopic_id_returns_422(client: TestClient) -> None:
    response = client.post("/v1/pretests/abc/start")
    assert response.status_code == 422


def test_start_pretest_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.post("/v1/pretests/1/start")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/pretests/{pretest_id}/submit
# ---------------------------------------------------------------------------


def test_submit_pretest_returns_200(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.submit_pretest.return_value = _make_submit_response()

    response = client.post(
        "/v1/pretests/10/submit",
        json={
            "answers": [
                {"question_id": 1, "selected_answer": "1:2"},
                {"question_id": 2, "selected_answer": "2:1"},
            ]
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "correct_count" in body
    assert "weak_concepts" in body
    assert isinstance(body["weak_concepts"], list)
    mock_service.submit_pretest.assert_called_once()


def test_submit_pretest_returns_score_and_totals(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_pretest.return_value = _make_submit_response()

    response = client.post(
        "/v1/pretests/10/submit",
        json={"answers": [{"question_id": 1, "selected_answer": "1:2"}]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == 50.0
    assert body["total_questions"] == 2
    assert body["correct_count"] == 1


def test_submit_pretest_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_pretest.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Pretest not found"
    )

    response = client.post(
        "/v1/pretests/999/submit",
        json={"answers": [{"question_id": 1, "selected_answer": "A"}]},
    )

    assert response.status_code == 404


def test_submit_pretest_missing_answers_field_returns_422(client: TestClient) -> None:
    response = client.post("/v1/pretests/10/submit", json={})
    assert response.status_code == 422


def test_submit_pretest_invalid_pretest_id_returns_422(client: TestClient) -> None:
    response = client.post(
        "/v1/pretests/abc/submit",
        json={"answers": [{"question_id": 1, "selected_answer": "A"}]},
    )
    assert response.status_code == 422


def test_submit_pretest_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.post(
        "/v1/pretests/10/submit",
        json={"answers": [{"question_id": 1, "selected_answer": "A"}]},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/pretests/{subtopic_id}/comparison
# ---------------------------------------------------------------------------


def test_get_comparison_returns_200(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_comparison.return_value = _make_comparison_response()

    response = client.get("/v1/pretests/1/comparison")

    assert response.status_code == 200
    body = response.json()
    assert "pretest_score" in body
    assert "post_lesson_score" in body
    assert "improvement" in body
    assert "message" in body
    mock_service.get_comparison.assert_called_once_with(1, 1)


def test_get_comparison_shows_improvement(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_comparison.return_value = _make_comparison_response()

    response = client.get("/v1/pretests/1/comparison")

    assert response.status_code == 200
    body = response.json()
    assert body["improvement"] == 30.0
    assert body["pretest_score"] == 50.0
    assert body["post_lesson_score"] == 80.0


def test_get_comparison_no_post_score_when_lesson_not_done(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_comparison.return_value = PretestComparisonResponse(
        subtopic_id=1,
        pretest_score=50.0,
        post_lesson_score=None,
        improvement=None,
        message="Complete the lesson and take a quiz to see your improvement.",
    )

    response = client.get("/v1/pretests/1/comparison")

    assert response.status_code == 200
    body = response.json()
    assert body["post_lesson_score"] is None
    assert body["improvement"] is None


def test_get_comparison_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_comparison.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No pretest found for this subtopic"
    )

    response = client.get("/v1/pretests/999/comparison")

    assert response.status_code == 404


def test_get_comparison_invalid_subtopic_id_returns_422(client: TestClient) -> None:
    response = client.get("/v1/pretests/abc/comparison")
    assert response.status_code == 422


def test_get_comparison_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/pretests/1/comparison")
    assert response.status_code == 401
