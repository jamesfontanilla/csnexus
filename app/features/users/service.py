"""User business logic (self-service profile and admin user actions).

Handles username uniqueness enforcement and profile updates. The username
is unique case-insensitively: "Alice" and "alice" cannot coexist. When a
user changes their username, the old one is immediately released for others.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from app.features.users.models import User
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserUpdate


class UserService:
    """Self-service profile operations."""

    def __init__(self, *, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

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
