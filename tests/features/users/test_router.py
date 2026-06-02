"""Router tests for the users feature — account deletion endpoint.

Per ``testing-standards.md``, router tests use ``TestClient`` with a mocked
service injected via ``app.dependency_overrides``. The DB is never hit here.

Coverage shape (per Task 4.5 acceptance bullets):

* ``DELETE /v1/users/me``: 204 on correct phrase, 400 when service raises
  for bad phrase, 409 when already deleted, 422 on missing field.
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
from app.features.users.models import AccountState, Category, Role, User
from app.features.users.router import get_user_service, router as users_router
from app.features.users.service import UserService


# --- factories --------------------------------------------------------------


def _make_user(**overrides: object) -> User:
    defaults: dict[str, object] = {
        "id": 1,
        "email": "alice@example.com",
        "display_name": "Alice",
        "age": 25,
        "category": Category.PROFESSIONAL.value,
        "role": Role.LEARNER.value,
        "account_state": AccountState.VERIFIED.value,
        "is_banned": False,
        "tz_name": "UTC",
        "password_hash": "x",
        "username": "aliceuser",
        "cross_category_preview": False,
    }
    return User(**{**defaults, **overrides})


# --- fixtures ---------------------------------------------------------------


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock(spec=UserService)


@pytest.fixture
def authed_user() -> User:
    return _make_user()


@pytest.fixture
def app(mock_service: MagicMock, authed_user: User) -> Iterator[FastAPI]:
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(AuthMiddleware)
    fastapi_app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(fastapi_app)
    fastapi_app.include_router(users_router)

    fastapi_app.dependency_overrides[get_user_service] = lambda: mock_service
    fastapi_app.dependency_overrides[get_current_user] = lambda: authed_user

    try:
        yield fastapi_app
    finally:
        fastapi_app.dependency_overrides.clear()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


# ===========================================================================
# DELETE /v1/users/me
# ===========================================================================


class TestDeleteAccount:
    """Router-level tests for ``DELETE /v1/users/me``."""

    def test_correct_phrase_returns_204(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        mock_service.delete_account.return_value = None

        response = client.request(
            "DELETE",
            "/v1/users/me",
            json={"confirmation_phrase": "DELETE MY ACCOUNT"},
        )

        assert response.status_code == 204
        mock_service.delete_account.assert_called_once()

    def test_bad_phrase_returns_400(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        """When the service raises 400 for invalid confirmation, the router
        propagates it through the error handler."""
        mock_service.delete_account.side_effect = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid_confirmation",
        )

        response = client.request(
            "DELETE",
            "/v1/users/me",
            json={"confirmation_phrase": "DELETE MY ACCOUNT"},
        )

        assert response.status_code == 400
        assert response.json() == {
            "error": {"message": "invalid_confirmation", "code": "HTTP_400"}
        }

    def test_already_deleted_returns_409(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        """When the service raises 409 for already-deleted account, the
        router propagates it."""
        mock_service.delete_account.side_effect = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="account_already_deleted",
        )

        response = client.request(
            "DELETE",
            "/v1/users/me",
            json={"confirmation_phrase": "DELETE MY ACCOUNT"},
        )

        assert response.status_code == 409
        assert response.json() == {
            "error": {"message": "account_already_deleted", "code": "HTTP_409"}
        }

    def test_missing_confirmation_phrase_returns_422(
        self, client: TestClient, mock_service: MagicMock
    ) -> None:
        """Missing required field in request body triggers Pydantic 422."""
        response = client.request(
            "DELETE",
            "/v1/users/me",
            json={},
        )

        assert response.status_code == 422
        mock_service.delete_account.assert_not_called()
