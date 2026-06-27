"""Pydantic request/response schemas for the tutor feature."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TutorReasoningMode(str, Enum):
    """Structured reasoning mode for math and graph-heavy prompts."""

    TEXT = "TEXT"
    ARITHMETIC = "ARITHMETIC"
    ALGEBRA = "ALGEBRA"
    LOGICAL_REASONING = "LOGICAL_REASONING"
    ABSTRACT_PATTERN = "ABSTRACT_PATTERN"
    GRAPH_INTERPRETATION = "GRAPH_INTERPRETATION"
    TABLE_INTERPRETATION = "TABLE_INTERPRETATION"
    FALLBACK = "FALLBACK"


class GraphAxis(BaseModel):
    """Axis metadata for graph-backed tutor prompts."""

    label: str = Field(default="")
    unit: str | None = None


class GraphSeriesPoint(BaseModel):
    """One point in a graph series."""

    x: float | int | str
    y: float | int | str


class GraphSeries(BaseModel):
    """A named graph series or chart line/bar group."""

    name: str = Field(default="")
    points: list[GraphSeriesPoint] = Field(default_factory=list)


class GraphContext(BaseModel):
    """Structured chart or graph context for tutor reasoning."""

    graph_type: str = Field(default="")
    title: str = Field(default="")
    x_axis: GraphAxis = Field(default_factory=GraphAxis)
    y_axis: GraphAxis = Field(default_factory=GraphAxis)
    legend: list[str] = Field(default_factory=list)
    series: list[GraphSeries] = Field(default_factory=list)
    table_rows: list[list[str]] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    highlighted_points: list[str] = Field(default_factory=list)
    source_text: str = Field(default="")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ReasoningContext(BaseModel):
    """Optional structured context for math and graph reasoning."""

    mode: TutorReasoningMode | None = None
    prompt_type: str | None = None
    question_text: str | None = None
    math_expression: str | None = None
    graph_context: GraphContext | None = None
    answer_choices: list[str] = Field(default_factory=list)
    notes: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class TutorRequest(BaseModel):
    """Request body for tutor explain/simplify/hint/step-by-step."""

    question_id: int
    selected_answer: str | None = None
    reasoning_context: ReasoningContext | None = None


class TutorResponse(BaseModel):
    """Response for text-based tutor interactions."""

    interaction_id: int
    response_text: str
    interaction_type: str
    reasoning_mode: TutorReasoningMode | None = None
    reasoning_summary: str | None = None


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
    context_json: dict[str, Any] | None = None
    reasoning_context: ReasoningContext | None = None
    # Deprecated: kept for backward compatibility, ignored if context_json present
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class LessonChatResponse(BaseModel):
    """Response from the lesson chatbot."""

    interaction_id: int
    response_text: str
    detected_intent: str
    context_json: dict[str, Any] = Field(default_factory=dict)
    reasoning_mode: TutorReasoningMode | None = None
    reasoning_summary: str | None = None
