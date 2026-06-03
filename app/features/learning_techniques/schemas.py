"""Pydantic schemas for learning technique extensions.

Covers: Elaborative Interrogation, Recall Mode, Sleep-Aware Review,
Metacognitive Reflection, Productive Failure.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


# ─── Elaborative Interrogation ───────────────────────────────────────────────


class PersonalNoteCreate(BaseModel):
    """Request to create a personal note on a question."""

    note_text: str = Field(..., min_length=1, max_length=500)


class PersonalNoteResponse(BaseModel):
    """Response for a personal note."""

    id: int
    question_id: int
    note_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LessonReflectionCreate(BaseModel):
    """Request to create a lesson reflection."""

    section_index: int = Field(default=0, ge=0)
    reflection_text: str = Field(..., min_length=1, max_length=2000)


class LessonReflectionResponse(BaseModel):
    """Response for a lesson reflection."""

    id: int
    lesson_id: int
    section_index: int
    reflection_text: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Recall Mode ─────────────────────────────────────────────────────────────


class RecallAnswerRequest(BaseModel):
    """Request to submit a recall-mode answer."""

    user_response: str = Field(..., min_length=1, max_length=500)


class RecallAnswerResponse(BaseModel):
    """Response after grading a recall answer."""

    question_id: int
    is_correct: bool | None  # None means "needs_review"
    match_type: str  # "exact", "fuzzy", "needs_review"
    correct_answer: str
    user_response: str


# ─── Sleep-Aware Review ──────────────────────────────────────────────────────


class GoodnightSessionItem(BaseModel):
    """A single item in the goodnight review session."""

    question_id: int
    stem: str
    correct_answer: str
    confidence: float  # Lower = appeared in session


class GoodnightSessionResponse(BaseModel):
    """Response for GET /v1/queue/goodnight."""

    items: list[GoodnightSessionItem] = Field(..., max_length=10)
    estimated_minutes: int


class BedtimePreferenceRequest(BaseModel):
    """Request to set bedtime preference."""

    bedtime: str = Field(
        ..., pattern=r"^\d{2}:\d{2}$", description="HH:MM format, e.g. '22:00'"
    )


# ─── Metacognitive Reflection ────────────────────────────────────────────────


class SessionReflectionCreate(BaseModel):
    """Request to submit a post-session reflection."""

    hardest_item_id: int | None = None
    confidence_rating: int = Field(..., ge=1, le=5)
    review_note: str | None = Field(None, max_length=1000)


class SessionReflectionResponse(BaseModel):
    """Response for a session reflection."""

    id: int
    session_date: datetime
    hardest_item_id: int | None
    confidence_rating: int
    review_note: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Productive Failure ──────────────────────────────────────────────────────


class ChallengeAttemptRequest(BaseModel):
    """Request to submit a pre-lesson challenge answer."""

    answer: str = Field(..., min_length=1, max_length=500)


class ChallengeAttemptResponse(BaseModel):
    """Response after submitting a challenge attempt."""

    challenge_id: int
    subtopic_id: int
    question_stem: str
    is_correct: bool
    message: str = Field(
        ...,
        description="Failure-normalizing framing message.",
    )


class ChallengeRetestRequest(BaseModel):
    """Request to submit a post-lesson retest."""

    answer: str = Field(..., min_length=1, max_length=500)


class ChallengeComparisonResponse(BaseModel):
    """Before/after comparison for a productive failure challenge."""

    challenge_id: int
    pre_lesson_correct: bool | None
    post_lesson_correct: bool | None
    is_productive_failure_success: bool
    message: str
