"""Validation rules for semantic lesson documents."""

from __future__ import annotations

from typing import Iterable

from .ast import LessonDocumentAst, LessonSectionNode, ValidationIssue


def validate_lesson_document(document: LessonDocumentAst) -> list[ValidationIssue]:
    """Validate the semantic lesson document and return non-fatal issues."""

    issues: list[ValidationIssue] = []

    if not document.title.strip():
        issues.append(
            ValidationIssue(
                code="missing_title",
                message="Lesson is missing a title heading.",
            )
        )

    if not document.explanations:
        issues.append(
            ValidationIssue(
                code="missing_explanations",
                message="Lesson is missing an Explanations section.",
            )
        )

    if document.sections:
        first_kind = document.sections[0].kind
        if first_kind != "explanations":
            issues.append(
                ValidationIssue(
                    code="explanations_not_first",
                    message="Explanations should appear before other major sections.",
                    section_title=document.sections[0].title,
                )
            )

    if document.worked_examples and document.sections:
        first_worked = _first_index(document.sections, "worked_examples")
        first_micro = _first_index(document.sections, "micro_concept")
        if first_micro is not None and first_worked is not None and first_micro > first_worked:
            issues.append(
                ValidationIssue(
                    code="microconcept_after_worked_examples",
                    message="MicroConcept sections should appear before Worked Examples.",
                )
            )

    for section in document.microconcepts:
        if not section.subsections:
            issues.append(
                ValidationIssue(
                    code="microconcept_missing_subsections",
                    message=f"MicroConcept '{section.title}' has no recognized subsections.",
                    section_title=section.title,
                )
            )

    if not document.key_takeaways:
        issues.append(
            ValidationIssue(
                code="missing_key_takeaways",
                message="Lesson should include at least one key takeaway.",
            )
        )

    if not document.summary.strip():
        issues.append(
            ValidationIssue(
                code="missing_summary",
                message="Lesson should include a summary.",
            )
        )

    return issues


def _first_index(sections: list[LessonSectionNode], kind: str) -> int | None:
    for index, section in enumerate(sections):
        if section.kind == kind:
            return index
    return None
