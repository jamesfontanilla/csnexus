"""Router-layer tests for the learning techniques slice.

Uses TestClient with mocked LearningTechniquesService. No DB is hit here.

Endpoints under test:
  POST  /v1/explanations/{question_id}/note
  GET   /v1/notes
  POST  /v1/lessons/{lesson_id}/reflections
  POST  /v1/quiz-attempts/{attempt_id}/recall-answer
  GET   /v1/queue/goodnight
  POST  /v1/queue/goodnight/:complete
  POST  /v1/sessions/{session_date}/reflection
  GET   /v1/sessions/reflections
  POST  /v1/challenges/{subtopic_id}/attempt
  POST  /v1/challenges/{challenge_id}/retest
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
from app.features.learning_techniques.router import _get_service, router as lt_router
from app.features.learning_techniques.schemas import (
    ChallengeAttemptResponse,
    ChallengeComparisonResponse,
    GoodnightSessionResponse,
    LessonReflectionResponse,
    PersonalNoteResponse,
    RecallAnswerResponse,
    SessionReflectionResponse,
)
from app.features.learning_techniques.service import LearningTechniquesService
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


def _make_note(question_id: int = 42) -> PersonalNoteResponse:
    return PersonalNoteResponse(
        id=1,
        question_id=question_id,
        note_text="Because proportion means equal ratios.",
        created_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc),
    )


def _make_lesson_reflection(lesson_id: int = 5) -> LessonReflectionResponse:
    return LessonReflectionResponse(
        id=1,
        lesson_id=lesson_id,
        section_index=2,
        reflection_text="I struggled with the formula derivation.",
        created_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc),
    )


def _make_recall_response(is_correct: bool | None = True, match_type: str = "exact") -> RecallAnswerResponse:
    return RecallAnswerResponse(
        question_id=1,
        is_correct=is_correct,
        match_type=match_type,
        correct_answer="proportion",
        user_response="proportion",
    )


def _make_goodnight_session() -> GoodnightSessionResponse:
    return GoodnightSessionResponse(items=[], estimated_minutes=0)


def _make_session_reflection() -> SessionReflectionResponse:
    return SessionReflectionResponse(
        id=1,
        session_date=datetime(2025, 6, 4, tzinfo=timezone.utc),
        hardest_item_id=7,
        confidence_rating=3,
        review_note="Need more practice on ratios.",
        created_at=datetime(2025, 6, 4, 10, 0, tzinfo=timezone.utc),
    )


def _make_challenge_attempt() -> ChallengeAttemptResponse:
    return ChallengeAttemptResponse(
        challenge_id=10,
        subtopic_id=1,
        question_stem="What is the relationship between ratio and proportion?",
        is_correct=False,
        message=(
            "That's expected — this is a tough question designed to highlight "
            "what the lesson will teach you. Research shows that attempting hard "
            "problems before learning actually improves long-term retention."
        ),
    )


def _make_challenge_comparison() -> ChallengeComparisonResponse:
    return ChallengeComparisonResponse(
        challenge_id=10,
        pre_lesson_correct=False,
        post_lesson_correct=True,
        is_productive_failure_success=True,
        message=(
            "You went from not knowing to getting it right after the lesson. "
            "This is productive failure in action — your brain encoded it deeply."
        ),
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=LearningTechniquesService)


@pytest.fixture
def authed_user() -> User:
    return _make_user()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(lt_router)

    fastapi_app.dependency_overrides[_get_service] = lambda: mock_service
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
# POST /v1/explanations/{question_id}/note
# ---------------------------------------------------------------------------


def test_create_note_returns_201(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.create_personal_note.return_value = _make_note()

    response = client.post(
        "/v1/explanations/42/note",
        json={"note_text": "Because proportion means equal ratios."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["question_id"] == 42
    assert "note_text" in body
    mock_service.create_personal_note.assert_called_once_with(
        user_id=1, question_id=42, note_text="Because proportion means equal ratios."
    )


def test_create_note_missing_note_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/explanations/42/note", json={})
    assert response.status_code == 422


def test_create_note_invalid_question_id_returns_422(client: TestClient) -> None:
    response = client.post("/v1/explanations/abc/note", json={"note_text": "test"})
    assert response.status_code == 422


def test_create_note_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.post(
        "/v1/explanations/42/note", json={"note_text": "test"}
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/notes
# ---------------------------------------------------------------------------


def test_get_all_notes_returns_200(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_all_notes.return_value = [_make_note(42), _make_note(43)]

    response = client.get("/v1/notes")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2
    mock_service.get_all_notes.assert_called_once_with(user_id=1)


def test_get_all_notes_empty_list(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_all_notes.return_value = []

    response = client.get("/v1/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_notes_401_without_token(unauthenticated_client: TestClient) -> None:
    response = unauthenticated_client.get("/v1/notes")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/lessons/{lesson_id}/reflections
# ---------------------------------------------------------------------------


def test_create_lesson_reflection_returns_201(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.create_lesson_reflection.return_value = _make_lesson_reflection()

    response = client.post(
        "/v1/lessons/5/reflections",
        json={"section_index": 2, "reflection_text": "I struggled with the formula derivation."},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["lesson_id"] == 5
    assert body["section_index"] == 2
    mock_service.create_lesson_reflection.assert_called_once_with(
        user_id=1,
        lesson_id=5,
        section_index=2,
        reflection_text="I struggled with the formula derivation.",
    )


def test_create_lesson_reflection_missing_fields_returns_422(client: TestClient) -> None:
    response = client.post("/v1/lessons/5/reflections", json={})
    assert response.status_code == 422


def test_create_lesson_reflection_invalid_lesson_id_returns_422(client: TestClient) -> None:
    response = client.post(
        "/v1/lessons/abc/reflections",
        json={"section_index": 0, "reflection_text": "test"},
    )
    assert response.status_code == 422


def test_create_lesson_reflection_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.post(
        "/v1/lessons/5/reflections",
        json={"section_index": 2, "reflection_text": "test"},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/quiz-attempts/{attempt_id}/recall-answer
# ---------------------------------------------------------------------------


def test_submit_recall_answer_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_recall_answer.return_value = _make_recall_response()

    response = client.post(
        "/v1/quiz-attempts/5/recall-answer?question_id=1",
        json={"user_response": "proportion"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["is_correct"] is True
    assert body["match_type"] == "exact"
    assert "correct_answer" in body


def test_submit_recall_answer_fuzzy_match(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_recall_answer.return_value = _make_recall_response(
        is_correct=True, match_type="fuzzy"
    )

    response = client.post(
        "/v1/quiz-attempts/5/recall-answer?question_id=1",
        json={"user_response": "proporton"},
    )

    assert response.status_code == 200
    assert response.json()["match_type"] == "fuzzy"


def test_submit_recall_answer_question_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_recall_answer.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
    )

    response = client.post(
        "/v1/quiz-attempts/5/recall-answer?question_id=999",
        json={"user_response": "proportion"},
    )

    assert response.status_code == 404


def test_submit_recall_answer_missing_user_response_returns_422(
    client: TestClient,
) -> None:
    response = client.post("/v1/quiz-attempts/5/recall-answer?question_id=1", json={})
    assert response.status_code == 422


def test_submit_recall_answer_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.post(
        "/v1/quiz-attempts/5/recall-answer?question_id=1",
        json={"user_response": "proportion"},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/queue/goodnight
# ---------------------------------------------------------------------------


def test_get_goodnight_review_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_goodnight_review.return_value = _make_goodnight_session()

    response = client.get("/v1/queue/goodnight")

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "estimated_minutes" in body
    mock_service.get_goodnight_review.assert_called_once_with(user_id=1)


def test_get_goodnight_review_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.get("/v1/queue/goodnight")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/queue/goodnight/:complete
# ---------------------------------------------------------------------------


def test_complete_goodnight_review_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.complete_goodnight_review.return_value = {
        "status": "completed",
        "interval_bonus": 1.2,
    }

    response = client.post("/v1/queue/goodnight/:complete")

    assert response.status_code == 200
    body = response.json()
    assert body["interval_bonus"] == 1.2
    assert body["status"] == "completed"
    mock_service.complete_goodnight_review.assert_called_once_with(user_id=1)


def test_complete_goodnight_review_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.post("/v1/queue/goodnight/:complete")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/sessions/{session_date}/reflection
# ---------------------------------------------------------------------------


def test_create_session_reflection_returns_201(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.create_session_reflection.return_value = _make_session_reflection()

    response = client.post(
        "/v1/sessions/2025-06-04T00:00:00/reflection",
        json={
            "hardest_item_id": 7,
            "confidence_rating": 3,
            "review_note": "Need more practice on ratios.",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["confidence_rating"] == 3
    assert "session_date" in body
    mock_service.create_session_reflection.assert_called_once()


def test_create_session_reflection_missing_confidence_returns_422(
    client: TestClient,
) -> None:
    response = client.post(
        "/v1/sessions/2025-06-04T00:00:00/reflection",
        json={"hardest_item_id": 7},
    )
    assert response.status_code == 422


def test_create_session_reflection_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.post(
        "/v1/sessions/2025-06-04T00:00:00/reflection",
        json={"confidence_rating": 3},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /v1/sessions/reflections
# ---------------------------------------------------------------------------


def test_get_session_reflections_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.get_session_reflections.return_value = [_make_session_reflection()]

    response = client.get("/v1/sessions/reflections")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["confidence_rating"] == 3
    mock_service.get_session_reflections.assert_called_once_with(user_id=1)


def test_get_session_reflections_empty(client: TestClient, mock_service: MagicMock) -> None:
    mock_service.get_session_reflections.return_value = []

    response = client.get("/v1/sessions/reflections")

    assert response.status_code == 200
    assert response.json() == []


def test_get_session_reflections_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.get("/v1/sessions/reflections")
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/challenges/{subtopic_id}/attempt
# ---------------------------------------------------------------------------


def test_submit_challenge_attempt_returns_201(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_challenge_attempt.return_value = _make_challenge_attempt()

    response = client.post("/v1/challenges/1/attempt", json={"answer": "proportion"})

    assert response.status_code == 201
    body = response.json()
    assert "challenge_id" in body
    assert "question_stem" in body
    assert "is_correct" in body
    assert "message" in body
    mock_service.submit_challenge_attempt.assert_called_once_with(
        user_id=1, subtopic_id=1, answer="proportion"
    )


def test_submit_challenge_attempt_wrong_has_normalizing_message(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_challenge_attempt.return_value = _make_challenge_attempt()

    response = client.post("/v1/challenges/1/attempt", json={"answer": "wrong"})

    assert response.status_code == 201
    body = response.json()
    assert body["is_correct"] is False
    # Failure-normalizing framing should be present
    assert "retention" in body["message"] or "expected" in body["message"]


def test_submit_challenge_attempt_no_hard_questions_returns_422(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_challenge_attempt.side_effect = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="No hard questions available for this subtopic",
    )

    response = client.post("/v1/challenges/1/attempt", json={"answer": "anything"})

    assert response.status_code == 422


def test_submit_challenge_attempt_missing_answer_returns_422(client: TestClient) -> None:
    response = client.post("/v1/challenges/1/attempt", json={})
    assert response.status_code == 422


def test_submit_challenge_attempt_invalid_subtopic_id_returns_422(
    client: TestClient,
) -> None:
    response = client.post("/v1/challenges/abc/attempt", json={"answer": "test"})
    assert response.status_code == 422


def test_submit_challenge_attempt_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.post(
        "/v1/challenges/1/attempt", json={"answer": "proportion"}
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# POST /v1/challenges/{challenge_id}/retest
# ---------------------------------------------------------------------------


def test_submit_challenge_retest_returns_200(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_challenge_retest.return_value = _make_challenge_comparison()

    response = client.post("/v1/challenges/10/retest", json={"answer": "proportion"})

    assert response.status_code == 200
    body = response.json()
    assert "pre_lesson_correct" in body
    assert "post_lesson_correct" in body
    assert "is_productive_failure_success" in body
    assert "message" in body
    mock_service.submit_challenge_retest.assert_called_once_with(
        user_id=1, challenge_id=10, answer="proportion"
    )


def test_submit_challenge_retest_productive_failure_success(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_challenge_retest.return_value = _make_challenge_comparison()

    response = client.post("/v1/challenges/10/retest", json={"answer": "proportion"})

    assert response.status_code == 200
    body = response.json()
    assert body["is_productive_failure_success"] is True
    assert "productive failure" in body["message"].lower()


def test_submit_challenge_retest_not_found_returns_404(
    client: TestClient, mock_service: MagicMock
) -> None:
    mock_service.submit_challenge_retest.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found"
    )

    response = client.post("/v1/challenges/999/retest", json={"answer": "proportion"})

    assert response.status_code == 404


def test_submit_challenge_retest_missing_answer_returns_422(client: TestClient) -> None:
    response = client.post("/v1/challenges/10/retest", json={})
    assert response.status_code == 422


def test_submit_challenge_retest_invalid_challenge_id_returns_422(
    client: TestClient,
) -> None:
    response = client.post("/v1/challenges/abc/retest", json={"answer": "test"})
    assert response.status_code == 422


def test_submit_challenge_retest_401_without_token(
    unauthenticated_client: TestClient,
) -> None:
    response = unauthenticated_client.post(
        "/v1/challenges/10/retest", json={"answer": "proportion"}
    )
    assert response.status_code == 401
