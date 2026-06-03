"""Repository tests for OnboardingRepository — real DB, no mocks."""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from sqlalchemy.orm import Session

from app.features.planner.models import OnboardingProfile
from app.features.planner.repository import OnboardingRepository
from app.features.users.models import User


def _create_user(db: Session, user_id: int = 1) -> User:
    """Create a user for FK reference."""
    user = User(
        id=user_id,
        email=f"user{user_id}@test.com",
        display_name="Test User",
        age=25,
        category="PROFESSIONAL",
        password_hash="hashed",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _make_profile(user_id: int = 1, **kwargs) -> OnboardingProfile:
    """Build a profile with sensible defaults."""
    defaults = {
        "user_id": user_id,
        "exam_date": date.today() + timedelta(days=30),
        "exam_category": "Professional",
        "time_budget_minutes": 30,
    }
    defaults.update(kwargs)
    return OnboardingProfile(**defaults)


class TestOnboardingRepository:
    """Tests for OnboardingRepository CRUD operations."""

    def test_create_profile(self, db_session: Session):
        """create_profile persists and returns the profile."""
        _create_user(db_session)
        repo = OnboardingRepository(db=db_session)

        profile = _make_profile(user_id=1)
        result = repo.create_profile(profile)

        assert result.id is not None
        assert result.user_id == 1
        assert result.exam_category == "Professional"
        assert result.time_budget_minutes == 30

    def test_get_profile_found(self, db_session: Session):
        """get_profile returns profile when exists."""
        _create_user(db_session)
        repo = OnboardingRepository(db=db_session)
        repo.create_profile(_make_profile(user_id=1))

        result = repo.get_profile(user_id=1)

        assert result is not None
        assert result.user_id == 1

    def test_get_profile_not_found(self, db_session: Session):
        """get_profile returns None when no profile exists."""
        repo = OnboardingRepository(db=db_session)

        result = repo.get_profile(user_id=999)

        assert result is None

    def test_update_exam_date(self, db_session: Session):
        """update_exam_date updates the date and returns profile."""
        _create_user(db_session)
        repo = OnboardingRepository(db=db_session)
        repo.create_profile(_make_profile(user_id=1))

        new_date = date.today() + timedelta(days=60)
        result = repo.update_exam_date(user_id=1, exam_date=new_date)

        assert result is not None
        assert result.exam_date == new_date

    def test_update_exam_date_no_profile(self, db_session: Session):
        """update_exam_date returns None when no profile exists."""
        repo = OnboardingRepository(db=db_session)

        result = repo.update_exam_date(user_id=999, exam_date=date.today() + timedelta(days=30))

        assert result is None
