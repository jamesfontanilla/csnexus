"""Service tests for ``UserService``.

Per ``testing-standards.md``, service tests mock the repository layer via
``MagicMock(spec=...)``. Each branch (happy path + exception) gets its own
test. Assertions target status codes (contractual) rather than detail strings.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.auth.repository import AuthRepository
from app.features.users.models import AccountState, User
from app.features.users.repository import UserRepository
from app.features.users.service import UserService


# --- helpers ---------------------------------------------------------------


def _make_user(**kwargs) -> MagicMock:
    """Build a mock User with sensible defaults."""
    defaults = {
        "id": 1,
        "email": "test@example.com",
        "display_name": "Test User",
        "username": "testuser",
        "account_state": AccountState.VERIFIED.value,
        "is_banned": False,
    }
    defaults.update(kwargs)
    user = MagicMock(spec=User)
    for key, value in defaults.items():
        setattr(user, key, value)
    return user


def _make_service() -> tuple[UserService, MagicMock, MagicMock]:
    """Return ``(service, user_repo_mock, auth_repo_mock)``."""
    user_repo = MagicMock(spec=UserRepository)
    auth_repo = MagicMock(spec=AuthRepository)
    service = UserService(user_repo=user_repo, auth_repo=auth_repo)
    return service, user_repo, auth_repo


# --- delete_account --------------------------------------------------------


class TestDeleteAccount:
    """Tests for ``UserService.delete_account``."""

    def test_correct_phrase_soft_deletes_and_revokes_sessions(self) -> None:
        service, user_repo, auth_repo = _make_service()
        user = _make_user()

        service.delete_account(user, confirmation_phrase="DELETE MY ACCOUNT")

        user_repo.set_account_state.assert_called_once_with(user, AccountState.DELETED)
        auth_repo.revoke_all_for_user.assert_called_once_with(user.id)

    def test_wrong_phrase_raises_400(self) -> None:
        service, user_repo, auth_repo = _make_service()
        user = _make_user()

        with pytest.raises(HTTPException) as exc_info:
            service.delete_account(user, confirmation_phrase="wrong phrase")

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "invalid_confirmation"
        user_repo.set_account_state.assert_not_called()
        auth_repo.revoke_all_for_user.assert_not_called()

    def test_already_deleted_raises_409(self) -> None:
        service, user_repo, auth_repo = _make_service()
        user = _make_user(account_state=AccountState.DELETED.value)

        with pytest.raises(HTTPException) as exc_info:
            service.delete_account(user, confirmation_phrase="DELETE MY ACCOUNT")

        assert exc_info.value.status_code == 409
        assert exc_info.value.detail == "account_already_deleted"
        user_repo.set_account_state.assert_not_called()
        auth_repo.revoke_all_for_user.assert_not_called()

    def test_empty_phrase_raises_400(self) -> None:
        service, _, _ = _make_service()
        user = _make_user()

        with pytest.raises(HTTPException) as exc_info:
            service.delete_account(user, confirmation_phrase="")

        assert exc_info.value.status_code == 400

    def test_case_sensitive_phrase_mismatch_raises_400(self) -> None:
        service, _, _ = _make_service()
        user = _make_user()

        with pytest.raises(HTTPException) as exc_info:
            service.delete_account(user, confirmation_phrase="delete my account")

        assert exc_info.value.status_code == 400
