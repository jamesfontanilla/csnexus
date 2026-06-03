"""Service tests for the explanations feature — mocked repository.

Tests business logic in isolation per testing-standards.md.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.features.explanations.models import QuestionExplanation
from app.features.explanations.repository import ExplanationRepository
from app.features.explanations.service import ExplanationService, MAX_DAILY_ESCALATIONS
from app.features.tutor.schemas import TutorResponse
from app.features.tutor.service import TutorService


def _make_explanation(**kwargs) -> MagicMock:
    defaults = {
        "id": 1,
        "question_id": 42,
        "explanation_text": "This is a detailed explanation of the answer.",
        "key_concept": "Basic Arithmetic",
        "related_subtopics": "[1, 2, 3]",
        "cache_version": 1,
    }
    defaults.update(kwargs)
    obj = MagicMock(spec=QuestionExplanation)
    for k, v in defaults.items():
        setattr(obj, k, v)
    return obj


@pytest.fixture
def mock_explanation_repo() -> MagicMock:
    return MagicMock(spec=ExplanationRepository)


@pytest.fixture
def mock_tutor_service() -> MagicMock:
    return MagicMock(spec=TutorService)


@pytest.fixture
def service(mock_explanation_repo, mock_tutor_service) -> ExplanationService:
    return ExplanationService(
        explanation_repo=mock_explanation_repo,
        tutor_service=mock_tutor_service,
    )


@pytest.fixture
def service_no_tutor(mock_explanation_repo) -> ExplanationService:
    return ExplanationService(
        explanation_repo=mock_explanation_repo,
        tutor_service=None,
    )


# --- get_explanation tests ---


class TestGetExplanation:
    def test_returns_explanation_when_found(self, service, mock_explanation_repo):
        explanation = _make_explanation(question_id=42)
        mock_explanation_repo.get_by_question_id.return_value = explanation

        result = service.get_explanation(42)

        assert result is explanation
        mock_explanation_repo.get_by_question_id.assert_called_once_with(42)

    def test_returns_none_when_not_found(self, service, mock_explanation_repo):
        mock_explanation_repo.get_by_question_id.return_value = None

        result = service.get_explanation(999)

        assert result is None
        mock_explanation_repo.get_by_question_id.assert_called_once_with(999)


# --- get_bulk_explanations tests ---


class TestGetBulkExplanations:
    def test_returns_all_with_none_for_missing(self, service, mock_explanation_repo):
        exp1 = _make_explanation(question_id=1)
        mock_explanation_repo.get_bulk.return_value = {
            1: exp1,
            2: None,
            3: None,
        }

        result = service.get_bulk_explanations([1, 2, 3])

        assert result[1] is exp1
        assert result[2] is None
        assert result[3] is None
        mock_explanation_repo.get_bulk.assert_called_once_with([1, 2, 3])

    def test_returns_all_found(self, service, mock_explanation_repo):
        exp1 = _make_explanation(question_id=10)
        exp2 = _make_explanation(question_id=20)
        mock_explanation_repo.get_bulk.return_value = {10: exp1, 20: exp2}

        result = service.get_bulk_explanations([10, 20])

        assert result[10] is exp1
        assert result[20] is exp2


# --- escalate_to_tutor tests ---


class TestEscalateToTutor:
    def test_successful_escalation(self, service, mock_tutor_service):
        mock_tutor_service.explain.return_value = TutorResponse(
            interaction_id=99,
            response_text="Here is a deeper explanation.",
            interaction_type="explain_answer",
        )

        result = service.escalate_to_tutor(user_id=1, question_id=42, selected_answer="B")

        assert result["interaction_id"] == 99
        assert result["response_text"] == "Here is a deeper explanation."
        assert result["interaction_type"] == "explain_answer"
        mock_tutor_service.explain.assert_called_once_with(
            user_id=1, question_id=42, selected_answer="B"
        )

    def test_escalation_increments_counter(self, service, mock_tutor_service):
        mock_tutor_service.explain.return_value = TutorResponse(
            interaction_id=1,
            response_text="Explanation",
            interaction_type="explain_answer",
        )

        service.escalate_to_tutor(user_id=1, question_id=1)
        service.escalate_to_tutor(user_id=1, question_id=2)

        assert mock_tutor_service.explain.call_count == 2

    def test_rate_limit_raises_429_after_20_escalations(
        self, service, mock_tutor_service
    ):
        mock_tutor_service.explain.return_value = TutorResponse(
            interaction_id=1,
            response_text="Explanation",
            interaction_type="explain_answer",
        )

        # Exhaust the daily limit
        for i in range(MAX_DAILY_ESCALATIONS):
            service.escalate_to_tutor(user_id=1, question_id=i)

        # The 21st should raise
        with pytest.raises(HTTPException) as exc_info:
            service.escalate_to_tutor(user_id=1, question_id=100)

        assert exc_info.value.status_code == 429

    def test_rate_limit_is_per_user(self, service, mock_tutor_service):
        mock_tutor_service.explain.return_value = TutorResponse(
            interaction_id=1,
            response_text="Explanation",
            interaction_type="explain_answer",
        )

        # User 1 uses all 20
        for i in range(MAX_DAILY_ESCALATIONS):
            service.escalate_to_tutor(user_id=1, question_id=i)

        # User 2 should still be able to escalate
        result = service.escalate_to_tutor(user_id=2, question_id=1)
        assert result["interaction_id"] == 1

    def test_tutor_service_unavailable_raises_503(
        self, service_no_tutor
    ):
        with pytest.raises(HTTPException) as exc_info:
            service_no_tutor.escalate_to_tutor(user_id=1, question_id=42)

        assert exc_info.value.status_code == 503
