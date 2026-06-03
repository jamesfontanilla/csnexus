"""Router tests for the explanations feature — mocked service, HTTP client."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.features.explanations.models import QuestionExplanation
from app.features.explanations.service import ExplanationService
from app.features.users.models import User
from app.main import app


@pytest.fixture
def mock_user() -> User:
    user = MagicMock(spec=User)
    user.id = 1
    user.role = "LEARNER"
    user.is_banned = False
    return user


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=ExplanationService)


@pytest.fixture
def client(mock_user, mock_service) -> TestClient:
    from app.common.deps import get_current_user
    from app.features.explanations.router import get_explanation_service

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_explanation_service] = lambda: mock_service

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def _make_explanation(**kwargs) -> MagicMock:
    """Build a mock QuestionExplanation with sensible defaults."""
    defaults = {
        "id": 1,
        "question_id": 42,
        "explanation_text": "This is a detailed explanation of the concept that is at least fifty characters long for validation.",
        "key_concept": "Test Concept",
        "related_subtopics": "[1, 2, 3]",
        "cache_version": 1,
    }
    defaults.update(kwargs)
    mock = MagicMock(spec=QuestionExplanation)
    for k, v in defaults.items():
        setattr(mock, k, v)
    return mock


# ---------------------------------------------------------------------------
# GET /v1/explanations/{question_id}
# ---------------------------------------------------------------------------


def test_get_explanation_returns_200(client, mock_service):
    mock_service.get_explanation.return_value = _make_explanation()
    response = client.get("/v1/explanations/42")
    assert response.status_code == 200
    data = response.json()
    assert data["key_concept"] == "Test Concept"
    assert data["related_subtopics"] == [1, 2, 3]
    assert data["cache_version"] == 1
    assert "ETag" in response.headers
    assert response.headers["ETag"] == "1"


def test_get_explanation_returns_404_when_not_found(client, mock_service):
    mock_service.get_explanation.return_value = None
    response = client.get("/v1/explanations/999")
    assert response.status_code == 404


def test_get_explanation_returns_304_when_etag_matches(client, mock_service):
    mock_service.get_explanation.return_value = _make_explanation(cache_version=5)
    response = client.get(
        "/v1/explanations/42", headers={"If-None-Match": "5"}
    )
    assert response.status_code == 304


def test_get_explanation_returns_200_when_etag_does_not_match(client, mock_service):
    mock_service.get_explanation.return_value = _make_explanation(cache_version=5)
    response = client.get(
        "/v1/explanations/42", headers={"If-None-Match": "3"}
    )
    assert response.status_code == 200
    assert response.headers["ETag"] == "5"


# ---------------------------------------------------------------------------
# POST /v1/explanations/bulk
# ---------------------------------------------------------------------------


def test_bulk_returns_200_with_explanations(client, mock_service):
    exp1 = _make_explanation(question_id=1)
    exp2 = _make_explanation(question_id=2, key_concept="Other Concept")
    mock_service.get_bulk_explanations.return_value = {1: exp1, 2: exp2}

    response = client.post(
        "/v1/explanations/bulk", json={"question_ids": [1, 2]}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["explanations"]) == 2
    assert data["explanations"][0]["key_concept"] == "Test Concept"
    assert data["explanations"][1]["key_concept"] == "Other Concept"


def test_bulk_returns_null_for_missing_explanations(client, mock_service):
    exp1 = _make_explanation(question_id=1)
    mock_service.get_bulk_explanations.return_value = {1: exp1, 2: None}

    response = client.post(
        "/v1/explanations/bulk", json={"question_ids": [1, 2]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["explanations"][0] is not None
    assert data["explanations"][1] is None


def test_bulk_returns_422_for_empty_list(client):
    response = client.post(
        "/v1/explanations/bulk", json={"question_ids": []}
    )
    assert response.status_code == 422


def test_bulk_returns_422_for_too_many_ids(client):
    response = client.post(
        "/v1/explanations/bulk", json={"question_ids": list(range(1, 52))}
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /v1/explanations/{question_id}/:escalate
# ---------------------------------------------------------------------------


def test_escalate_returns_200(client, mock_service):
    mock_service.escalate_to_tutor.return_value = {
        "interaction_id": 10,
        "response_text": "Here's a deeper explanation.",
        "interaction_type": "explain_answer",
    }
    response = client.post("/v1/explanations/42/:escalate")
    assert response.status_code == 200
    data = response.json()
    assert data["interaction_id"] == 10
    assert data["response_text"] == "Here's a deeper explanation."


def test_escalate_returns_429_when_limit_exceeded(client, mock_service):
    mock_service.escalate_to_tutor.side_effect = HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Daily AI Tutor escalation limit reached (20/day).",
    )
    response = client.post("/v1/explanations/42/:escalate")
    assert response.status_code == 429


# ---------------------------------------------------------------------------
# Auth guard
# ---------------------------------------------------------------------------


def test_unauthenticated_returns_401():
    app.dependency_overrides.clear()
    client = TestClient(app)
    response = client.get("/v1/explanations/42")
    assert response.status_code == 401
