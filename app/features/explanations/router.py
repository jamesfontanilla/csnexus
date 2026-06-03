"""FastAPI router for /v1/explanations/* endpoints.

Exposes inline question explanation retrieval, bulk prefetch for offline
caching, and AI Tutor escalation. Supports conditional requests via
If-None-Match/ETag for cache freshness (Requirement 9.3).

Validates: Requirements 7.1, 7.5, 7.7, 8.1, 8.3, 9.2, 9.3
"""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Header, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.common.deps import get_current_user
from app.features.explanations.repository import ExplanationRepository
from app.features.explanations.schemas import (
    BulkExplanationRequest,
    BulkExplanationResponse,
    ExplanationResponse,
)
from app.features.explanations.service import ExplanationService
from app.features.tutor.algorithms.cross_lesson_registry import CrossLessonRegistry
from app.features.tutor.repository import TutorRepository
from app.features.tutor.service import TutorService
from app.features.content.repository import (
    LessonRepository,
    QuestionRepository,
    SubtopicRepository,
)
from app.features.mastery.repository import MasteryRepository
from app.features.users.models import User
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/v1/explanations", tags=["explanations"])


# ---------------------------------------------------------------------------
# Dependency injection
# ---------------------------------------------------------------------------


def get_explanation_service(
    db: Session = Depends(get_db),
) -> ExplanationService:
    """Construct ExplanationService for the request.

    Wires ExplanationRepository and TutorService so the escalation
    path has access to the tutor's explain() method.
    """
    tutor_service = TutorService(
        tutor_repo=TutorRepository(db=db),
        question_repo=QuestionRepository(db=db),
        subtopic_repo=SubtopicRepository(db=db),
        lesson_repo=LessonRepository(db=db),
        mastery_repo=MasteryRepository(db=db),
    )
    return ExplanationService(
        explanation_repo=ExplanationRepository(db=db),
        tutor_service=tutor_service,
    )


# ---------------------------------------------------------------------------
# Helper: serialize ORM model → response schema
# ---------------------------------------------------------------------------


def _serialize_explanation(explanation) -> ExplanationResponse:
    """Convert a QuestionExplanation ORM instance to ExplanationResponse."""
    related = json.loads(explanation.related_subtopics)
    # Handle concrete_examples: can be None, a JSON string, or already parsed list
    concrete = None
    raw = explanation.concrete_examples
    if isinstance(raw, str):
        concrete = json.loads(raw)
    elif isinstance(raw, list):
        concrete = raw
    # Otherwise (None, MagicMock in tests, etc.) → stays None
    return ExplanationResponse(
        explanation_text=explanation.explanation_text,
        key_concept=explanation.key_concept,
        related_subtopics=related,
        cache_version=explanation.cache_version,
        concrete_examples=concrete,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/{question_id}", response_model=ExplanationResponse)
def get_explanation(
    question_id: int,
    response: Response,
    user: User = Depends(get_current_user),
    service: ExplanationService = Depends(get_explanation_service),
    if_none_match: str | None = Header(default=None),
) -> ExplanationResponse | Response:
    """Get explanation for a single question with ETag/conditional request support.

    Returns the explanation with an ETag header set to the cache_version.
    If the client sends If-None-Match matching the current cache_version,
    returns 304 Not Modified (Requirement 9.3).
    """
    explanation = service.get_explanation(question_id)

    if explanation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Explanation not found",
        )

    # Conditional request: check If-None-Match against cache_version
    etag = str(explanation.cache_version)
    if if_none_match is not None and if_none_match == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    # Set ETag header for cache validation
    response.headers["ETag"] = etag

    return _serialize_explanation(explanation)


@router.post("/bulk", response_model=BulkExplanationResponse)
def get_bulk_explanations(
    payload: BulkExplanationRequest,
    user: User = Depends(get_current_user),
    service: ExplanationService = Depends(get_explanation_service),
) -> BulkExplanationResponse:
    """Bulk fetch explanations for offline caching (Requirement 7.5, 9.2).

    Accepts 1-50 question IDs. Returns explanations in the same order as
    the request. Questions without stored explanations return None.
    """
    explanation_map = service.get_bulk_explanations(payload.question_ids)

    explanations: list[ExplanationResponse | None] = []
    for qid in payload.question_ids:
        exp = explanation_map.get(qid)
        if exp is None:
            explanations.append(None)
        else:
            explanations.append(_serialize_explanation(exp))

    return BulkExplanationResponse(explanations=explanations)


@router.post("/{question_id}/:escalate")
def escalate_to_tutor(
    question_id: int,
    user: User = Depends(get_current_user),
    service: ExplanationService = Depends(get_explanation_service),
) -> dict:
    """Escalate a question to the AI Tutor for deeper explanation (Requirement 8.1, 8.3).

    Forwards question context to the existing TutorService. Rate-limited
    to 20 escalations per user per day. Returns 429 when limit is exceeded.
    """
    return service.escalate_to_tutor(
        user_id=user.id,
        question_id=question_id,
    )
