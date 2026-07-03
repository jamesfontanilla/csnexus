"""Semantic AST nodes for lesson Markdown."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class LessonBlockNode:
    """A semantic block within a lesson section."""

    kind: str
    content: Any = None
    children: list["LessonBlockNode"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    language: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LessonSectionNode:
    """A semantic section node with nested subsections."""

    kind: str
    title: str
    blocks: list[LessonBlockNode] = field(default_factory=list)
    subsections: list["LessonSectionNode"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    level: int = 0
    word_count: int = 0
    estimated_reading_seconds: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LessonDocumentAst:
    """Top-level lesson AST."""

    title: str
    summary: str = ""
    lead_in_blocks: list[LessonBlockNode] = field(default_factory=list)
    sections: list[LessonSectionNode] = field(default_factory=list)
    learning_objectives: list[str] = field(default_factory=list)
    key_takeaways: list[str] = field(default_factory=list)
    explanations: list[LessonSectionNode] = field(default_factory=list)
    microconcepts: list[LessonSectionNode] = field(default_factory=list)
    worked_examples: list[LessonSectionNode] = field(default_factory=list)
    exam_strategies: list[LessonSectionNode] = field(default_factory=list)
    memory_aids: list[LessonSectionNode] = field(default_factory=list)
    practice_review: list[LessonSectionNode] = field(default_factory=list)
    final_challenge: list[LessonSectionNode] = field(default_factory=list)
    generic_sections: list[LessonSectionNode] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ValidationIssue:
    """A validation warning or error emitted by the lesson engine."""

    code: str
    message: str
    severity: str = "warning"
    section_title: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
