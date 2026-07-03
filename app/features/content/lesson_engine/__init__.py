"""Lesson parsing engine for portfolioOS.

The lesson engine turns Markdown into a semantic AST, validates the result,
and compiles it into the lesson content JSON consumed by the rest of the app.
"""

from __future__ import annotations

from .ast import LessonBlockNode, LessonDocumentAst, LessonSectionNode, ValidationIssue
from .compiler import compile_lesson_model
from .parser import MarkdownLessonParser, parse_lesson_markdown
from .validation import validate_lesson_document

__all__ = [
    "LessonBlockNode",
    "LessonDocumentAst",
    "LessonSectionNode",
    "MarkdownLessonParser",
    "ValidationIssue",
    "compile_lesson_model",
    "parse_lesson_markdown",
    "validate_lesson_document",
]
