"""Pydantic request/response schemas for pretesting feature.

Requirements: 20.1, 20.3, 20.5
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class PretestQuestion(BaseModel):
    """A single question in a pretest."""

    id: int
    stem: str
    options: list[str]
    key_concept: str


class PretestStartResponse(BaseModel):
    """Response for POST /v1/pretests/{subtopic_id}/start."""

    pretest_id: int
    subtopic_id: int
    questions: list[PretestQuestion]


class PretestAnswer(BaseModel):
    """A single answer submission in a pretest."""

    question_id: int
    selected_answer: str


class PretestSubmitRequest(BaseModel):
    """Request for POST /v1/pretests/{pretest_id}/submit."""

    answers: list[PretestAnswer] = Field(..., min_length=1)


class PretestSubmitResponse(BaseModel):
    """Response after pretest submission."""

    pretest_id: int
    score: float
    total_questions: int
    correct_count: int
    weak_concepts: list[str] = Field(
        default_factory=list,
        description="Key concepts the user got wrong — prioritized for future practice.",
    )


class PretestComparisonResponse(BaseModel):
    """Before/after comparison between pretest and post-lesson quiz."""

    subtopic_id: int
    pretest_score: float
    post_lesson_score: float | None
    improvement: float | None = Field(
        None, description="Percentage point improvement (post - pre)."
    )
    message: str
