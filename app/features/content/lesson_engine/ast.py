"""Semantic lesson AST helpers.

The parser in ``scripts.parse_lesson`` already turns Markdown into structured
lesson JSON. This module lifts that parsed structure into a semantic tree so
the compiler can reason about educational meaning instead of raw Markdown.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


@dataclass(slots=True)
class LessonAstNode:
    """A semantic node within the lesson AST."""

    kind: str
    title: str = ""
    text: str = ""
    content: Any = None
    children: list["LessonAstNode"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LessonAstSection:
    """A semantic lesson section with nested subsections."""

    title: str
    nodes: list[LessonAstNode] = field(default_factory=list)
    difficulty: list[str] = field(default_factory=list)
    word_count: int = 0
    estimated_reading_seconds: int = 0
    subsections: list["LessonAstSection"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LessonAstDocument:
    """Top-level AST for an authored lesson."""

    title: str
    summary: str
    learning_objectives: list[str] = field(default_factory=list)
    key_takeaways: list[str] = field(default_factory=list)
    practice_problems: list[LessonAstNode] = field(default_factory=list)
    memory_aids: list[str] = field(default_factory=list)
    exam_strategies: list[str] = field(default_factory=list)
    sections: list[LessonAstSection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    guided_session: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_lesson_ast(parsed: Mapping[str, Any]) -> LessonAstDocument:
    """Lift parsed lesson JSON into a semantic AST.

    The parser output is already structured, so this step focuses on semantic
    labeling: block kinds become educational node kinds, section titles become
    roles, and nested headings become subsection trees.
    """

    metadata = dict(parsed.get("metadata") or {})
    title = str(metadata.get("title") or parsed.get("title") or "")
    summary = str(parsed.get("summary") or "")
    learning_objectives = _coerce_string_list(parsed.get("learning_objectives"))
    key_takeaways = _coerce_string_list(parsed.get("key_takeaways"))
    memory_aids = _coerce_string_list(parsed.get("memory_aids"))
    exam_strategies = _coerce_string_list(parsed.get("exam_strategies"))

    sections = [
        _build_section_ast(section, path=[section.get("title", "")])
        for section in parsed.get("sections") or []
        if isinstance(section, Mapping) and str(section.get("title", "")).strip()
    ]

    practice_problems = [
        LessonAstNode(
            kind="practice",
            title=f"Practice {problem.get('number', index + 1)}",
            text=str(problem.get("question") or ""),
            content=dict(problem),
            metadata={
                "difficulty": problem.get("difficulty", "medium"),
            },
        )
        for index, problem in enumerate(parsed.get("practice_problems") or [])
        if isinstance(problem, Mapping)
    ]

    guided_session = dict(parsed.get("guided_session") or {})

    return LessonAstDocument(
        title=title,
        summary=summary,
        learning_objectives=learning_objectives,
        key_takeaways=key_takeaways,
        practice_problems=practice_problems,
        memory_aids=memory_aids,
        exam_strategies=exam_strategies,
        sections=sections,
        metadata=metadata,
        guided_session=guided_session,
    )


def _build_section_ast(
    section: Mapping[str, Any],
    *,
    path: list[str],
) -> LessonAstSection:
    title = str(section.get("title", "")).strip()
    nodes = [
        _block_to_node(block, section_title=title)
        for block in section.get("blocks") or []
        if isinstance(block, Mapping)
    ]
    subsections = [
        _build_section_ast(subsection, path=path + [str(subsection.get("title", "")).strip()])
        for subsection in section.get("subsections") or []
        if isinstance(subsection, Mapping) and str(subsection.get("title", "")).strip()
    ]

    return LessonAstSection(
        title=title,
        nodes=nodes,
        difficulty=_coerce_string_list(section.get("difficulty")),
        word_count=int(section.get("word_count") or 0),
        estimated_reading_seconds=int(section.get("estimated_reading_seconds") or 0),
        subsections=subsections,
        metadata={
            "role": _infer_section_role(title, nodes),
            "path": path,
        },
    )


def _block_to_node(block: Mapping[str, Any], *, section_title: str) -> LessonAstNode:
    block_type = str(block.get("type") or "prose").lower().strip()
    content = block.get("content")

    if block_type == "table" and isinstance(content, Mapping):
        return LessonAstNode(
            kind="table",
            title=section_title,
            content=dict(content),
            metadata={"block_type": block_type},
        )

    if block_type == "check_understanding":
        checks = content if isinstance(content, list) else []
        return LessonAstNode(
            kind="quiz",
            title=section_title,
            content=checks,
            metadata={"block_type": block_type, "check_count": len(checks)},
        )

    text = str(content or "")
    kind = {
        "prose": _infer_prose_kind(section_title, text),
        "code": "syntax",
        "formula": "formula",
        "tip": "insight",
        "warning": "warning",
        "example": "example",
        "step_by_step": "practice",
        "list": "checklist",
        "svg": "diagram",
    }.get(block_type, "explanation")

    return LessonAstNode(
        kind=kind,
        title=section_title if kind not in {"syntax", "formula"} else "",
        text=text,
        content=text,
        metadata={"block_type": block_type},
    )


def _infer_section_role(title: str, nodes: list[LessonAstNode]) -> str:
    lower = title.lower().strip()
    node_kinds = {node.kind for node in nodes}

    if any(
        marker in lower
        for marker in ("introduction", "why ", "why tested", "lesson cover", "cover")
    ):
        return "cover"
    if "learning objective" in lower or lower in {"objective", "objectives"}:
        return "objectives"
    if any(marker in lower for marker in ("overview", "section overview", "focus areas")):
        return "overview"
    if "practice" in lower or "guided practice" in lower:
        return "practice"
    if "check your understanding" in lower or "quick check" in lower:
        return "quick_check"
    if "memory aid" in lower or "mnemonic" in lower:
        return "remember"
    if "exam strateg" in lower or "strategy" in lower:
        return "strategy"
    if "mastery checklist" in lower or "takeaway" in lower:
        return "takeaway"
    if "summary" in lower or "recap" in lower:
        return "summary"
    if "example" in lower or node_kinds == {"example"}:
        return "example"
    if "table" in node_kinds or "diagram" in node_kinds or "svg" in node_kinds:
        return "visualization"
    if "quiz" in node_kinds:
        return "quick_check"
    return "concept"


def _infer_prose_kind(section_title: str, text: str) -> str:
    lower = section_title.lower().strip()
    if any(marker in lower for marker in ("what is", "definition", "define")):
        return "definition"
    if any(marker in lower for marker in ("why ", "how ", "principle", "rule", "concept")):
        return "insight"
    if len(text.split()) <= 24:
        return "explanation"
    return "concept"


def _coerce_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result
