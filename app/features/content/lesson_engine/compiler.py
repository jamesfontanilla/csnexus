"""Lesson compiler.

Consumes a semantic AST and produces a screen plan that a renderer can turn
into a guided lesson flow. The compiler intentionally groups and labels
screens by educational purpose instead of preserving Markdown structure.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .ast import LessonAstDocument, LessonAstNode, LessonAstSection

SCREEN_KIND_COVER = "cover"
SCREEN_KIND_OBJECTIVES = "objectives"
SCREEN_KIND_OVERVIEW = "overview"
SCREEN_KIND_CONCEPT = "concept"
SCREEN_KIND_EXAMPLE = "example"
SCREEN_KIND_VISUALIZATION = "visualization"
SCREEN_KIND_QUICK_CHECK = "quick_check"
SCREEN_KIND_PRACTICE = "practice"
SCREEN_KIND_STRATEGY = "strategy"
SCREEN_KIND_REMEMBER = "remember"
SCREEN_KIND_TAKEAWAY = "takeaway"
SCREEN_KIND_SUMMARY = "summary"
SCREEN_KIND_COMPLETION = "completion"

_SPECIAL_SCREEN_KINDS = {
    SCREEN_KIND_COVER,
    SCREEN_KIND_OBJECTIVES,
    SCREEN_KIND_OVERVIEW,
    SCREEN_KIND_EXAMPLE,
    SCREEN_KIND_VISUALIZATION,
    SCREEN_KIND_QUICK_CHECK,
    SCREEN_KIND_PRACTICE,
    SCREEN_KIND_STRATEGY,
    SCREEN_KIND_REMEMBER,
    SCREEN_KIND_TAKEAWAY,
    SCREEN_KIND_SUMMARY,
    SCREEN_KIND_COMPLETION,
}

_TARGET_SCREEN_SECONDS = 180


@dataclass(slots=True)
class CompiledLessonScreen:
    """One runtime screen in the guided lesson flow."""

    index: int
    kind: str
    title: str
    summary: str = ""
    section_indices: list[int] = field(default_factory=list)
    section_titles: list[str] = field(default_factory=list)
    estimated_reading_seconds: int = 0
    focus_tags: list[str] = field(default_factory=list)
    node_kinds: list[str] = field(default_factory=list)
    call_to_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CompiledLessonPlan:
    """Top-level compiled lesson flow."""

    title: str
    objective: str
    must_know: list[str]
    screens: list[CompiledLessonScreen]
    estimated_reading_minutes: int
    screen_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compile_lesson_plan(document: LessonAstDocument) -> CompiledLessonPlan:
    """Compile semantic lesson nodes into an ordered screen plan."""

    screens: list[CompiledLessonScreen] = []
    screen_index = 0

    objective = _choose_objective(document)
    must_know = _choose_must_know(document)

    preamble_sections = list(document.sections[:3])
    remainder_start = len(preamble_sections)

    if preamble_sections:
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_COVER,
                title=document.title or "Lesson cover",
                summary=document.summary or objective,
                section_indices=[0] if document.sections else [],
                section_titles=[section.title for section in preamble_sections[:1]],
                estimated_reading_seconds=sum(
                    section.estimated_reading_seconds for section in preamble_sections[:1]
                ),
                focus_tags=["cover", "progress"],
                node_kinds=_collect_node_kinds(preamble_sections[:1]),
                call_to_action="Start lesson",
            )
        )
        screen_index += 1

    if len(preamble_sections) >= 2 or document.learning_objectives:
        sections_for_objectives = preamble_sections[1:2] if len(preamble_sections) > 1 else []
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_OBJECTIVES,
                title="Learning objectives",
                summary=document.learning_objectives[0] if document.learning_objectives else objective,
                section_indices=[1] if len(document.sections) > 1 else [],
                section_titles=[section.title for section in sections_for_objectives],
                estimated_reading_seconds=sum(
                    section.estimated_reading_seconds for section in sections_for_objectives
                ),
                focus_tags=["objectives", "clarity"],
                node_kinds=_collect_node_kinds(sections_for_objectives),
                call_to_action="See what you will master",
            )
        )
        screen_index += 1

    overview_sections = [
        section
        for section in document.sections
        if section.metadata.get("role") == "overview"
    ]
    if overview_sections:
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_OVERVIEW,
                title="Section overview",
                summary=_join_preview(overview_sections),
                section_indices=_section_indices(document.sections, overview_sections),
                section_titles=[section.title for section in overview_sections],
                estimated_reading_seconds=sum(section.estimated_reading_seconds for section in overview_sections),
                focus_tags=["overview", "navigation"],
                node_kinds=_collect_node_kinds(overview_sections),
                call_to_action="Map the journey",
            )
        )
        screen_index += 1

    content_sections = [
        section for section in document.sections if section not in preamble_sections[:2] and section.metadata.get("role") not in {"overview"}
    ]

    grouped_sections = _group_sections_for_screens(content_sections)
    for group in grouped_sections:
        if not group:
            continue
        kind = _screen_kind_for_group(group)
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=kind,
                title=_screen_title_for_group(kind, group),
                summary=_join_preview(group),
                section_indices=_section_indices(document.sections, group),
                section_titles=[section.title for section in group],
                estimated_reading_seconds=sum(section.estimated_reading_seconds for section in group),
                focus_tags=_focus_tags_for_group(kind, group),
                node_kinds=_collect_node_kinds(group),
                call_to_action=_call_to_action_for_kind(kind),
            )
        )
        screen_index += 1

    if document.practice_problems:
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_PRACTICE,
                title="Practice",
                summary="Work through the guided practice and check your understanding.",
                section_indices=[],
                section_titles=[],
                estimated_reading_seconds=max(60, len(document.practice_problems) * 45),
                focus_tags=["practice", "feedback"],
                node_kinds=["practice"],
                call_to_action="Try the exercises",
            )
        )
        screen_index += 1

    if document.memory_aids:
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_REMEMBER,
                title="Memory aids",
                summary=document.memory_aids[0],
                section_indices=[],
                section_titles=[],
                estimated_reading_seconds=max(20, len(document.memory_aids) * 15),
                focus_tags=["memory", "retention"],
                node_kinds=["memory_aid"],
                call_to_action="Lock it in",
            )
        )
        screen_index += 1

    if document.exam_strategies:
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_STRATEGY,
                title="Exam strategy",
                summary=document.exam_strategies[0],
                section_indices=[],
                section_titles=[],
                estimated_reading_seconds=max(20, len(document.exam_strategies) * 15),
                focus_tags=["strategy", "exam"],
                node_kinds=["strategy"],
                call_to_action="Use this on test day",
            )
        )
        screen_index += 1

    if document.key_takeaways:
        screens.append(
            CompiledLessonScreen(
                index=screen_index,
                kind=SCREEN_KIND_TAKEAWAY,
                title="Key takeaways",
                summary=document.key_takeaways[0],
                section_indices=[],
                section_titles=[],
                estimated_reading_seconds=max(30, len(document.key_takeaways) * 12),
                focus_tags=["takeaway", "recall"],
                node_kinds=["takeaway"],
                call_to_action="Review the essentials",
            )
        )
        screen_index += 1

    screens.append(
        CompiledLessonScreen(
            index=screen_index,
            kind=SCREEN_KIND_COMPLETION,
            title="Lesson complete",
            summary=document.summary or objective,
            section_indices=[],
            section_titles=[],
            estimated_reading_seconds=10,
            focus_tags=["completion", "progress"],
            node_kinds=["completion"],
            call_to_action="Mark complete",
        )
    )

    return CompiledLessonPlan(
        title=document.title,
        objective=objective,
        must_know=must_know,
        screens=screens,
        estimated_reading_minutes=max(
            1,
            _round_minutes(
                sum(screen.estimated_reading_seconds for screen in screens)
            ),
        ),
        screen_count=len(screens),
    )


def _choose_objective(document: LessonAstDocument) -> str:
    if document.learning_objectives:
        return document.learning_objectives[0]
    if document.summary.strip():
        return document.summary.strip()
    return f"Learn {document.title}".strip()


def _choose_must_know(document: LessonAstDocument) -> list[str]:
    items: list[str] = []
    items.extend(document.learning_objectives[:3])
    items.extend(document.key_takeaways[:4])
    return _dedupe_nonempty(items) or ([document.summary] if document.summary else [])


def _group_sections_for_screens(
    sections: list[LessonAstSection],
) -> list[list[LessonAstSection]]:
    groups: list[list[LessonAstSection]] = []
    current: list[LessonAstSection] = []
    current_seconds = 0
    current_role = ""

    def flush() -> None:
        nonlocal current, current_seconds, current_role
        if current:
            groups.append(list(current))
        current = []
        current_seconds = 0
        current_role = ""

    for section in sections:
        role = str(section.metadata.get("role") or "concept")
        if role in {"cover", "objectives", "overview"}:
            # The preamble screens are built separately.
            continue

        if not current:
            current = [section]
            current_seconds = section.estimated_reading_seconds
            current_role = role
            continue

        should_force_split = role in _SPECIAL_SCREEN_KINDS and role not in {"concept"}
        would_exceed_target = current_seconds + section.estimated_reading_seconds > _TARGET_SCREEN_SECONDS
        role_shift = role != current_role and current_role == "concept"

        if should_force_split or (would_exceed_target and role_shift):
            flush()
            current = [section]
            current_seconds = section.estimated_reading_seconds
            current_role = role
        else:
            current.append(section)
            current_seconds += section.estimated_reading_seconds
            if current_role == "concept" and role != "concept":
                current_role = role

    flush()
    return groups


def _screen_kind_for_group(group: list[LessonAstSection]) -> str:
    roles = [str(section.metadata.get("role") or "concept") for section in group]
    if any(role == "quick_check" for role in roles):
        return SCREEN_KIND_QUICK_CHECK
    if any(role == "practice" for role in roles):
        return SCREEN_KIND_PRACTICE
    if any(role == "strategy" for role in roles):
        return SCREEN_KIND_STRATEGY
    if any(role == "remember" for role in roles):
        return SCREEN_KIND_REMEMBER
    if any(role == "takeaway" for role in roles):
        return SCREEN_KIND_TAKEAWAY
    if any(role == "summary" for role in roles):
        return SCREEN_KIND_SUMMARY
    if any(role == "example" for role in roles):
        return SCREEN_KIND_EXAMPLE
    if any(role == "visualization" for role in roles):
        return SCREEN_KIND_VISUALIZATION
    return SCREEN_KIND_CONCEPT


def _screen_title_for_group(kind: str, group: list[LessonAstSection]) -> str:
    if len(group) == 1:
        return group[0].title
    if kind == SCREEN_KIND_CONCEPT:
        return group[0].title
    return kind.replace("_", " ").title()


def _focus_tags_for_group(kind: str, group: list[LessonAstSection]) -> list[str]:
    tags = [kind]
    for section in group:
        role = str(section.metadata.get("role") or "concept")
        if role not in tags:
            tags.append(role)
        for node in section.nodes:
            if node.kind not in tags:
                tags.append(node.kind)
    return _dedupe_nonempty(tags)


def _call_to_action_for_kind(kind: str) -> str:
    return {
        SCREEN_KIND_CONCEPT: "Keep going",
        SCREEN_KIND_EXAMPLE: "Study the example",
        SCREEN_KIND_VISUALIZATION: "Read the visual",
        SCREEN_KIND_QUICK_CHECK: "Check your understanding",
        SCREEN_KIND_PRACTICE: "Practice now",
        SCREEN_KIND_STRATEGY: "Use this strategy",
        SCREEN_KIND_REMEMBER: "Memorize the cue",
        SCREEN_KIND_TAKEAWAY: "Lock in the lesson",
        SCREEN_KIND_SUMMARY: "Review the summary",
    }.get(kind, "Continue")


def _join_preview(sections: list[LessonAstSection]) -> str:
    previews: list[str] = []
    for section in sections:
        preview = _section_preview(section)
        if preview:
            previews.append(preview)
    return " ".join(previews).strip()


def _section_preview(section: LessonAstSection) -> str:
    for node in section.nodes:
        if node.text.strip():
            return _shorten(node.text)
        if isinstance(node.content, dict):
            candidate = str(node.content.get("summary") or node.content.get("text") or "")
            if candidate.strip():
                return _shorten(candidate)
        if isinstance(node.content, str) and node.content.strip():
            return _shorten(node.content)
    return ""


def _shorten(text: str, limit: int = 180) -> str:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[:limit].rsplit(" ", 1)[0].strip()


def _section_indices(
    all_sections: list[LessonAstSection],
    selected: list[LessonAstSection],
) -> list[int]:
    indices: list[int] = []
    selected_ids = {id(section) for section in selected}
    for index, section in enumerate(all_sections):
        if id(section) in selected_ids:
            indices.append(index)
    return indices


def _collect_node_kinds(sections: list[LessonAstSection]) -> list[str]:
    kinds: list[str] = []
    for section in sections:
        for node in section.nodes:
            if node.kind not in kinds:
                kinds.append(node.kind)
    return kinds


def _round_minutes(seconds: int) -> int:
    return max(1, (seconds + 59) // 60)


def _dedupe_nonempty(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        value = item.strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result
