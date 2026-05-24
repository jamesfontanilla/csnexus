"""Pydantic request/response schemas for the tutor feature."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TutorRequest(BaseModel):
    """Request body for tutor explain/simplify/hint/step-by-step."""

    question_id: int
    selected_answer: str | None = None


class TutorResponse(BaseModel):
    """Response for text-based tutor interactions."""

    interaction_id: int
    response_text: str
    interaction_type: str


class SimilarQuestionResponse(BaseModel):
    """Response for similar question generation."""

    interaction_id: int
    stem: str
    options: list[str] | None = None
    correct_answer: str
    explanation: str


class StepByStepResponse(BaseModel):
    """Response for step-by-step breakdown."""

    interaction_id: int
    steps: list[str]


class RateRequest(BaseModel):
    """Request body for rating an interaction."""

    helpful: bool


# ---------------------------------------------------------------------------
# Lesson Chat schemas
# ---------------------------------------------------------------------------


class ChatMessage(BaseModel):
    """A single message in the conversation history."""

    role: str = Field(pattern=r"^(user|assistant)$")
    content: str = Field(min_length=1)


class LessonChatRequest(BaseModel):
    """Request body for the lesson chatbot."""

    subtopic_id: int
    message: str = Field(min_length=1, max_length=1000)
    active_section_index: int | None = None
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class LessonChatResponse(BaseModel):
    """Response from the lesson chatbot."""

    interaction_id: int
    response_text: str
    detected_intent: str
