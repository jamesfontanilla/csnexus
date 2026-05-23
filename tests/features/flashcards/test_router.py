"""Router layer tests for the flashcard feature (Task 15.2).

Per testing-standards.md: mocked service via dependency_overrides,
TestClient for HTTP-level testing. Tests status codes, request
validation, and response shape.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.common.deps import get_current_user, require_admin
from app.features.flashcards.models import Deck, Flashcard
from app.features.flashcards.router import get_flashcard_service
from app.features.flashcards.service import FlashcardService
from app.features.users.models import User
from app.main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_service() -> MagicMock:
    return MagicMock(spec=FlashcardService)


@pytest.fixture()
def mock_user() -> MagicMock:
    user = MagicMock(spec=User)
    user.id = 1
    user.role = "learner"
    return user


@pytest.fixture()
def mock_admin() -> MagicMock:
    user = MagicMock(spec=User)
    user.id = 99
    user.role = "admin"
    return user


@pytest.fixture()
def client(mock_service: MagicMock, mock_user: MagicMock) -> TestClient:
    """TestClient with mocked service and auth."""
    app.dependency_overrides[get_flashcard_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_client(mock_service: MagicMock, mock_admin: MagicMock) -> TestClient:
    """TestClient with admin auth."""
    app.dependency_overrides[get_flashcard_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: mock_admin
    app.dependency_overrides[require_admin] = lambda: mock_admin
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def unauth_client(mock_service: MagicMock) -> TestClient:
    """TestClient without auth override (will get 401)."""
    app.dependency_overrides[get_flashcard_service] = lambda: mock_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def _mock_deck(**kwargs) -> MagicMock:
    defaults = {
        "id": 1, "owner_id": 1, "title": "Test", "description": None,
        "category": "verbal", "visibility": "private", "tags": None,
        "clone_count": 0, "bookmark_count": 0, "average_rating": None,
        "rating_count": 0, "is_featured": False, "cloned_from_deck_id": None,
        "cloned_from_user_id": None, "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }
    defaults.update(kwargs)
    deck = MagicMock(spec=Deck)
    for k, v in defaults.items():
        setattr(deck, k, v)
    return deck


# ---------------------------------------------------------------------------
# Deck endpoint tests
# ---------------------------------------------------------------------------


class TestCreateDeckEndpoint:
    def test_returns_201_on_success(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.create_deck.return_value = _mock_deck()
        response = client.post("/v1/flashcards/decks", json={
            "title": "My Deck", "category": "verbal"
        })
        assert response.status_code == 201

    def test_returns_422_on_missing_title(self, client: TestClient) -> None:
        response = client.post("/v1/flashcards/decks", json={
            "category": "verbal"
        })
        assert response.status_code == 422

    def test_returns_422_on_invalid_category(self, client: TestClient) -> None:
        response = client.post("/v1/flashcards/decks", json={
            "title": "Deck", "category": "invalid"
        })
        assert response.status_code == 422


class TestListDecksEndpoint:
    def test_returns_200(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.list_user_decks.return_value = ([_mock_deck()], 1)
        response = client.get("/v1/flashcards/decks")
        assert response.status_code == 200

    def test_accepts_pagination_params(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.list_user_decks.return_value = ([], 0)
        response = client.get("/v1/flashcards/decks?skip=10&limit=5")
        assert response.status_code == 200


class TestDeleteDeckEndpoint:
    def test_returns_204_on_success(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.delete_deck.return_value = None
        response = client.delete("/v1/flashcards/decks/1")
        assert response.status_code == 204


class TestDuplicateDeckEndpoint:
    def test_returns_201_on_success(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.duplicate_deck.return_value = _mock_deck(id=2)
        response = client.post("/v1/flashcards/decks/1/:duplicate")
        assert response.status_code == 201


# ---------------------------------------------------------------------------
# Flashcard endpoint tests
# ---------------------------------------------------------------------------


class TestCreateFlashcardEndpoint:
    def test_returns_201_on_success(self, client: TestClient, mock_service: MagicMock) -> None:
        card = MagicMock(spec=Flashcard)
        card.id = 1
        card.deck_id = 1
        card.front = "Q"
        card.back = "A"
        card.card_type = "basic"
        card.hints = None
        card.tags = None
        card.explanation = None
        card.ease_factor = 2.5
        card.retention_score = 0.0
        card.memory_stability = 1.0
        card.review_interval = 1
        card.lapse_count = 0
        card.mastery_percentage = 0.0
        card.next_review_date = None
        card.last_review_date = None
        card.total_reviews = 0
        card.successful_reviews = 0
        card.is_graduated = False
        card.is_bookmarked = False
        card.created_at = "2024-01-01T00:00:00Z"
        card.updated_at = "2024-01-01T00:00:00Z"
        mock_service.create_flashcard.return_value = card
        response = client.post("/v1/flashcards/decks/1/cards", json={
            "front": "What is X?", "back": "X is Y.", "card_type": "basic"
        })
        assert response.status_code == 201

    def test_returns_422_on_missing_front(self, client: TestClient) -> None:
        response = client.post("/v1/flashcards/decks/1/cards", json={
            "back": "Answer", "card_type": "basic"
        })
        assert response.status_code == 422


class TestDeleteFlashcardEndpoint:
    def test_returns_204(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.delete_flashcard.return_value = None
        response = client.delete("/v1/flashcards/cards/1")
        assert response.status_code == 204


# ---------------------------------------------------------------------------
# Session endpoint tests
# ---------------------------------------------------------------------------


class TestStartSessionEndpoint:
    def test_returns_201(self, client: TestClient, mock_service: MagicMock) -> None:
        session = MagicMock()
        session.id = 1
        session.study_mode = "swipe"
        mock_service.start_study_session.return_value = session
        response = client.post("/v1/flashcards/sessions", json={
            "study_mode": "swipe", "deck_ids": [1]
        })
        assert response.status_code == 201
        assert response.json()["id"] == 1

    def test_returns_422_on_empty_deck_ids(self, client: TestClient) -> None:
        response = client.post("/v1/flashcards/sessions", json={
            "study_mode": "swipe", "deck_ids": []
        })
        assert response.status_code == 422


class TestEndSessionEndpoint:
    def test_returns_200(self, client: TestClient, mock_service: MagicMock) -> None:
        from app.features.flashcards.schemas import StudySessionSummary
        mock_service.end_study_session.return_value = StudySessionSummary(
            cards_reviewed=10, cards_correct=7, cards_incorrect=2,
            cards_skipped=1, duration_seconds=300, xp_earned=27,
        )
        response = client.post("/v1/flashcards/sessions/1/:end")
        assert response.status_code == 200
        assert response.json()["xp_earned"] == 27


# ---------------------------------------------------------------------------
# Marketplace endpoint tests
# ---------------------------------------------------------------------------


class TestMarketplaceEndpoint:
    def test_search_returns_200(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.search_marketplace.return_value = ([_mock_deck(visibility="public")], 1)
        response = client.get("/v1/flashcards/marketplace")
        assert response.status_code == 200

    def test_rate_deck_returns_201(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.rate_deck.return_value = None
        response = client.post("/v1/flashcards/marketplace/1/ratings", json={"rating": 4})
        assert response.status_code == 201

    def test_rate_deck_422_on_invalid_rating(self, client: TestClient) -> None:
        response = client.post("/v1/flashcards/marketplace/1/ratings", json={"rating": 6})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Social endpoint tests
# ---------------------------------------------------------------------------


class TestFollowEndpoint:
    def test_follow_returns_201(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.follow_creator.return_value = None
        response = client.post("/v1/flashcards/creators/2/:follow")
        assert response.status_code == 201

    def test_unfollow_returns_204(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.unfollow_creator.return_value = None
        response = client.delete("/v1/flashcards/creators/2/:follow")
        assert response.status_code == 204


# ---------------------------------------------------------------------------
# Admin endpoint tests
# ---------------------------------------------------------------------------


class TestAdminEndpoints:
    def test_admin_analytics_returns_200(self, admin_client: TestClient, mock_service: MagicMock) -> None:
        mock_service.get_admin_analytics.return_value = {"top_failed_cards": []}
        response = admin_client.get("/v1/flashcards/admin/analytics")
        assert response.status_code == 200

    def test_flag_deck_returns_200(self, admin_client: TestClient, mock_service: MagicMock) -> None:
        mock_service.flag_deck.return_value = None
        response = admin_client.post("/v1/flashcards/admin/decks/1/:flag")
        assert response.status_code == 200

    def test_feature_deck_returns_200(self, admin_client: TestClient, mock_service: MagicMock) -> None:
        mock_service.toggle_featured.return_value = None
        response = admin_client.post("/v1/flashcards/admin/decks/1/:feature")
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# Sync endpoint tests
# ---------------------------------------------------------------------------


class TestSyncEndpoint:
    def test_sync_returns_200(self, client: TestClient, mock_service: MagicMock) -> None:
        mock_service.batch_sync_reviews.return_value = {"accepted": 2, "duplicates": 0, "failures": 0}
        response = client.post("/v1/flashcards/sync", json={
            "items": [
                {
                    "client_event_id": "evt-1",
                    "card_id": 1,
                    "response_type": "remembered",
                    "reviewed_at": "2024-01-01T10:00:00Z",
                },
                {
                    "client_event_id": "evt-2",
                    "card_id": 2,
                    "response_type": "forgot",
                    "reviewed_at": "2024-01-01T10:01:00Z",
                },
            ]
        })
        assert response.status_code == 200
        assert response.json()["accepted"] == 2

    def test_sync_422_on_empty_items(self, client: TestClient) -> None:
        response = client.post("/v1/flashcards/sync", json={"items": []})
        assert response.status_code == 422
