"""FastAPI router for self-user routes (admin user routes live in admin slice).

Routes mounted under ``/v1/users``:

* ``PATCH /me``                — update the authenticated user's profile.
* ``GET   /usernames/:check``  — check if a username is available.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.auth.repository import AuthRepository
from app.features.users.models import User
from app.features.users.repository import UserRepository
from app.features.users.schemas import (
    AccountDeleteRequest,
    UserResponse,
    UserUpdate,
    validate_username,
)
from app.features.users.service import UserService
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/users", tags=["users"])


# --- factories -------------------------------------------------------------


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Construct a :class:`UserService` for the request scope."""
    return UserService(user_repo=UserRepository(db=db), auth_repo=AuthRepository(db=db))


# --- routes ----------------------------------------------------------------


@router.patch("/me", response_model=UserResponse)
def update_profile(
    payload: UserUpdate,
    user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> User:
    """Update the authenticated user's profile (display_name, username, tz_name)."""
    return service.update_profile(user, payload)


@router.get("/usernames:check")
def check_username(
    username: str = Query(min_length=3, max_length=30),
    service: UserService = Depends(get_user_service),
) -> dict[str, bool]:
    """Check whether a username is available (case-insensitive).

    Returns ``{"available": true}`` or ``{"available": false}``.
    Validates format before checking availability.
    """
    try:
        validate_username(username)
    except ValueError:
        return {"available": False}
    return {"available": service.check_username_available(username)}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    payload: AccountDeleteRequest,
    user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> Response:
    """Soft-delete the authenticated user's account.

    Requires a confirmation phrase (``"DELETE MY ACCOUNT"``) in the request
    body. Transitions the account to DELETED state and revokes all sessions.
    """
    service.delete_account(user, confirmation_phrase=payload.confirmation_phrase)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
