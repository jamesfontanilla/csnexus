"""Repository-layer tests for PretestRepository (real DB, no mocks)."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from app.features.content.models import Module, Question, Subtopic, Topic
from app.features.users.models import User
from app.features.pretesting.models import PretestAttempt
from app.features.pretesting.repository import PretestRepository


# ---------------------------------------------------------------------------
# Seed helpers
# ---------------------------------------------------------------------------


def _seed_user(db: Session, email: str = "pretest@cse.local") -> User:
    user = User(
        email=email,
        display_name="Test User",
        age=25,
        password_hash="x",
        role="LEARNER",
        account_state="VERIFIED",
        category="PROFESSIONAL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_subtopic(db: Session) -> Subtopic:
    module = Module(title="M", slug="m-pretest", order_index=1, category="PROFESSIONAL")
    db.add(module)
    db.flush()
    topic = Topic(title="T", slug="t-pretest", order_index=1, module_id=module.id)
    db.add(topic)
    db.flush()
    subtopic = Subtopic(title="S", slug="s-pretest", order_index=1, topic_id=topic.id)
    db.add(subtopic)
    db.commit()
    db.refresh(subtopic)
    return subtopic


def _make_attempt(user_id: int, subtopic_id: int, score: float = 60.0) -> PretestAttempt:
    return PretestAttempt(
        user_id=user_id,
        subtopic_id=subtopic_id,
        questions=[{"question_id": 1, "correct_answer": "A"}],
        score=score,
        total_questions=1,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_create_and_retrieve_pretest(db_session: Session):
    user = _seed_user(db_session)
    subtopic = _seed_subtopic(db_session)
    repo = PretestRepository(db_session)

    attempt = _make_attempt(user.id, subtopic.id, score=40.0)
    created = repo.create(attempt)

    assert created.id is not None
    assert created.user_id == user.id
    assert created.subtopic_id == subtopic.id
    assert created.score == 40.0

    fetched = repo.get(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.score == 40.0


def test_get_nonexistent_returns_none(db_session: Session):
    repo = PretestRepository(db_session)
    result = repo.get(9999)
    assert result is None


def test_get_by_user_and_subtopic(db_session: Session):
    user = _seed_user(db_session)
    subtopic = _seed_subtopic(db_session)
    repo = PretestRepository(db_session)

    attempt = _make_attempt(user.id, subtopic.id, score=55.0)
    repo.create(attempt)

    fetched = repo.get_by_user_and_subtopic(user.id, subtopic.id)
    assert fetched is not None
    assert fetched.user_id == user.id
    assert fetched.subtopic_id == subtopic.id
    assert fetched.score == 55.0


def test_get_by_user_and_subtopic_returns_most_recent(db_session: Session):
    """When two pretests exist for the same user+subtopic, returns the latest by id."""
    user = _seed_user(db_session, email="recent@cse.local")
    subtopic = _seed_subtopic(db_session)
    repo = PretestRepository(db_session)

    repo.create(_make_attempt(user.id, subtopic.id, score=30.0))
    repo.create(_make_attempt(user.id, subtopic.id, score=70.0))

    fetched = repo.get_by_user_and_subtopic(user.id, subtopic.id)
    assert fetched is not None
    assert fetched.score == 70.0


def test_get_by_user_and_subtopic_wrong_user_returns_none(db_session: Session):
    user = _seed_user(db_session)
    subtopic = _seed_subtopic(db_session)
    repo = PretestRepository(db_session)

    repo.create(_make_attempt(user.id, subtopic.id))

    result = repo.get_by_user_and_subtopic(user_id=9999, subtopic_id=subtopic.id)
    assert result is None


def test_has_pretest_returns_true_when_exists(db_session: Session):
    user = _seed_user(db_session, email="has@cse.local")
    subtopic = _seed_subtopic(db_session)
    repo = PretestRepository(db_session)

    repo.create(_make_attempt(user.id, subtopic.id))

    assert repo.has_pretest(user.id, subtopic.id) is True


def test_has_pretest_returns_false_when_absent(db_session: Session):
    user = _seed_user(db_session, email="absent@cse.local")
    subtopic = _seed_subtopic(db_session)
    repo = PretestRepository(db_session)

    assert repo.has_pretest(user.id, subtopic.id) is False
