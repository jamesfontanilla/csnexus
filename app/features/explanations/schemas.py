"""Pydantic request/response schemas for explanations endpoints.

Validates: Requirements 7.1, 7.5, 7.7
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ExplanationResponse(BaseModel):
    """Response schema for a single question explanation."""

    explanation_text: str = Field(
        ..., min_length=50, max_length=2000, description="Markdown explanation text"
    )
    key_concept: str = Field(
        ..., max_length=100, description="The principle being tested"
    )
    related_subtopics: list[int] = Field(
        ..., max_length=10, description="Subtopic IDs sharing the same concept"
    )
    cache_version: int = Field(
        ..., ge=1, description="Version for cache invalidation"
    )
    concrete_examples: list[str] | None = Field(
        None,
        max_length=3,
        description="Filipino-context concrete examples. 'Think of it like this:' callout.",
    )

    model_config = {"from_attributes": True}


class BulkExplanationRequest(BaseModel):
    """Request schema for bulk explanation retrieval."""

    question_ids: list[int] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Question IDs to fetch explanations for (1-50)",
    )


class BulkExplanationResponse(BaseModel):
    """Response schema for bulk explanation retrieval.

    Each entry is either an ExplanationResponse or None (for questions
    without a stored explanation).
    """

    explanations: list[ExplanationResponse | None]
