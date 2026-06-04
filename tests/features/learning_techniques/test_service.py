"""Service-layer tests for LearningTechniquesService.

Tests business logic with mocked repositories.
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.learning_techniques.service import LearningTechniquesService


def _make_service(**overrides) -> LearningTechniquesService:
    defaults = dict(
        note_repo=MagicMock(),
        reflection_repo=MagicMock(),
        recall_repo=MagicMock(),
        goodnight_repo=MagicMock(),
        session_reflection_repo=MagicMock(),
        challenge_repo=MagicMock(),
        question_repo=MagicMock(),
    )
    defaults.update(overrides)
    return LearningTechniquesService(**defaults)


def _make_mock_question(id=1, correct_answer="proportion", stem="What is a ratio?", difficulty="HARD", is_active=True):
    q = MagicMock()
    q.id = id
    q.correct_answer = correct_answer
    q.stem = stem
    q.difficulty = difficulty
    q.is_active = is_active
    q.subtopic_id = 1
    return q


# ── Elaborative Interrogation ─────────────────────────────────────────────────


def test_create_personal_note_calls_repo():
    note_repo = MagicMock()
    mock_note = MagicMock()
    mock_note.id = 1
    mock_note.question_id = 42
    mock_note.note_text = "My explanation"
    mock_note.created_at = datetime.utcnow()
    note_repo.create.return_value = mock_note

    service = _make_service(note_repo=note_repo)
    result = service.create_personal_note(user_id=1, question_id=42, note_text="My explanation")

    note_repo.create.assert_called_once_with(user_id=1, question_id=42, note_text="My explanation")
    assert result.question_id == 42
    assert result.note_text == "My explanation"


def test_get_all_notes_returns_list():
    note_repo = MagicMock()
    mock_note = MagicMock()
    mock_note.id = 1
    mock_note.question_id = 42
    mock_note.note_text = "A note"
    mock_note.created_at = datetime.utcnow()
    note_repo.list_by_user.return_value = [mock_note]

    service = _make_service(note_repo=note_repo)
    result = service.get_all_notes(user_id=1)

    assert len(result) == 1
    note_repo.list_by_user.assert_called_once_with(1)


# ── Recall Mode ───────────────────────────────────────────────────────────────


def test_submit_recall_exact_match():
    question_repo = MagicMock()
    recall_repo = MagicMock()
    question_repo.get.return_value = _make_mock_question(correct_answer="proportion")

    service = _make_service(question_repo=question_repo, recall_repo=recall_repo)
    result = service.submit_recall_answer(user_id=1, question_id=1, user_response="proportion")

    assert result.is_correct is True
    assert result.match_type == "exact"
    recall_repo.create.assert_called_once()


def test_submit_recall_fuzzy_match():
    question_repo = MagicMock()
    recall_repo = MagicMock()
    question_repo.get.return_value = _make_mock_question(correct_answer="proportion")

    service = _make_service(question_repo=question_repo, recall_repo=recall_repo)
    result = service.submit_recall_answer(user_id=1, question_id=1, user_response="proporton")

    assert result.is_correct is True
    assert result.match_type == "fuzzy"


def test_submit_recall_needs_review():
    question_repo = MagicMock()
    recall_repo = MagicMock()
    question_repo.get.return_value = _make_mock_question(correct_answer="proportion")

    service = _make_service(question_repo=question_repo, recall_repo=recall_repo)
    result = service.submit_recall_answer(user_id=1, question_id=1, user_response="completely wrong")

    assert result.is_correct is None
    assert result.match_type == "needs_review"


def test_submit_recall_question_not_found_raises_404():
    question_repo = MagicMock()
    question_repo.get.return_value = None

    service = _make_service(question_repo=question_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.submit_recall_answer(user_id=1, question_id=999, user_response="proportion")
    assert exc_info.value.status_code == 404


# ── Metacognitive Reflection ──────────────────────────────────────────────────


def test_create_session_reflection_persists():
    session_reflection_repo = MagicMock()
    mock_reflection = MagicMock()
    mock_reflection.id = 1
    mock_reflection.session_date = datetime.utcnow()
    mock_reflection.hardest_item_id = 5
    mock_reflection.confidence_rating = 3
    mock_reflection.review_note = None
    mock_reflection.created_at = datetime.utcnow()
    session_reflection_repo.create.return_value = mock_reflection

    service = _make_service(session_reflection_repo=session_reflection_repo)
    result = service.create_session_reflection(
        user_id=1,
        session_date=datetime.utcnow(),
        hardest_item_id=5,
        confidence_rating=3,
        review_note=None,
    )

    session_reflection_repo.create.assert_called_once()
    assert result.confidence_rating == 3


# ── Productive Failure ────────────────────────────────────────────────────────


def test_submit_challenge_attempt_no_hard_questions_raises_422():
    question_repo = MagicMock()
    question_repo.list_active_passing_quality_gate.return_value = []

    service = _make_service(question_repo=question_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.submit_challenge_attempt(user_id=1, subtopic_id=1, answer="test")
    assert exc_info.value.status_code == 422


def test_submit_challenge_attempt_correct_answer():
    question_repo = MagicMock()
    challenge_repo = MagicMock()

    hard_q = _make_mock_question(correct_answer="proportion", difficulty="HARD")
    question_repo.list_active_passing_quality_gate.return_value = [hard_q]

    mock_attempt = MagicMock()
    mock_attempt.id = 1
    challenge_repo.create.return_value = mock_attempt

    service = _make_service(question_repo=question_repo, challenge_repo=challenge_repo)
    result = service.submit_challenge_attempt(user_id=1, subtopic_id=1, answer="proportion")

    assert result.is_correct is True
    assert "already have a strong grasp" in result.message


def test_submit_challenge_attempt_wrong_answer_normalizing_message():
    question_repo = MagicMock()
    challenge_repo = MagicMock()

    hard_q = _make_mock_question(correct_answer="proportion", difficulty="HARD")
    question_repo.list_active_passing_quality_gate.return_value = [hard_q]

    mock_attempt = MagicMock()
    mock_attempt.id = 1
    challenge_repo.create.return_value = mock_attempt

    service = _make_service(question_repo=question_repo, challenge_repo=challenge_repo)
    result = service.submit_challenge_attempt(user_id=1, subtopic_id=1, answer="wrong answer")

    assert result.is_correct is False
    # Failure-normalizing message should mention retention/learning
    assert "retention" in result.message or "expected" in result.message


def test_submit_challenge_retest_not_found_raises_404():
    challenge_repo = MagicMock()
    challenge_repo.get.return_value = None

    service = _make_service(challenge_repo=challenge_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.submit_challenge_retest(user_id=1, challenge_id=999, answer="proportion")
    assert exc_info.value.status_code == 404


def test_submit_challenge_retest_productive_failure_success():
    question_repo = MagicMock()
    challenge_repo = MagicMock()

    mock_attempt = MagicMock()
    mock_attempt.id = 1
    mock_attempt.question_id = 1
    mock_attempt.pre_lesson_correct = False  # Failed before lesson

    updated_attempt = MagicMock()
    updated_attempt.id = 1
    updated_attempt.pre_lesson_correct = False
    updated_attempt.post_lesson_correct = True
    updated_attempt.is_productive_failure_success = True

    challenge_repo.get.return_value = mock_attempt
    challenge_repo.update_retest.return_value = updated_attempt
    question_repo.get.return_value = _make_mock_question(correct_answer="proportion")

    service = _make_service(question_repo=question_repo, challenge_repo=challenge_repo)
    result = service.submit_challenge_retest(user_id=1, challenge_id=1, answer="proportion")

    assert result.is_productive_failure_success is True
    assert "productive failure" in result.message.lower()


# ── Goodnight Review ──────────────────────────────────────────────────────────


def test_get_goodnight_review_returns_session():
    service = _make_service()
    result = service.get_goodnight_review(user_id=1)
    assert result.items == []
    assert result.estimated_minutes == 0


def test_complete_goodnight_review_returns_interval_bonus():
    service = _make_service()
    result = service.complete_goodnight_review(user_id=1)
    assert result["interval_bonus"] == 1.2
    assert result["status"] == "completed"
