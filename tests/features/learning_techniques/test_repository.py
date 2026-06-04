"""Repository-layer tests for learning techniques (real DB, no mocks)."""

from __future__ import annotations

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from app.features.content.models import Module, Question, Subtopic, Topic
from app.features.users.models import User
from app.features.learning_techniques.models import (
    ChallengeAttempt,
    LessonReflection,
    PersonalNote,
    RecallAnswer,
    SessionReflection,
)
from app.features.learning_techniques.repository import (
    ChallengeAttemptRepository,
    LessonReflectionRepository,
    PersonalNoteRepository,
    RecallAnswerRepository,
    SessionReflectionRepository,
)


def _seed_user(db: Session, email: str = "test@cse.local") -> User:
    user = User(
        email=email,
        hashed_password="x",
        is_verified=True,
        role="learner",
        category="PROFESSIONAL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_question(db: Session, subtopic_id: int = 1) -> Question:
    module = Module(title="M", slug="m", description="d", order_index=1, category="PROFESSIONAL")
    db.add(module)
    db.flush()
    topic = Topic(title="T", slug="t", description="d", order_index=1, module_id=module.id)
    db.add(topic)
    db.flush()
    subtopic = Subtopic(title="S", slug="s", description="d", order_index=1, topic_id=topic.id, module_id=module.id)
    db.add(subtopic)
    db.flush()
    question = Question(
        stem="What is a ratio?",
        correct_answer="proportion",
        difficulty="EASY",
        qtype="MULTIPLE_CHOICE",
        subtopic_id=subtopic.id,
        topic_id=topic.id,
        module_id=module.id,
        category="PROFESSIONAL",
        level_scope="PROFESSIONAL",
        is_active=True,
        explanation="A ratio is a comparison.",
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


# ── PersonalNoteRepository ────────────────────────────────────────────────────


def test_create_and_retrieve_personal_note(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = PersonalNoteRepository(db_session)

    note = repo.create(user_id=user.id, question_id=question.id, note_text="My insight")

    assert note.id is not None
    assert note.note_text == "My insight"
    assert note.user_id == user.id


def test_list_personal_notes_by_user(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = PersonalNoteRepository(db_session)

    repo.create(user_id=user.id, question_id=question.id, note_text="Note 1")
    repo.create(user_id=user.id, question_id=question.id, note_text="Note 2")

    notes = repo.list_by_user(user.id)
    assert len(notes) == 2


def test_get_note_for_question_returns_most_recent(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = PersonalNoteRepository(db_session)

    repo.create(user_id=user.id, question_id=question.id, note_text="First")
    repo.create(user_id=user.id, question_id=question.id, note_text="Second")

    note = repo.get_by_user_and_question(user.id, question.id)
    assert note is not None
    assert note.note_text == "Second"


def test_list_notes_empty_for_no_notes(db_session: Session):
    user = _seed_user(db_session)
    repo = PersonalNoteRepository(db_session)
    notes = repo.list_by_user(user.id)
    assert notes == []


# ── RecallAnswerRepository ────────────────────────────────────────────────────


def test_create_recall_answer_exact(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = RecallAnswerRepository(db_session)

    answer = repo.create(
        user_id=user.id,
        question_id=question.id,
        user_response="proportion",
        is_correct=True,
        match_type="exact",
    )

    assert answer.id is not None
    assert answer.is_correct is True
    assert answer.match_type == "exact"


def test_create_recall_answer_needs_review(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = RecallAnswerRepository(db_session)

    answer = repo.create(
        user_id=user.id,
        question_id=question.id,
        user_response="wrong",
        is_correct=None,
        match_type="needs_review",
    )

    assert answer.is_correct is None
    assert answer.match_type == "needs_review"


# ── SessionReflectionRepository ──────────────────────────────────────────────


def test_create_session_reflection(db_session: Session):
    user = _seed_user(db_session)
    repo = SessionReflectionRepository(db_session)

    reflection = repo.create(
        user_id=user.id,
        session_date=datetime.utcnow(),
        hardest_item_id=5,
        confidence_rating=2,
        review_note="Found this hard",
    )

    assert reflection.id is not None
    assert reflection.confidence_rating == 2
    assert reflection.hardest_item_id == 5


def test_list_session_reflections_by_user(db_session: Session):
    user = _seed_user(db_session)
    repo = SessionReflectionRepository(db_session)

    repo.create(user_id=user.id, session_date=datetime.utcnow(), hardest_item_id=1, confidence_rating=3, review_note=None)
    repo.create(user_id=user.id, session_date=datetime.utcnow(), hardest_item_id=2, confidence_rating=4, review_note=None)

    reflections = repo.list_by_user(user.id)
    assert len(reflections) == 2


# ── LessonReflectionRepository ───────────────────────────────────────────────


def test_create_lesson_reflection(db_session: Session):
    user = _seed_user(db_session)
    repo = LessonReflectionRepository(db_session)

    reflection = repo.create(
        user_id=user.id,
        lesson_id=1,
        section_index=2,
        reflection_text="I understand subject-verb agreement now",
    )

    assert reflection.id is not None
    assert reflection.section_index == 2
    assert reflection.lesson_id == 1


# ── ChallengeAttemptRepository ───────────────────────────────────────────────


def test_create_and_update_challenge_attempt(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = ChallengeAttemptRepository(db_session)

    attempt = repo.create(
        user_id=user.id,
        subtopic_id=question.subtopic_id,
        question_id=question.id,
        pre_lesson_answer="wrong",
        pre_lesson_correct=False,
    )

    assert attempt.id is not None
    assert attempt.pre_lesson_correct is False
    assert attempt.post_lesson_correct is None

    updated = repo.update_retest(attempt, post_answer="proportion", post_correct=True)

    assert updated.post_lesson_correct is True
    assert updated.is_productive_failure_success is True


def test_get_challenge_attempt_wrong_user_returns_none(db_session: Session):
    user = _seed_user(db_session)
    question = _seed_question(db_session)
    repo = ChallengeAttemptRepository(db_session)

    attempt = repo.create(
        user_id=user.id,
        subtopic_id=question.subtopic_id,
        question_id=question.id,
        pre_lesson_answer="wrong",
        pre_lesson_correct=False,
    )

    result = repo.get(attempt.id, user_id=9999)
    assert result is None
