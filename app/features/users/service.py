"""User business logic (self-service profile and admin user actions).

Handles username uniqueness enforcement and profile updates. The username
is unique case-insensitively: "Alice" and "alice" cannot coexist. When a
user changes their username, the old one is immediately released for others.

Account deletion is a soft-delete: the user's ``account_state`` transitions
to ``DELETED`` and all sessions are revoked, but data is retained for future
GDPR-style deferred purge.
"""

from __future__ import annotations

from typing import Final

from fastapi import HTTPException, status

from app.features.auth.repository import AuthRepository
from app.features.users.models import AccountState, User
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserUpdate

_CONFIRMATION_PHRASE: Final[str] = "DELETE MY ACCOUNT"


class UserService:
    """Self-service profile operations."""

    def __init__(
        self,
        *,
        user_repo: UserRepository,
        auth_repo: AuthRepository,
    ) -> None:
        self._user_repo = user_repo
        self._auth_repo = auth_repo

    def update_profile(self, user: User, payload: UserUpdate) -> User:
        """Apply partial profile updates. Enforces username uniqueness.

        When a username is provided and differs from the current one, the
        service checks that no other user holds it (case-insensitive). If
        the check passes, the old username is simply overwritten — making
        it immediately available for others.
        """
        fields = payload.model_dump(exclude_unset=True)

        if "username" in fields and fields["username"] is not None:
            new_username: str = fields["username"]
            # Skip the DB check if the user is keeping the same username
            if user.username is None or new_username.lower() != user.username.lower():
                existing = self._user_repo.get_by_username(new_username)
                if existing is not None and existing.id != user.id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="username_taken",
                    )

        return self._user_repo.update(user, **fields)

    def check_username_available(self, username: str) -> bool:
        """Return True if the username is not taken (case-insensitive)."""
        return self._user_repo.get_by_username(username) is None

    def delete_account(self, user: User, *, confirmation_phrase: str) -> None:
        """Soft-delete the user account and revoke all sessions.

        Steps (Req 5.7, 5.8):

        1. Verify ``confirmation_phrase`` equals the canonical phrase.
        2. Guard against double-deletion (409 if already DELETED).
        3. Transition ``account_state`` to DELETED via the repository.
        4. Revoke all active sessions so the user is immediately logged out.
        """
        if confirmation_phrase != _CONFIRMATION_PHRASE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid_confirmation",
            )

        if user.account_state == AccountState.DELETED.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="account_already_deleted",
            )

        self._user_repo.set_account_state(user, AccountState.DELETED)
        self._auth_repo.revoke_all_for_user(user.id)
