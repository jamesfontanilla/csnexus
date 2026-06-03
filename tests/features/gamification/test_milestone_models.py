"""Model tests for CompetenceMilestone, CompetenceMilestoneAward, StudyConsistency.

Per testing-standards.md: real DB, no mocks. Validates ORM definitions,
constraints, and defaults before a repository layer is built.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.features.gamification.models import (
    CompetenceMilestone,
    CompetenceMilestoneAward,
    StudyConsistency,
)
from app.features.users.models import Category, User
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate


# --- factories --------------------------------------------------------------


def _make_user(db: Session, *, email: str = "alice@example.com") -> User:
    repo = UserRepository(db=db)
    username = email.split("@")[0].replace(".", "_").replace("-", "_")
    return repo.create(
        UserCreate(
            email=email,
            display_name="Alice",
            username=username,
            age=25,
            category=Category.PROFESSIONAL.value,
            password="Strong1Pass!",
        ),
        password_hash="bcrypt$fake$hash",
    )


def _make_milestone(
    db: Session,
    *,
    slug: str = "verbal-mastery",
    name: str = "Verbal Mastery",
    description: str = "Master all 23 verbal subtopics",
    category: str = "mastery",
    threshold_config: str | None = None,
) -> CompetenceMilestone:
    config = threshold_config or json.dumps(
        {"required_mastery": 0.8, "subtopic_count": 23}
    )
    milestone = CompetenceMilestone(
        slug=slug,
        name=name,
        description=description,
        category=category,
        threshold_config=config,
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone


# --- CompetenceMilestone tests -----------------------------------------------


def test_create_milestone(db_session: Session) -> None:
    milestone = _make_milestone(db_session)

    assert milestone.id is not None
    assert milestone.slug == "verbal-mastery"
    assert milestone.name == "Verbal Mastery"
    assert milestone.category == "mastery"
    assert milestone.created_at is not None


def test_milestone_slug_unique(db_session: Session) -> None:
    _make_milestone(db_session, slug="unique-slug")

    with pytest.raises(IntegrityError):
        _make_milestone(db_session, slug="unique-slug")


# --- CompetenceMilestoneAward tests ------------------------------------------


def test_award_milestone_to_user(db_session: Session) -> None:
    user = _make_user(db_session)
    milestone = _make_milestone(db_session)

    award = CompetenceMilestoneAward(
        user_id=user.id,
        milestone_id=milestone.id,
        triggering_values=json.dumps({"mastery_scores": [0.85, 0.9]}),
    )
    db_session.add(award)
    db_session.commit()
    db_session.refresh(award)

    assert award.id is not None
    assert award.user_id == user.id
    assert award.milestone_id == milestone.id
    assert award.awarded_at is not None


def test_award_unique_constraint_user_milestone(db_session: Session) -> None:
    user = _make_user(db_session)
    milestone = _make_milestone(db_session)

    award1 = CompetenceMilestoneAward(
        user_id=user.id,
        milestone_id=milestone.id,
        triggering_values=json.dumps({"first": True}),
    )
    db_session.add(award1)
    db_session.commit()

    award2 = CompetenceMilestoneAward(
        user_id=user.id,
        milestone_id=milestone.id,
        triggering_values=json.dumps({"duplicate": True}),
    )
    db_session.add(award2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_award_cascade_on_user_delete(db_session: Session) -> None:
    user = _make_user(db_session)
    milestone = _make_milestone(db_session)

    award = CompetenceMilestoneAward(
        user_id=user.id,
        milestone_id=milestone.id,
        triggering_values=json.dumps({"test": 1}),
    )
    db_session.add(award)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    remaining = db_session.query(CompetenceMilestoneAward).all()
    assert len(remaining) == 0


# --- StudyConsistency tests --------------------------------------------------


def test_create_study_consistency(db_session: Session) -> None:
    user = _make_user(db_session)

    consistency = StudyConsistency(user_id=user.id)
    db_session.add(consistency)
    db_session.commit()
    db_session.refresh(consistency)

    assert consistency.id is not None
    assert consistency.current_streak == 0
    assert consistency.longest_streak == 0
    assert consistency.total_consistent_days == 0
    assert consistency.last_qualifying_date is None
    assert consistency.updated_at is not None


def test_study_consistency_user_unique(db_session: Session) -> None:
    user = _make_user(db_session)

    c1 = StudyConsistency(user_id=user.id)
    db_session.add(c1)
    db_session.commit()

    c2 = StudyConsistency(user_id=user.id)
    db_session.add(c2)

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_study_consistency_tracks_streaks(db_session: Session) -> None:
    user = _make_user(db_session)

    consistency = StudyConsistency(
        user_id=user.id,
        current_streak=5,
        longest_streak=12,
        total_consistent_days=45,
        last_qualifying_date=date(2025, 6, 15),
    )
    db_session.add(consistency)
    db_session.commit()
    db_session.refresh(consistency)

    assert consistency.current_streak == 5
    assert consistency.longest_streak == 12
    assert consistency.total_consistent_days == 45
    assert consistency.last_qualifying_date == date(2025, 6, 15)
