"""Service tests for the tutor feature — mocked repository."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.features.content.models import Question
from app.features.content.repository import (
    LessonRepository,
    QuestionRepository,
    SubtopicRepository,
)
from app.features.mastery.repository import MasteryRepository
from app.features.tutor.algorithms.chat_models import ChatResult
from app.features.tutor.algorithms.cross_lesson_registry import CrossLessonRegistry
from app.features.tutor.models import TutorInteraction
from app.features.tutor.repository import TutorRepository
from app.features.tutor.service import TutorService


def _make_question(**kwargs) -> Question:
    defaults = {
        "id": 1,
        "subtopic_id": 10,
        "topic_id": 5,
        "module_id": 2,
        "category": "PROFESSIONAL",
        "level_scope": "SUBTOPIC",
        "stem": "What is the capital of the Philippines?",
        "options": ["Manila", "Cebu", "Davao", "Quezon City"],
        "correct_answer": "Manila",
        "explanation": "Manila is the capital city of the Philippines.",
        "difficulty": "EASY",
        "qtype": "MULTIPLE_CHOICE",
        "is_active": True,
    }
    defaults.update(kwargs)
    q = MagicMock(spec=Question)
    for k, v in defaults.items():
        setattr(q, k, v)
    return q


def _make_interaction(**kwargs) -> TutorInteraction:
    defaults = {
        "id": 1,
        "user_id": 1,
        "question_id": 1,
        "subtopic_id": 10,
        "interaction_type": "explain_answer",
        "request_context": None,
        "response_text": "test response",
        "helpful": None,
    }
    defaults.update(kwargs)
    obj = MagicMock(spec=TutorInteraction)
    for k, v in defaults.items():
        setattr(obj, k, v)
    return obj


@pytest.fixture
def mock_tutor_repo() -> MagicMock:
    return MagicMock(spec=TutorRepository)


@pytest.fixture
def mock_question_repo() -> MagicMock:
    return MagicMock(spec=QuestionRepository)


@pytest.fixture
def mock_subtopic_repo() -> MagicMock:
    return MagicMock(spec=SubtopicRepository)


@pytest.fixture
def service(mock_tutor_repo, mock_question_repo, mock_subtopic_repo) -> TutorService:
    return TutorService(
        tutor_repo=mock_tutor_repo,
        question_repo=mock_question_repo,
        subtopic_repo=mock_subtopic_repo,
    )


def test_explain_returns_response(service, mock_question_repo, mock_tutor_repo):
    question = _make_question()
    mock_question_repo.get.return_value = question
    mock_tutor_repo.create_interaction.return_value = _make_interaction(
        interaction_type="explain_answer"
    )

    result = service.explain(user_id=1, question_id=1, selected_answer="Cebu")

    assert result.interaction_type == "explain_answer"
    assert result.interaction_id == 1
    mock_question_repo.get.assert_called_once_with(1)


def test_explain_raises_404_when_question_missing(service, mock_question_repo):
    mock_question_repo.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.explain(user_id=1, question_id=999)
    assert exc_info.value.status_code == 404


def test_hint_returns_response(service, mock_question_repo, mock_tutor_repo):
    question = _make_question()
    mock_question_repo.get.return_value = question
    mock_tutor_repo.create_interaction.return_value = _make_interaction(
        interaction_type="hint"
    )

    result = service.hint(user_id=1, question_id=1)
    assert result.interaction_type == "hint"


def test_step_by_step_returns_steps(service, mock_question_repo, mock_tutor_repo):
    question = _make_question()
    mock_question_repo.get.return_value = question
    mock_tutor_repo.create_interaction.return_value = _make_interaction(
        interaction_type="step_by_step"
    )

    result = service.step_by_step_explain(user_id=1, question_id=1)
    assert result.interaction_id == 1
    assert isinstance(result.steps, list)
    assert len(result.steps) > 0


def test_similar_question_returns_data(service, mock_question_repo, mock_tutor_repo):
    question = _make_question()
    mock_question_repo.get.return_value = question
    mock_tutor_repo.create_interaction.return_value = _make_interaction(
        interaction_type="similar_question"
    )

    result = service.similar_question(user_id=1, question_id=1)
    assert result.interaction_id == 1
    assert result.correct_answer == "Manila"


def test_rate_interaction_raises_404_when_missing(service, mock_tutor_repo):
    mock_tutor_repo.rate_interaction.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        service.rate_interaction(999, True)
    assert exc_info.value.status_code == 404


def test_rate_interaction_success(service, mock_tutor_repo):
    mock_tutor_repo.rate_interaction.return_value = _make_interaction(helpful=True)
    # Should not raise
    service.rate_interaction(1, True)
    mock_tutor_repo.rate_interaction.assert_called_once_with(1, True)


# ---------------------------------------------------------------------------
# Lesson Chat Service Tests (Task 14.1)
# ---------------------------------------------------------------------------


def _make_lesson_mock(**kwargs):
    """Create a mock Lesson object with sensible defaults."""
    from app.features.content.models import Lesson

    defaults = {
        "id": 1,
        "subtopic_id": 10,
        "content_json": {
            "title": "Test Lesson",
            "sections": [
                {"heading": "Intro", "body": "Introduction to the topic."}
            ],
            "key_takeaways": ["concept_a", "concept_b"],
        },
    }
    defaults.update(kwargs)
    lesson = MagicMock(spec=Lesson)
    for k, v in defaults.items():
        setattr(lesson, k, v)
    return lesson


def _make_mastery_mock(**kwargs):
    """Create a mock UserSubtopicMastery object."""
    from app.features.mastery.models import UserSubtopicMastery

    defaults = {
        "id": 1,
        "user_id": 1,
        "subtopic_id": 10,
        "mastery_score": 0.5,
        "mastery_level": "FAMILIAR",
        "total_attempts": 10,
        "correct_attempts": 5,
    }
    defaults.update(kwargs)
    obj = MagicMock(spec=UserSubtopicMastery)
    for k, v in defaults.items():
        setattr(obj, k, v)
    return obj


@pytest.fixture
def mock_lesson_repo() -> MagicMock:
    return MagicMock(spec=LessonRepository)


@pytest.fixture
def mock_mastery_repo() -> MagicMock:
    return MagicMock(spec=MasteryRepository)


@pytest.fixture
def mock_cross_lesson_registry() -> MagicMock:
    return MagicMock(spec=CrossLessonRegistry)


@pytest.fixture
def chat_service(
    mock_tutor_repo,
    mock_question_repo,
    mock_subtopic_repo,
    mock_lesson_repo,
    mock_mastery_repo,
    mock_cross_lesson_registry,
) -> TutorService:
    """TutorService wired with all repositories for lesson chat tests."""
    return TutorService(
        tutor_repo=mock_tutor_repo,
        question_repo=mock_question_repo,
        subtopic_repo=mock_subtopic_repo,
        lesson_repo=mock_lesson_repo,
        mastery_repo=mock_mastery_repo,
        cross_lesson_registry=mock_cross_lesson_registry,
    )


class TestLessonChatHappyPath:
    """Req 5.7, 7.4 — happy path with mastery data and valid context."""

    @patch("app.features.tutor.service.generate_chat_response")
    def test_returns_response_with_updated_context(
        self,
        mock_engine,
        chat_service,
        mock_lesson_repo,
        mock_mastery_repo,
        mock_tutor_repo,
    ):
        mock_lesson_repo.get_by_subtopic_id.return_value = _make_lesson_mock()
        mock_mastery_repo.get_by_user_and_subtopic.return_value = _make_mastery_mock(
            mastery_score=0.5, mastery_level="FAMILIAR"
        )
        mock_engine.return_value = ChatResult(
            response_text="Here is a detailed explanation.",
            detected_intent="explain_section",
            context_json={"schema_version": 1, "exchanges": [{"msg": "hi"}]},
            reasoning_mode="ALGEBRA",
            reasoning_summary="Reasoning mode: ALGEBRA",
        )
        mock_tutor_repo.create_interaction.return_value = _make_interaction(
            id=42, interaction_type="lesson_chat"
        )

        result = chat_service.lesson_chat(
            user_id=1,
            subtopic_id=10,
            message="Explain this section",
            active_section_index=0,
            context_json={"schema_version": 1, "exchanges": []},
            reasoning_context={
                "mode": "ALGEBRA",
                "math_expression": "2x + 4 = 10",
            },
        )

        assert result.interaction_id == 42
        assert result.response_text == "Here is a detailed explanation."
        assert result.detected_intent == "explain_section"
        assert result.reasoning_mode == "ALGEBRA"
        assert result.reasoning_summary == "Reasoning mode: ALGEBRA"
        assert result.context_json == {
            "schema_version": 1,
            "exchanges": [{"msg": "hi"}],
        }
        # Engine was called with mastery data
        mock_engine.assert_called_once()
        call_kwargs = mock_engine.call_args[1]
        assert call_kwargs["mastery_score"] == 0.5
        assert call_kwargs["mastery_level"] == "FAMILIAR"
        assert call_kwargs["reasoning_context"] == {
            "mode": "ALGEBRA",
            "math_expression": "2x + 4 = 10",
        }


class TestLessonChatNoMastery:
    """Req 5.7 — no mastery data defaults to STANDARD complexity."""

    @patch("app.features.tutor.service.generate_chat_response")
    def test_no_mastery_passes_none_to_engine(
        self,
        mock_engine,
        chat_service,
        mock_lesson_repo,
        mock_mastery_repo,
        mock_tutor_repo,
    ):
        mock_lesson_repo.get_by_subtopic_id.return_value = _make_lesson_mock()
        mock_mastery_repo.get_by_user_and_subtopic.return_value = None
        mock_engine.return_value = ChatResult(
            response_text="Standard explanation.",
            detected_intent="explain_section",
            context_json={"schema_version": 1},
        )
        mock_tutor_repo.create_interaction.return_value = _make_interaction(
            id=50, interaction_type="lesson_chat"
        )

        result = chat_service.lesson_chat(
            user_id=1,
            subtopic_id=10,
            message="What is this?",
        )

        assert result.interaction_id == 50
        assert result.detected_intent == "explain_section"
        # Engine receives None for mastery → defaults to STANDARD internally
        call_kwargs = mock_engine.call_args[1]
        assert call_kwargs["mastery_score"] is None
        assert call_kwargs["mastery_level"] is None


class TestLessonChatMalformedContext:
    """Req 7.4 — malformed context_json starts fresh (no crash)."""

    @patch("app.features.tutor.service.generate_chat_response")
    def test_malformed_context_does_not_crash(
        self,
        mock_engine,
        chat_service,
        mock_lesson_repo,
        mock_mastery_repo,
        mock_tutor_repo,
    ):
        mock_lesson_repo.get_by_subtopic_id.return_value = _make_lesson_mock()
        mock_mastery_repo.get_by_user_and_subtopic.return_value = None
        # Engine handles malformed context gracefully and returns fresh context
        mock_engine.return_value = ChatResult(
            response_text="Fresh start response.",
            detected_intent="greeting",
            context_json={"schema_version": 1, "exchanges": []},
        )
        mock_tutor_repo.create_interaction.return_value = _make_interaction(
            id=60, interaction_type="lesson_chat"
        )

        # Pass garbled context_json — service should not crash
        result = chat_service.lesson_chat(
            user_id=1,
            subtopic_id=10,
            message="Hello",
            context_json={"garbage": True, "not_valid": [1, 2, 3]},
        )

        assert result.interaction_id == 60
        assert result.response_text == "Fresh start response."
        # The malformed dict was passed through to the engine (engine handles it)
        call_kwargs = mock_engine.call_args[1]
        assert call_kwargs["context_json"] == {
            "garbage": True,
            "not_valid": [1, 2, 3],
        }


class TestLessonChatEngineException:
    """Req 7.4 — engine exception caught and fallback response returned."""

    @patch("app.features.tutor.service.generate_chat_response")
    def test_engine_exception_returns_fallback(
        self,
        mock_engine,
        chat_service,
        mock_lesson_repo,
        mock_mastery_repo,
        mock_tutor_repo,
    ):
        mock_lesson_repo.get_by_subtopic_id.return_value = _make_lesson_mock()
        mock_mastery_repo.get_by_user_and_subtopic.return_value = _make_mastery_mock()
        mock_engine.side_effect = RuntimeError("Unexpected engine crash")
        mock_tutor_repo.create_interaction.return_value = _make_interaction(
            id=70, interaction_type="lesson_chat"
        )

        result = chat_service.lesson_chat(
            user_id=1,
            subtopic_id=10,
            message="Explain this",
            context_json={"schema_version": 1},
        )

        assert result.interaction_id == 70
        assert result.detected_intent == "fallback"
        assert "trouble processing" in result.response_text
        # context_json should be the original or empty dict on failure
        assert result.context_json == {"schema_version": 1}
