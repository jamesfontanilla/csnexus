"""Compile the lesson AST into the JSON model consumed by the app."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.features.content.schemas import (
    ContentBlock,
    GuidedSession,
    GuidedSessionStep,
    LessonContent,
    LessonExplanation,
    LessonMetadata,
    LessonScreen,
    LessonScreenPlan,
    LessonSection,
    LessonWorkedExample,
    PracticeProblem,
    TableOfContentsEntry,
)

from .ast import LessonBlockNode, LessonDocumentAst, LessonSectionNode


def compile_lesson_model(document: LessonDocumentAst) -> dict[str, Any]:
    """Compile the semantic document into the published lesson JSON shape."""

    sections = [_compile_section(section) for section in document.sections]
    explanations = _compile_explanations(document)
    worked_examples = _compile_worked_examples(document)
    practice_problems = _compile_practice_problems(document)
    memory_aids = _compile_text_list(document, {"memory_aids"})
    exam_strategies = _compile_text_list(document, {"exam_strategies"})
    table_of_contents = [TableOfContentsEntry(title=section.title, index=index) for index, section in enumerate(sections)]
    guided_session = _build_guided_session(document, sections)
    screen_plan = _build_screen_plan(document, sections, guided_session)
    metadata = _compile_metadata(document, screen_plan, practice_problem_count=len(practice_problems))
    model = LessonContent(
        explanations=explanations,
        worked_examples=worked_examples,
        key_takeaways=document.key_takeaways or [document.summary or f"Learn {document.title}."],
        summary=document.summary or f"Learn {document.title}.",
        metadata=metadata,
        learning_objectives=document.learning_objectives,
        guided_session=guided_session,
        screen_plan=screen_plan,
        table_of_contents=table_of_contents,
        sections=sections,
        practice_problems=practice_problems,
        memory_aids=memory_aids,
        exam_strategies=exam_strategies,
    )
    return model.model_dump()


def _compile_section(section: LessonSectionNode) -> LessonSection:
    return LessonSection(
        title=section.title,
        kind=section.kind,
        blocks=[_compile_block(block) for block in section.blocks],
        subsections=[_compile_section(subsection) for subsection in section.subsections],
        metadata=dict(section.metadata),
        difficulty=_difficulty_for_section(section),
        word_count=section.word_count,
        estimated_reading_seconds=section.estimated_reading_seconds,
    )


def _compile_block(block: LessonBlockNode) -> ContentBlock:
    block_type, content, language, metadata = _render_block(block)
    return ContentBlock(
        type=block_type,
        content=content,
        language=language,
        children=[_compile_block(child) for child in block.children],
        metadata=metadata,
    )


def _render_block(block: LessonBlockNode) -> tuple[str, Any, str | None, dict[str, Any]]:
    metadata = dict(block.metadata)
    kind = block.kind

    if kind in {"prose", "definition", "quote", "note", "callout", "divider", "video"}:
        return "prose", _block_to_markdown(block), block.language, metadata
    if kind in {"bullet_list", "checklist"}:
        items = metadata.get("items") or _block_list_items(block)
        return "list", "\n".join(f"- {item}" for item in items), None, metadata
    if kind == "ordered_list":
        items = metadata.get("items") or _block_list_items(block)
        return "step_by_step", "\n".join(f"{index + 1}. {item}" for index, item in enumerate(items)), None, metadata
    if kind == "table":
        return "table", block.content, None, metadata
    if kind == "tip":
        return "tip", _block_to_markdown(block), None, metadata
    if kind == "warning":
        return "warning", _block_to_markdown(block), None, metadata
    if kind == "example":
        return "example", _block_to_markdown(block), None, metadata
    if kind == "code":
        return "code", _block_to_markdown(block), block.language, metadata
    if kind == "formula":
        return "formula", _block_to_markdown(block), block.language or "formula", metadata
    if kind == "svg":
        return "svg", _block_to_markdown(block), None, metadata
    if kind == "mermaid":
        return "code", _block_to_markdown(block), "mermaid", metadata
    if kind == "image":
        return "prose", _block_to_markdown(block), None, metadata
    if kind in {"question", "answer"}:
        return "prose", _block_to_markdown(block), None, metadata
    if kind in {"diagram"}:
        return "svg", _block_to_markdown(block), None, metadata
    if kind in {"interactive_exercise", "embedded_quiz"}:
        checks = _extract_checks(block)
        return "check_understanding", checks, None, metadata
    if kind == "check_understanding":
        checks = _extract_checks(block)
        return "check_understanding", checks, None, metadata

    return "prose", _block_to_markdown(block), block.language, metadata


def _extract_checks(block: LessonBlockNode) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if block.kind == "question":
        question = _block_to_markdown(block)
        answer = str(block.metadata.get("answer") or "").strip()
        checks.append({"question": question, "answer": answer, "rationale": str(block.metadata.get("rationale") or "")})
    elif block.kind == "answer":
        answer = _block_to_markdown(block)
        question = str(block.metadata.get("question") or "").strip()
        checks.append({"question": question, "answer": answer, "rationale": str(block.metadata.get("rationale") or "")})
    else:
        payload = block.content if isinstance(block.content, list) else []
        for item in payload:
            if isinstance(item, dict):
                question = str(item.get("question") or "").strip()
                answer = str(item.get("answer") or "").strip()
                rationale = str(item.get("rationale") or "").strip()
                if question or answer:
                    checks.append({"question": question, "answer": answer, "rationale": rationale})
    return checks


def _block_to_markdown(block: LessonBlockNode) -> str:
    content = block.content
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if "headers" in content and "rows" in content:
            headers = content.get("headers") or []
            rows = content.get("rows") or []
            header_line = "| " + " | ".join(str(header) for header in headers) + " |"
            separator_line = "| " + " | ".join("---" for _ in headers) + " |"
            row_lines = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
            return "\n".join([header_line, separator_line, *row_lines]).strip()
        if "text" in content and isinstance(content["text"], str):
            return content["text"]
        if "body" in content and isinstance(content["body"], str):
            return content["body"]
        if "content" in content and isinstance(content["content"], str):
            return content["content"]
        if "items" in content and isinstance(content["items"], list):
            items = [str(item) for item in content["items"]]
            return "\n".join(f"- {item}" for item in items)
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                question = str(item.get("question") or "").strip()
                answer = str(item.get("answer") or "").strip()
                rationale = str(item.get("rationale") or "").strip()
                if question:
                    parts.append(f"Question: {question}")
                if answer:
                    parts.append(f"Answer: {answer}")
                if rationale:
                    parts.append(f"Rationale: {rationale}")
            else:
                parts.append(str(item))
        return "\n\n".join(parts)
    return str(content or "")


def _block_list_items(block: LessonBlockNode) -> list[str]:
    content = block.content
    if isinstance(content, dict):
        items = content.get("items")
        if isinstance(items, list):
            return [str(item) for item in items if str(item).strip()]
    if isinstance(content, str):
        return [line.strip(" -*\t") for line in content.splitlines() if line.strip()]
    return []


def _compile_explanations(document: LessonDocumentAst) -> list[LessonExplanation]:
    explanations: list[LessonExplanation] = []
    for section in document.sections:
        if section.kind == "explanations":
            for child in section.subsections:
                body = _section_body(child)
                if body:
                    explanations.append(LessonExplanation(heading=child.title, body=body))
            if not explanations:
                body = _section_body(section)
                if body:
                    explanations.append(LessonExplanation(heading=section.title, body=body))
    if not explanations:
        fallback = document.summary or f"Lesson covering {document.title}."
        explanations.append(LessonExplanation(heading="Overview", body=fallback))
    return explanations


def _compile_worked_examples(document: LessonDocumentAst) -> list[LessonWorkedExample]:
    examples: list[LessonWorkedExample] = []
    for section in document.sections:
        if section.kind == "worked_examples":
            for child in section.subsections:
                body = _section_body(child)
                examples.append(LessonWorkedExample(title=child.title or "Worked example", body=body or document.summary))
            if not examples:
                body = _section_body(section)
                if body:
                    examples.append(LessonWorkedExample(title=section.title, body=body))
    if not examples:
        examples.append(
            LessonWorkedExample(
                title="See lesson sections",
                body="Worked examples are embedded within lesson sections.",
            )
        )
    return examples


def _compile_practice_problems(document: LessonDocumentAst) -> list[PracticeProblem]:
    problems: list[PracticeProblem] = []
    number = 1
    for section in document.sections:
        if section.kind not in {"practice_review", "final_challenge"}:
            continue
        for block in _flatten_blocks(section):
            checks = _extract_checks(block)
            for check in checks:
                if not check["question"] and not check["answer"]:
                    continue
                problems.append(
                    PracticeProblem(
                        number=number,
                        question=check["question"],
                        answer=check["answer"],
                        explanation=check.get("rationale", ""),
                        difficulty="medium",
                    )
                )
                number += 1
    return problems


def _compile_text_list(document: LessonDocumentAst, kinds: set[str]) -> list[str]:
    items: list[str] = []
    for section in document.sections:
        if section.kind not in kinds:
            continue
        items.extend(_section_text_lines(section))
        for child in section.subsections:
            items.extend(_section_text_lines(child))
    return _dedupe_text(items)


def _section_text_lines(section: LessonSectionNode) -> list[str]:
    lines: list[str] = []
    for block in _flatten_blocks(section):
        text = _block_to_markdown(block)
        if not text.strip():
            continue
        for line in text.splitlines():
            cleaned = line.strip(" -*\t")
            if cleaned:
                lines.append(cleaned)
    return lines


def _flatten_blocks(section: LessonSectionNode) -> list[LessonBlockNode]:
    blocks = list(section.blocks)
    for child in section.subsections:
        blocks.extend(_flatten_blocks(child))
    return blocks


def _build_guided_session(document: LessonDocumentAst, sections: list[LessonSection]) -> GuidedSession:
    steps: list[GuidedSessionStep] = []
    index = 0

    if document.learning_objectives:
        steps.append(
            GuidedSessionStep(
                index=index,
                kind="objective",
                title="Learning objectives",
                summary=document.learning_objectives[0],
                section_index=0 if sections else None,
                estimated_reading_seconds=20,
                subsection_count=0,
                focus_tags=["objective"],
            )
        )
        index += 1

    for section_index, section in enumerate(sections):
        if section.kind == "explanations":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="foundation",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "foundation"],
                )
            )
            index += 1
        elif section.kind == "micro_concept":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="concept",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, *[child.kind for child in section.subsections[:3]]],
                )
            )
            index += 1
        elif section.kind == "worked_examples":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="example",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "example"],
                )
            )
            index += 1
        elif section.kind == "exam_strategies":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="strategy",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "strategy"],
                )
            )
            index += 1
        elif section.kind == "memory_aids":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="insight",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "memory"],
                )
            )
            index += 1
        elif section.kind == "practice_review":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="practice",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "practice"],
                )
            )
            index += 1
        elif section.kind == "key_takeaways":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="summary",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "recall"],
                )
            )
            index += 1
        elif section.kind == "summary":
            steps.append(
                GuidedSessionStep(
                    index=index,
                    kind="summary",
                    title=section.title,
                    summary=_section_preview(section),
                    section_index=section_index,
                    estimated_reading_seconds=section.estimated_reading_seconds,
                    subsection_count=len(section.subsections),
                    focus_tags=[section.kind, "summary"],
                )
            )
            index += 1

    if document.summary:
        steps.append(
            GuidedSessionStep(
                index=index,
                kind="exit",
                title="Wrap up",
                summary=document.summary,
                section_index=len(sections) - 1 if sections else None,
                estimated_reading_seconds=10,
                subsection_count=0,
                focus_tags=["completion"],
            )
        )

    return GuidedSession(
        title=document.title,
        objective=document.learning_objectives[0] if document.learning_objectives else document.summary,
        must_know=(document.learning_objectives[:3] + document.key_takeaways[:3])[:5],
        steps=steps,
    )


def _build_screen_plan(
    document: LessonDocumentAst,
    sections: list[LessonSection],
    guided_session: GuidedSession,
) -> LessonScreenPlan:
    screens: list[LessonScreen] = []
    index = 0

    if sections:
        screens.append(
            LessonScreen(
                index=index,
                kind="cover",
                title=document.title or "Lesson",
                summary=document.summary or document.title,
                section_indices=[0],
                section_titles=[sections[0].title],
                estimated_reading_seconds=sections[0].estimated_reading_seconds,
                focus_tags=["cover"],
                node_kinds=[sections[0].kind],
                call_to_action="Start lesson",
            )
        )
        index += 1

    for section_index, section in enumerate(sections):
        kind = _screen_kind_for_section(section)
        if section_index == 0 and kind == "cover":
            continue
        screens.append(
            LessonScreen(
                index=index,
                kind=kind,
                title=section.title,
                summary=_section_preview(section),
                section_indices=[section_index],
                section_titles=[section.title],
                estimated_reading_seconds=section.estimated_reading_seconds,
                focus_tags=[section.kind, *[child.kind for child in section.subsections[:3]]],
                node_kinds=_collect_node_kinds(section),
                call_to_action=_call_to_action(kind),
            )
        )
        index += 1

    if not screens:
        screens.append(
            LessonScreen(
                index=0,
                kind="summary",
                title=document.title or "Lesson",
                summary=document.summary or document.title,
                section_indices=[],
                section_titles=[],
                estimated_reading_seconds=30,
                focus_tags=["summary"],
                node_kinds=["summary"],
                call_to_action="Continue",
            )
        )

    return LessonScreenPlan(
        title=document.title,
        objective=guided_session.objective,
        must_know=guided_session.must_know,
        screens=screens,
        estimated_reading_minutes=max(1, int(round(sum(screen.estimated_reading_seconds for screen in screens) / 60))),
        screen_count=len(screens),
    )


def _screen_kind_for_section(section: LessonSectionNode) -> str:
    if section.kind == "explanations":
        return "overview"
    if section.kind == "micro_concept":
        return "concept"
    if section.kind == "worked_examples":
        return "example"
    if section.kind == "exam_strategies":
        return "strategy"
    if section.kind == "memory_aids":
        return "remember"
    if section.kind == "practice_review":
        return "practice"
    if section.kind == "key_takeaways":
        return "takeaway"
    if section.kind == "summary":
        return "summary"
    if section.kind == "final_challenge":
        return "completion"
    return "concept"


def _call_to_action(kind: str) -> str:
    return {
        "cover": "Start lesson",
        "overview": "Scan the structure",
        "concept": "Study the concept",
        "example": "Work through the example",
        "strategy": "Use this strategy",
        "remember": "Lock it in",
        "practice": "Practice now",
        "takeaway": "Review the essentials",
        "summary": "Finish the summary",
        "completion": "Complete the lesson",
    }.get(kind, "Continue")


def _section_preview(section: LessonSectionNode) -> str:
    for block in section.blocks:
        text = _block_preview(block)
        if text:
            return text
    for child in section.subsections:
        text = _section_preview(child)
        if text:
            return text
    return ""


def _block_preview(block: LessonBlockNode) -> str:
    if isinstance(block.content, str) and block.content.strip():
        return " ".join(block.content.split())[:200]
    if isinstance(block.content, dict):
        for key in ("summary", "body", "content", "text"):
            value = block.content.get(key)
            if isinstance(value, str) and value.strip():
                return " ".join(value.split())[:200]
    if isinstance(block.content, list) and block.content:
        first = block.content[0]
        if isinstance(first, dict):
            question = str(first.get("question") or "").strip()
            answer = str(first.get("answer") or "").strip()
            if question and answer:
                return f"{question} {answer}"[:200]
    return ""


def _collect_node_kinds(section: LessonSectionNode) -> list[str]:
    kinds: list[str] = []
    for block in _flatten_blocks(section):
        kind = str(block.metadata.get("semantic_kind") or block.type)
        if kind not in kinds:
            kinds.append(kind)
    for child in section.subsections:
        if child.kind not in kinds:
            kinds.append(child.kind)
    return kinds


def _difficulty_for_section(section: LessonSectionNode) -> list[str]:
    if section.kind == "micro_concept":
        return ["medium"]
    if section.kind in {"worked_examples", "practice_review", "final_challenge"}:
        return ["medium", "hard"]
    if section.kind in {"key_takeaways", "summary", "memory_aids"}:
        return ["easy"]
    return ["medium"]


def _compile_metadata(
    document: LessonDocumentAst,
    screen_plan: LessonScreenPlan,
    *,
    practice_problem_count: int,
) -> LessonMetadata:
    total_words = sum(section.word_count for section in document.sections)
    return LessonMetadata(
        title=document.title,
        estimated_reading_minutes=screen_plan.estimated_reading_minutes,
        section_count=len(document.sections),
        learning_objective_count=len(document.learning_objectives),
        has_practice_problems=practice_problem_count > 0,
        practice_problem_count=practice_problem_count,
        difficulty_distribution=_difficulty_distribution(document),
        total_word_count=total_words,
        screen_count=screen_plan.screen_count,
    )


def _difficulty_distribution(document: LessonDocumentAst) -> dict[str, int]:
    distribution = defaultdict(int)
    for section in document.sections:
        for difficulty in _difficulty_for_section(section):
            distribution[difficulty] += 1
    return {"easy": distribution["easy"], "medium": distribution["medium"], "hard": distribution["hard"]}


def _section_body(section: LessonSectionNode) -> str:
    parts: list[str] = []
    for block in section.blocks:
        text = _block_preview(block)
        if text:
            parts.append(text)
    return "\n\n".join(parts).strip()


def _dedupe_text(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        value = " ".join(str(item).split()).strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result
