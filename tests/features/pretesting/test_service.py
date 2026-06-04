"""Service-layer tests for PretestService.

Tests business logic in isolation with mocked repositories.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.pretesting.service import PretestService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service(**overrides) -> PretestService:
    defaults = dict(
        pretest_repo=MagicMock(),
        question_repo=MagicMock(),
        subtopic_repo=MagicMock(),
        mastery_repo=MagicMock(),
        progress_repo=MagicMock(),
    )
    defaults.update(overrides)
    return PretestService(**defaults)


def _make_mock_subtopic(id: int = 1, title: str = "Ratios") -> MagicMock:
    s = MagicMock()
    s.id = id
    s.title = title
    return s


def _make_mock_question(
    id: int = 1,
    stem: str = "What is a ratio?",
    correct_answer: str = "A comparison",
    difficulty: str = "easy",
    options: list[str] | None = None,
    explanation: str = "A ratio is a comparison",
) -> MagicMock:
    q = MagicMock()
    q.id = id
    q.stem = stem
    q.correct_answer = correct_answer
    q.difficulty = difficulty
    q.options = options or ["A comparison", "An operation", "A fraction", "A sum"]
    q.explanation = explanation
    return q


def _make_mock_attempt(
    id: int = 10,
    user_id: int = 1,
    subtopic_id: int = 1,
    score: float = 0.0,
    total_questions: int = 3,
    questions: list[dict] | None = None,
) -> MagicMock:
    attempt = MagicMock()
    attempt.id = id
    attempt.user_id = user_id
    attempt.subtopic_id = subtopic_id
    attempt.score = score
    attempt.total_questions = total_questions
    attempt.questions = questions or [
        {"question_id": 1, "correct_answer": "A comparison"},
        {"question_id": 2, "correct_answer": "B"},
        {"question_id": 3, "correct_answer": "C"},
    ]
    return attempt


# ---------------------------------------------------------------------------
# start_pretest
# ---------------------------------------------------------------------------


def test_start_pretest_returns_questions():
    subtopic_repo = MagicMock()
    question_repo = MagicMock()
    progress_repo = MagicMock()
    pretest_repo = MagicMock()

    subtopic_repo.get.return_value = _make_mock_subtopic()
    progress_repo.is_lesson_completed.return_value = False

    questions = [_make_mock_question(id=i) for i in range(1, 6)]
    question_repo.get_by_subtopic.return_value = questions

    persisted_attempt = _make_mock_attempt(total_questions=5)
    pretest_repo.create.return_value = persisted_attempt

    service = _make_service(
        pretest_repo=pretest_repo,
        question_repo=question_repo,
        subtopic_repo=subtopic_repo,
        progress_repo=progress_repo,
    )
    result = service.start_pretest(user_id=1, subtopic_id=1)

    assert result.pretest_id == 10
    assert result.subtopic_id == 1
    assert len(result.questions) >= 3


def test_start_pretest_skips_if_lesson_completed():
    """Req 20.7 — raise 409 when lesson is already completed."""
    subtopic_repo = MagicMock()
    progress_repo = MagicMock()

    subtopic_repo.get.return_value = _make_mock_subtopic()
    progress_repo.is_lesson_completed.return_value = True

    service = _make_service(
        subtopic_repo=subtopic_repo,
        progress_repo=progress_repo,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.start_pretest(user_id=1, subtopic_id=1)

    assert exc_info.value.status_code == 409


def test_start_pretest_subtopic_not_found_raises_404():
    subtopic_repo = MagicMock()
    subtopic_repo.get.return_value = None

    service = _make_service(subtopic_repo=subtopic_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.start_pretest(user_id=1, subtopic_id=999)

    assert exc_info.value.status_code == 404


def test_start_pretest_insufficient_questions_raises_422():
    subtopic_repo = MagicMock()
    question_repo = MagicMock()
    progress_repo = MagicMock()

    subtopic_repo.get.return_value = _make_mock_subtopic()
    progress_repo.is_lesson_completed.return_value = False
    # Only 2 easy/medium questions — not enough
    question_repo.get_by_subtopic.return_value = [
        _make_mock_question(id=1, difficulty="easy"),
        _make_mock_question(id=2, difficulty="medium"),
    ]

    service = _make_service(
        subtopic_repo=subtopic_repo,
        question_repo=question_repo,
        progress_repo=progress_repo,
    )

    with pytest.raises(HTTPException) as exc_info:
        service.start_pretest(user_id=1, subtopic_id=1)

    assert exc_info.value.status_code == 422


# ---------------------------------------------------------------------------
# submit_pretest
# ---------------------------------------------------------------------------


def test_submit_pretest_grades_correctly():
    pretest_repo = MagicMock()
    question_repo = MagicMock()

    stored_questions = [
        {"question_id": 1, "correct_answer": "A"},
        {"question_id": 2, "correct_answer": "B"},
        {"question_id": 3, "correct_answer": "C"},
    ]
    attempt = _make_mock_attempt(questions=stored_questions)
    pretest_repo.get.return_value = attempt
    question_repo.get.return_value = _make_mock_question()

    service = _make_service(
        pretest_repo=pretest_repo,
        question_repo=question_repo,
    )

    answers = [
        {"question_id": 1, "selected_answer": "A"},  # correct
        {"question_id": 2, "selected_answer": "B"},  # correct
        {"question_id": 3, "selected_answer": "X"},  # wrong
    ]
    result = service.submit_pretest(user_id=1, pretest_id=10, answers=answers)

    assert result.correct_count == 2
    assert result.total_questions == 3
    assert abs(result.score - 66.67) < 1.0  # 2/3 * 100


def test_submit_pretest_does_not_affect_mastery():
    """Property 39 — submitting a pretest must NOT update any mastery record."""
    pretest_repo = MagicMock()
    mastery_repo = MagicMock()
    question_repo = MagicMock()

    stored_questions = [{"question_id": 1, "correct_answer": "A"}]
    attempt = _make_mock_attempt(questions=stored_questions)
    pretest_repo.get.return_value = attempt
    question_repo.get.return_value = _make_mock_question()

    service = _make_service(
        pretest_repo=pretest_repo,
        mastery_repo=mastery_repo,
        question_repo=question_repo,
    )

    service.submit_pretest(
        user_id=1,
        pretest_id=10,
        answers=[{"question_id": 1, "selected_answer": "A"}],
    )

    mastery_repo.update.assert_not_called()
    mastery_repo.create.assert_not_called()
    mastery_repo.upsert.assert_not_called() if hasattr(mastery_repo, "upsert") else None


def test_submit_pretest_not_found_raises_404():
    pretest_repo = MagicMock()
    pretest_repo.get.return_value = None

    service = _make_service(pretest_repo=pretest_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.submit_pretest(
            user_id=1,
            pretest_id=999,
            answers=[{"question_id": 1, "selected_answer": "A"}],
        )

    assert exc_info.value.status_code == 404


def test_submit_pretest_wrong_user_raises_404():
    """Accessing another user's pretest raises 404 (no leakage)."""
    pretest_repo = MagicMock()
    attempt = _make_mock_attempt(user_id=99)  # owned by user 99
    pretest_repo.get.return_value = attempt

    service = _make_service(pretest_repo=pretest_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.submit_pretest(
            user_id=1,  # caller is user 1 — mismatch
            pretest_id=10,
            answers=[{"question_id": 1, "selected_answer": "A"}],
        )

    assert exc_info.value.status_code == 404


# ---------------------------------------------------------------------------
# get_comparison
# ---------------------------------------------------------------------------


def test_get_comparison_returns_improvement():
    pretest_repo = MagicMock()
    mastery_repo = MagicMock()

    pretest_attempt = _make_mock_attempt(score=40.0)
    pretest_repo.get_by_user_and_subtopic.return_value = pretest_attempt

    mastery = MagicMock()
    mastery.mastery_score = 0.80  # 80% post-lesson
    mastery_repo.get_by_user_and_subtopic.return_value = mastery

    service = _make_service(
        pretest_repo=pretest_repo,
        mastery_repo=mastery_repo,
    )
    result = service.get_comparison(user_id=1, subtopic_id=1)

    assert result.pretest_score == 40.0
    assert result.post_lesson_score == pytest.approx(80.0)
    assert result.improvement == pytest.approx(40.0)
    assert "improv" in result.message.lower()


def test_get_comparison_no_post_score_returns_message():
    pretest_repo = MagicMock()
    mastery_repo = MagicMock()

    pretest_attempt = _make_mock_attempt(score=50.0)
    pretest_repo.get_by_user_and_subtopic.return_value = pretest_attempt
    mastery_repo.get_by_user_and_subtopic.return_value = None  # no post-lesson data

    service = _make_service(
        pretest_repo=pretest_repo,
        mastery_repo=mastery_repo,
    )
    result = service.get_comparison(user_id=1, subtopic_id=1)

    assert result.post_lesson_score is None
    assert result.improvement is None
    assert "lesson" in result.message.lower()


def test_get_comparison_no_pretest_raises_404():
    pretest_repo = MagicMock()
    pretest_repo.get_by_user_and_subtopic.return_value = None

    service = _make_service(pretest_repo=pretest_repo)

    with pytest.raises(HTTPException) as exc_info:
        service.get_comparison(user_id=1, subtopic_id=1)

    assert exc_info.value.status_code == 404
