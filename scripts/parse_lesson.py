"""Enhanced lesson markdown parser.

Extracts rich structured content from lesson.md files for frontend rendering:
- Sections with table-of-contents metadata
- Practice problems as interactive quiz items
- Tables, formulas, tips, warnings, and memory aids as typed content blocks
- Difficulty-tagged examples
- Estimated reading time and section counts
- Key takeaways and exam strategies extracted into dedicated fields
- Guided-session metadata for bite-sized, card-oriented lesson UX

The output JSON is designed so a frontend can render each content type
with a distinct UI component rather than dumping raw markdown.
"""

from __future__ import annotations

import math
import re
from typing import Any

from app.features.content.lesson_engine import build_lesson_ast, compile_lesson_plan


# ---------------------------------------------------------------------------
# Content block types the frontend can render distinctly
# ---------------------------------------------------------------------------

BLOCK_TYPE_PROSE = "prose"
BLOCK_TYPE_TABLE = "table"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_FORMULA = "formula"
BLOCK_TYPE_TIP = "tip"
BLOCK_TYPE_WARNING = "warning"
BLOCK_TYPE_EXAMPLE = "example"
BLOCK_TYPE_STEP_BY_STEP = "step_by_step"
BLOCK_TYPE_LIST = "list"
BLOCK_TYPE_SVG = "svg"
BLOCK_TYPE_CHECK_UNDERSTANDING = "check_understanding"

GUIDED_STEP_KIND_OBJECTIVE = "objective"
GUIDED_STEP_KIND_FOUNDATION = "foundation"
GUIDED_STEP_KIND_CONCEPT = "concept"
GUIDED_STEP_KIND_INSIGHT = "insight"
GUIDED_STEP_KIND_EXAMPLE = "example"
GUIDED_STEP_KIND_WARNING = "warning"
GUIDED_STEP_KIND_PRACTICE = "practice"
GUIDED_STEP_KIND_STRATEGY = "strategy"
GUIDED_STEP_KIND_SUMMARY = "summary"
GUIDED_STEP_KIND_EXIT = "exit"

# Average reading speed in words per minute for educational content
_WORDS_PER_MINUTE = 200

# Segment target: words per segment (~3-5 min read)
_SEGMENT_TARGET_WORDS = 800

# Section titles that always start a new segment (mode-shift boundaries)
_SEGMENT_BREAK_TITLES = {
    "exam strategies",
    "memory aids",
    "guided practice",
    "which method?",
    "before you practice",
    "mini practice set",
    "practice set",
    "connections",
    "mastery checklist",
    "check your understanding",
}

# Categories where segmentation is applied
_SEGMENTED_CATEGORIES = {"clerical-ability"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_lesson_markdown(md_text: str, category: str = "") -> dict[str, Any]:
    """Parse lesson markdown into a rich, UI-friendly JSON structure.

    Args:
        md_text:  Raw markdown content of the lesson file.
        category: Dot-separated content category path, e.g. "clerical-ability"
                  or "clerical-ability.spelling".  Used to decide whether to
                  apply segment-and-gate parsing.  Callers that don't supply
                  this get the legacy flat-section output unchanged.

    Handles two lesson formats:
    1. Old format: Single "## Explanations" with all content under H3 headings
    2. New format: Multiple H2 sections (## 4.1 ..., ## Introduction, etc.)
       with H3 subsections within them

    Returns a dict with:
    - metadata: reading time, section count, difficulty distribution, etc.
    - sections: ordered list of navigable sections with typed content blocks
    - practice_problems: interactive quiz items extracted from Mini Practice Set
    - key_takeaways: bullet-point summary items
    - memory_aids: mnemonic devices and shortcuts
    - exam_strategies: test-taking tips
    - summary: quick recap content
    - table_of_contents: section titles for navigation
    - segments: (clerical-ability only) list of timed chunks with gate checks
    - is_segmented: bool flag for the frontend layout dispatcher
    """
    # Strip the H1 title (lesson title comes from the subtopic record)
    lines = md_text.split("\n")
    title = ""
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            content_start = i + 1
            break

    body_text = "\n".join(lines[content_start:])

    # Split into H2 sections
    h2_sections = _split_h2(body_text)

    # Determine format: old (single "Explanations" H2) vs new (multiple H2s)
    # Old format: has "Explanations" and optionally "Worked Examples",
    # "Key Takeaways", "Summary" — these are structural markers, not content sections
    structural_h2s = {"Explanations", "Worked Examples", "Key Takeaways", "Summary"}
    content_h2s = set(h2_sections.keys()) - structural_h2s
    is_old_format = "Explanations" in h2_sections and len(content_h2s) == 0

    if is_old_format:
        # Old format: H3 headings under "Explanations" are the navigable sections
        explanations_raw = h2_sections.get("Explanations", "")
        all_sections = _split_h3(explanations_raw)
    else:
        # New format: H2 headings are the navigable sections
        # H3 subsections become part of the section body
        # Skip structural H2s that are handled separately
        all_sections = []
        for h2_title, h2_body in h2_sections.items():
            if h2_title in structural_h2s:
                # Still extract content from these for legacy fields
                if h2_title == "Explanations":
                    # If there's an Explanations section in new format,
                    # its H3s are navigable sections
                    h3_entries = _split_h3(h2_body)
                    if h3_entries:
                        all_sections.extend(h3_entries)
                    elif h2_body.strip():
                        all_sections.append((h2_title, h2_body))
                continue
            all_sections.append((h2_title, h2_body))

    # Identify special sections by title pattern and separate them
    regular_sections: list[tuple[str, str]] = []
    practice_raw = ""
    memory_aids_raw = ""
    exam_strategies_raw = ""
    recap_raw = ""
    mastery_raw = ""

    for sec_title, sec_body in all_sections:
        lower_title = sec_title.lower()
        if "mini practice" in lower_title or "practice set" in lower_title:
            practice_raw = sec_body
        elif "memory aid" in lower_title or "mnemonic" in lower_title:
            memory_aids_raw = sec_body
        elif "exam strateg" in lower_title:
            exam_strategies_raw = sec_body
        elif "quick recap" in lower_title or "recap" in lower_title:
            recap_raw = sec_body
        elif "mastery checklist" in lower_title:
            mastery_raw = sec_body
        elif lower_title in ("introduction", "focus areas"):
            # Introduction goes first in regular sections
            regular_sections.insert(0, (sec_title, sec_body))
        elif "learning objective" in lower_title:
            # Learning objectives go after introduction
            insert_idx = 1 if regular_sections else 0
            regular_sections.insert(insert_idx, (sec_title, sec_body))
        else:
            regular_sections.append((sec_title, sec_body))

    # Build structured sections with typed content blocks
    sections = []
    for sec_title, sec_body in regular_sections:
        blocks = _parse_content_blocks(sec_body)
        difficulty = _detect_section_difficulty(sec_body)
        word_count = len(sec_body.split())
        section: dict[str, Any] = {
            "title": sec_title,
            "blocks": blocks,
            "difficulty": difficulty,
            "word_count": word_count,
            "estimated_reading_seconds": math.ceil(word_count / _WORDS_PER_MINUTE * 60),
        }

        subsections = _parse_nested_sections(sec_body)
        if subsections:
            section["subsections"] = subsections

        sections.append(section)

    # Parse practice problems
    practice_problems = _parse_practice_problems(practice_raw)

    # Parse memory aids as bullet list
    memory_aids = _extract_bullets_or_paragraphs(memory_aids_raw)

    # Parse exam strategies
    exam_strategies = _extract_bullets_or_paragraphs(exam_strategies_raw)

    # Parse key takeaways from mastery checklist or recap
    key_takeaways = _extract_checklist(mastery_raw) or _extract_bullets_or_paragraphs(recap_raw)

    # Extract learning objectives for metadata and the guided-session outline
    learning_objectives = _extract_learning_objectives(h2_sections, all_sections)

    # Build table of contents
    toc = [{"title": s["title"], "index": i} for i, s in enumerate(sections)]

    # Compute metadata
    total_words = sum(s["word_count"] for s in sections)
    total_words += len(practice_raw.split()) + len(memory_aids_raw.split())
    estimated_reading_minutes = math.ceil(total_words / _WORDS_PER_MINUTE)

    difficulty_dist = {"easy": 0, "medium": 0, "hard": 0}
    for s in sections:
        if s["difficulty"]:
            for d in s["difficulty"]:
                difficulty_dist[d] = difficulty_dist.get(d, 0) + 1

    # Count practice problems by difficulty if available
    practice_difficulty_dist = {"easy": 0, "medium": 0, "hard": 0}
    for p in practice_problems:
        d = p.get("difficulty", "medium")
        practice_difficulty_dist[d] = practice_difficulty_dist.get(d, 0) + 1

    # Determine if this lesson should be segmented
    apply_segmentation = any(
        category.startswith(cat) for cat in _SEGMENTED_CATEGORIES
    ) if category else False

    segments: list[dict[str, Any]] = []
    if apply_segmentation and sections:
        segments = _build_segments(sections)

    is_segmented = len(segments) > 0

    metadata = {
        "title": title,
        "estimated_reading_minutes": estimated_reading_minutes,
        "section_count": len(sections),
        "learning_objective_count": len(learning_objectives),
        "has_practice_problems": len(practice_problems) > 0,
        "practice_problem_count": len(practice_problems),
        "difficulty_distribution": difficulty_dist,
        "total_word_count": total_words,
        **({"segment_count": len(segments), "is_segmented": True} if is_segmented else {}),
    }

    # Build the legacy-compatible fields too (explanations/worked_examples)
    # so existing consumers don't break
    explanations_legacy = [
        {"title": s["title"], "body": _blocks_to_markdown(s["blocks"])}
        for s in sections
    ]

    # For worked examples, check if there's a dedicated H2 section first
    worked_examples_legacy = []
    if not is_old_format and "Worked Examples" in h2_sections:
        we_entries = _split_h3(h2_sections["Worked Examples"])
        for we_title, we_body in we_entries:
            worked_examples_legacy.append({"title": we_title, "body": we_body})
    elif is_old_format and "Worked Examples" in h2_sections:
        we_entries = _split_h3(h2_sections["Worked Examples"])
        for we_title, we_body in we_entries:
            worked_examples_legacy.append({"title": we_title, "body": we_body})

    # If no dedicated worked examples section, extract from content blocks
    if not worked_examples_legacy:
        for s in sections:
            for block in s["blocks"]:
                if block["type"] == BLOCK_TYPE_EXAMPLE:
                    worked_examples_legacy.append({
                        "title": s["title"],
                        "body": block["content"],
                    })

    # Extract key_takeaways from dedicated H2 section if available
    if not key_takeaways and "Key Takeaways" in h2_sections:
        key_takeaways = _extract_bullets_or_paragraphs(h2_sections["Key Takeaways"])

    # Ensure key_takeaways is never empty (schema requirement)
    if not key_takeaways:
        key_takeaways = ["Review all sections for complete understanding."]

    # Build summary: prefer recap prose, then dedicated Summary H2, then auto-generate
    summary = ""
    if "Summary" in h2_sections:
        summary = _extract_summary_candidate(h2_sections["Summary"])

    if not summary and recap_raw.strip():
        summary = _extract_summary_candidate(recap_raw)

    if not summary:
        summary = _build_summary(sections)

    if not summary:
        summary = f"Lesson covering {title} with {len(sections)} sections."

    guided_session = _build_guided_session(
        title=title,
        summary=summary,
        learning_objectives=learning_objectives,
        key_takeaways=key_takeaways,
        sections=sections,
        practice_problems=practice_problems,
    )

    lesson_ast = build_lesson_ast(
        {
            "metadata": metadata,
            "summary": summary,
            "learning_objectives": learning_objectives,
            "key_takeaways": key_takeaways,
            "practice_problems": practice_problems,
            "memory_aids": memory_aids,
            "exam_strategies": exam_strategies,
            "guided_session": guided_session,
            "sections": sections,
        }
    )
    screen_plan = compile_lesson_plan(lesson_ast).to_dict()
    metadata["screen_count"] = screen_plan["screen_count"]

    return {
        # Legacy-compatible fields (existing schema validation)
        "explanations": explanations_legacy,
        "worked_examples": worked_examples_legacy if worked_examples_legacy else [
            {"title": "See lesson sections", "body": "Worked examples are embedded within lesson sections."}
        ],
        "key_takeaways": key_takeaways,
        "summary": summary,
        # Enhanced fields for rich UI rendering
        "metadata": metadata,
        "learning_objectives": learning_objectives,
        "guided_session": guided_session,
        "table_of_contents": toc,
        "sections": sections,
        "practice_problems": practice_problems,
        "memory_aids": memory_aids,
        "exam_strategies": exam_strategies,
        "screen_plan": screen_plan,
        # Segment-and-gate fields (clerical-ability and future opt-in categories)
        "segments": segments,
        "is_segmented": is_segmented,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _split_h2(text: str) -> dict[str, str]:
    """Split text by H2 headings into {title: body} dict."""
    sections: dict[str, str] = {}
    current_h2: str | None = None
    buffer: list[str] = []

    for line in text.split("\n"):
        if line.startswith("## "):
            if current_h2 is not None:
                sections[current_h2] = "\n".join(buffer).strip()
            current_h2 = line[3:].strip()
            buffer = []
        else:
            buffer.append(line)

    if current_h2 is not None:
        sections[current_h2] = "\n".join(buffer).strip()

    return sections


def _split_h3(text: str) -> list[tuple[str, str]]:
    """Split text by H3 headings into ordered (title, body) pairs."""
    entries: list[tuple[str, str]] = []
    current_title: str | None = None
    buffer: list[str] = []

    for line in text.split("\n"):
        if line.startswith("### "):
            if current_title is not None:
                entries.append((current_title, "\n".join(buffer).strip()))
            current_title = line[4:].strip()
            buffer = []
        else:
            buffer.append(line)

    if current_title is not None:
        entries.append((current_title, "\n".join(buffer).strip()))

    return entries


def _build_heading_tree(text: str) -> list[dict[str, Any]]:
    """Build a nested heading tree from markdown content.

    The tree preserves heading order and nested structure without assuming
    any specific lesson format. Headings inside fenced code blocks are left
    untouched so examples and formulas are not misclassified.
    """
    root = {"level": 0, "title": "", "body_lines": [], "children": []}
    stack = [root]
    in_code_block = False

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            stack[-1]["body_lines"].append(line)
            continue

        heading_match = None if in_code_block else re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match:
            level = len(heading_match.group(1))
            node = {
                "level": level,
                "title": heading_match.group(2).strip(),
                "body_lines": [],
                "children": [],
            }
            while stack and stack[-1]["level"] >= level:
                stack.pop()
            if not stack:
                stack = [root]
            stack[-1]["children"].append(node)
            stack.append(node)
        else:
            stack[-1]["body_lines"].append(line)

    return root["children"]


def _heading_tree_to_markdown(node: dict[str, Any]) -> str:
    """Serialize one heading node back into markdown text."""
    parts: list[str] = []

    body = "\n".join(node.get("body_lines", [])).strip()
    if body:
        parts.append(body)

    for child in node.get("children", []):
        child_md = _heading_tree_to_markdown(child)
        heading_line = f'{"#" * child["level"]} {child["title"]}'
        parts.append("\n".join([heading_line, child_md]).strip() if child_md else heading_line)

    return "\n\n".join(part for part in parts if part.strip()).strip()


def _heading_tree_to_section(node: dict[str, Any]) -> dict[str, Any]:
    """Convert a heading node into the lesson-section JSON shape."""
    raw_text = _heading_tree_to_markdown(node)
    blocks = _parse_content_blocks(raw_text)
    difficulty = _detect_section_difficulty(raw_text)
    word_count = len(raw_text.split())

    section: dict[str, Any] = {
        "title": node.get("title", ""),
        "blocks": blocks,
        "difficulty": difficulty,
        "word_count": word_count,
        "estimated_reading_seconds": math.ceil(word_count / _WORDS_PER_MINUTE * 60),
    }

    child_sections = [
        _heading_tree_to_section(child)
        for child in node.get("children", [])
        if child.get("title", "").strip()
    ]
    if child_sections:
        section["subsections"] = child_sections

    return section


def _parse_nested_sections(text: str) -> list[dict[str, Any]]:
    """Parse nested headings within a lesson section into subsection JSON."""
    return [
        _heading_tree_to_section(node)
        for node in _build_heading_tree(text)
        if node.get("title", "").strip()
    ]


def _extract_summary_candidate(text: str) -> str:
    """Strip markdown scaffolding and return the first meaningful prose."""
    if not text.strip():
        return ""

    paragraphs: list[str] = []
    current: list[str] = []

    def flush_current() -> None:
        if not current:
            return
        paragraph = " ".join(current).strip()
        if paragraph:
            paragraphs.append(paragraph)
        current.clear()

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            flush_current()
            continue

        if stripped.startswith("#") or stripped.startswith("---") or stripped.startswith("|"):
            flush_current()
            continue

        if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s", stripped):
            flush_current()
            continue

        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
            if not stripped:
                continue

        current.append(re.sub(r"\s+", " ", stripped))

    flush_current()

    candidate = " ".join(paragraphs[:2]).strip()
    if not candidate:
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", candidate)
    if len(sentences) > 3:
        candidate = " ".join(sentences[:3])

    if len(candidate) > 500:
        candidate = candidate[:500].rsplit(" ", 1)[0]

    return candidate.strip()


def _extract_learning_objectives(
    h2_sections: dict[str, str],
    all_sections: list[tuple[str, str]],
) -> list[str]:
    """Extract learning objectives from dedicated objective sections."""
    sources: list[str] = []

    for title, body in h2_sections.items():
        lower = title.lower().strip()
        if "learning objective" in lower or lower in {"objective", "objectives"}:
            sources.append(body)

    for title, body in all_sections:
        lower = title.lower().strip()
        if "learning objective" in lower or lower in {"objective", "objectives"}:
            sources.append(body)

    objectives: list[str] = []
    for source in sources:
        objectives.extend(_extract_bullets_or_paragraphs(source))

    if not objectives:
        return []

    return _dedupe_nonempty(objectives)


def _build_guided_session(
    *,
    title: str,
    summary: str,
    learning_objectives: list[str],
    key_takeaways: list[str],
    sections: list[dict[str, Any]],
    practice_problems: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a bite-sized guided session outline for modern lesson UX."""
    objective = ""
    if learning_objectives:
        objective = learning_objectives[0]
    elif summary.strip():
        objective = summary.strip()

    must_know = _dedupe_nonempty((learning_objectives[:3] if learning_objectives else []) + key_takeaways[:4])
    if not must_know and summary.strip():
        must_know = [summary.strip()]

    steps: list[dict[str, Any]] = []
    if objective:
        steps.append({
            "index": 0,
            "kind": GUIDED_STEP_KIND_OBJECTIVE,
            "title": "Learning outcome",
            "summary": objective,
            "section_index": None,
            "estimated_reading_seconds": 0,
            "subsection_count": 0,
            "focus_tags": ["objective"],
        })

    for index, section in enumerate(sections):
        step_kind = _classify_guided_step_kind(section, index, len(sections))
        section_summary = _summarize_guided_section(section)
        if not section_summary:
            section_summary = _derive_section_preview(section)

        steps.append({
            "index": len(steps),
            "kind": step_kind,
            "title": section.get("title", ""),
            "summary": section_summary,
            "section_index": index,
            "estimated_reading_seconds": section.get("estimated_reading_seconds", 0),
            "subsection_count": len(section.get("subsections") or []),
            "focus_tags": _build_guided_focus_tags(section),
        })

    if summary.strip() or practice_problems:
        exit_summary = summary.strip()
        if not exit_summary:
            exit_summary = "Finish with the practice set, then revisit the key takeaways if needed."
        steps.append({
            "index": len(steps),
            "kind": GUIDED_STEP_KIND_EXIT,
            "title": "What to do next",
            "summary": exit_summary,
            "section_index": None,
            "estimated_reading_seconds": 0,
            "subsection_count": 0,
            "focus_tags": ["exit", "practice"],
        })

    return {
        "title": title,
        "objective": objective,
        "must_know": must_know,
        "steps": steps,
    }


def _classify_guided_step_kind(
    section: dict[str, Any],
    index: int,
    total_sections: int,
) -> str:
    """Map a lesson section to a guided-session step kind."""
    title = str(section.get("title", "")).lower().strip()
    block_types = {
        str(block.get("type", "")).lower()
        for block in section.get("blocks", [])
        if isinstance(block, dict)
    }

    if index == 0 and any(
        title.startswith(prefix)
        for prefix in ("introduction", "overview", "what is", "learning objective")
    ):
        return GUIDED_STEP_KIND_FOUNDATION
    if "learning objective" in title or title in {"objective", "objectives"}:
        return GUIDED_STEP_KIND_OBJECTIVE
    if "summary" in title or "recap" in title or "wrap up" in title:
        return GUIDED_STEP_KIND_SUMMARY
    if "practice" in title or "check your understanding" in title:
        return GUIDED_STEP_KIND_PRACTICE
    if "strategy" in title or "memory aid" in title or "mnemonic" in title:
        return GUIDED_STEP_KIND_STRATEGY
    if "warning" in title or "mistake" in title or "misconception" in title:
        return GUIDED_STEP_KIND_WARNING
    if "example" in title or BLOCK_TYPE_EXAMPLE in block_types:
        return GUIDED_STEP_KIND_EXAMPLE
    if "why" in title or "how" in title or "principle" in title or "rule" in title:
        return GUIDED_STEP_KIND_INSIGHT
    if "concept" in title or "analysis" in title or "technique" in title:
        return GUIDED_STEP_KIND_CONCEPT
    if index == total_sections - 1:
        return GUIDED_STEP_KIND_EXIT
    return GUIDED_STEP_KIND_CONCEPT if index > 0 else GUIDED_STEP_KIND_FOUNDATION


def _summarize_guided_section(section: dict[str, Any]) -> str:
    """Build a short, human-readable summary for a guided-session step."""
    text_parts: list[str] = []
    for block in section.get("blocks", []):
        if not isinstance(block, dict):
            continue
        block_type = str(block.get("type", ""))
        content = block.get("content", "")
        if block_type in {
            BLOCK_TYPE_PROSE,
            BLOCK_TYPE_TIP,
            BLOCK_TYPE_WARNING,
            BLOCK_TYPE_EXAMPLE,
            BLOCK_TYPE_LIST,
            BLOCK_TYPE_STEP_BY_STEP,
        } and isinstance(content, str):
            text_parts.append(content)

    summary = _extract_summary_candidate("\n\n".join(text_parts))
    if summary:
        return summary

    for block in section.get("blocks", []):
        if not isinstance(block, dict):
            continue
        content = block.get("content", "")
        if isinstance(content, str) and content.strip():
            return content.strip().split("\n", 1)[0][:240]

    return ""


def _derive_section_preview(section: dict[str, Any]) -> str:
    """Fallback preview used when a section has no obvious prose summary."""
    blocks = section.get("blocks", [])
    preview_parts: list[str] = []
    for block in blocks[:2]:
        if not isinstance(block, dict):
            continue
        content = block.get("content", "")
        if isinstance(content, str) and content.strip():
            preview_parts.append(content.strip().split("\n", 1)[0])
        elif isinstance(content, dict):
            preview_parts.append(str(content.get("summary") or content.get("text") or ""))
    preview = " ".join(part for part in preview_parts if part)
    return preview[:240].strip()


def _build_guided_focus_tags(section: dict[str, Any]) -> list[str]:
    """Derive small focus tags for chip-style UI treatment."""
    tags: list[str] = []
    title = str(section.get("title", "")).lower()
    block_types = {
        str(block.get("type", "")).lower()
        for block in section.get("blocks", [])
        if isinstance(block, dict)
    }

    if "example" in title or BLOCK_TYPE_EXAMPLE in block_types:
        tags.append("example")
    if "warning" in title or "mistake" in title or "misconception" in title or BLOCK_TYPE_WARNING in block_types:
        tags.append("warning")
    if "practice" in title or "check your understanding" in title or BLOCK_TYPE_CHECK_UNDERSTANDING in block_types:
        tags.append("practice")
    if "strategy" in title or "technique" in title:
        tags.append("strategy")
    if "summary" in title or "recap" in title:
        tags.append("summary")
    if "why" in title or "how" in title or "principle" in title or "rule" in title:
        tags.append("insight")
    if "analysis" in title or "concept" in title:
        tags.append("concept")
    if "learning objective" in title or title in {"objective", "objectives"}:
        tags.append("objective")

    if not tags:
        tags.append("lesson")

    return _dedupe_nonempty(tags)


def _dedupe_nonempty(items: list[str]) -> list[str]:
    """Remove blank entries while preserving order."""
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


def _classify_blockquote(stripped_bq: str, raw_bq: str) -> str:
    """Classify a blockquote callout by its label first, then by fallback cues."""
    first_line = next((line.strip() for line in stripped_bq.split("\n") if line.strip()), "")
    normalized = re.sub(r"^[^\w]+", "", first_line.lower()).replace("**", "").strip()
    raw_lower = raw_bq.lower()

    if normalized.startswith("misconception"):
        return BLOCK_TYPE_WARNING
    if normalized.startswith("why it fails"):
        return BLOCK_TYPE_WARNING
    if normalized.startswith("correct model"):
        return BLOCK_TYPE_TIP
    if normalized.startswith("why does this work"):
        return BLOCK_TYPE_TIP

    # Fallback cues for older authored lessons that rely on emoji or keyword hints
    if "🤔" in raw_bq or "tip" in raw_lower[:40] or "note" in raw_lower[:40] or "important" in raw_lower[:40]:
        return BLOCK_TYPE_TIP
    if "⚠️" in raw_bq or "warning" in raw_lower[:40] or "caution" in raw_lower[:40]:
        return BLOCK_TYPE_WARNING
    if "🧠" in raw_bq or "mnemonic" in raw_lower[:40] or "memory" in raw_lower[:40]:
        return BLOCK_TYPE_TIP

    return BLOCK_TYPE_EXAMPLE


def _parse_content_blocks(text: str) -> list[dict[str, Any]]:
    """Parse a section body into typed content blocks.

    Identifies: tables, code blocks, formulas, tips/warnings, examples,
    step-by-step procedures, and regular prose.
    """
    blocks: list[dict[str, Any]] = []
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # SVG block: <svg ...> ... </svg>
        if re.match(r"^\s*<svg[\s>]", line, re.IGNORECASE):
            svg_lines = [line]
            # Check if the SVG closes on the same line
            if "</svg>" in line.lower():
                blocks.append({"type": BLOCK_TYPE_SVG, "content": line.strip()})
                i += 1
                continue
            # Multi-line SVG: collect until closing </svg>
            i += 1
            while i < len(lines):
                svg_lines.append(lines[i])
                if "</svg>" in lines[i].lower():
                    i += 1
                    break
                i += 1
            blocks.append({"type": BLOCK_TYPE_SVG, "content": "\n".join(svg_lines).strip()})
            continue

        # Code block (``` fenced)
        if line.strip().startswith("```"):
            code_lines = []
            lang = line.strip()[3:].strip()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            content = "\n".join(code_lines)
            # Detect if it's a formula/equation or actual code
            block_type = BLOCK_TYPE_FORMULA if _is_formula(content) else BLOCK_TYPE_CODE
            blocks.append({"type": block_type, "content": content, "language": lang})
            continue

        # Table (lines starting with |)
        if line.strip().startswith("|") and i + 1 < len(lines) and "|" in lines[i + 1]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            table_data = _parse_table(table_lines)
            if table_data:
                blocks.append({"type": BLOCK_TYPE_TABLE, "content": table_data})
            continue

        # Tip/CSE Tip/Note patterns
        if re.match(r"^\*\*(CSE\s+)?Tip[:\s]", line.strip(), re.IGNORECASE) or \
           re.match(r"^\*\*Note[:\s]", line.strip(), re.IGNORECASE) or \
           re.match(r"^\*\*Important[:\s]", line.strip(), re.IGNORECASE):
            tip_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                tip_lines.append(lines[i])
                i += 1
            blocks.append({"type": BLOCK_TYPE_TIP, "content": "\n".join(tip_lines)})
            continue

        # Warning/Common mistake patterns
        if re.match(r"^\*\*(Common\s+)?(Mistake|Error|Warning|Caution)[:\s]", line.strip(), re.IGNORECASE):
            warn_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                warn_lines.append(lines[i])
                i += 1
            blocks.append({"type": BLOCK_TYPE_WARNING, "content": "\n".join(warn_lines)})
            continue

        # Check Your Understanding sub-heading within a section body
        # Handles "### Check Your Understanding" appearing inside H3 section text
        if re.match(r"^#{3,4}\s+Check Your Understanding", line, re.IGNORECASE):
            check_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("#"):
                check_lines.append(lines[i])
                i += 1
            checks = _extract_inline_checks("\n".join(check_lines))
            if checks:
                blocks.append({"type": BLOCK_TYPE_CHECK_UNDERSTANDING, "content": checks})
            continue

        # Blockquote callouts: classify label-first, then fall back to emoji/keyword
        if line.strip().startswith("> "):
            bq_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("> "):
                bq_lines.append(lines[i])
                i += 1
            bq_content = "\n".join(bq_lines)
            stripped_bq = "\n".join(l.lstrip("> ").rstrip() for l in bq_lines)
            block_type = _classify_blockquote(stripped_bq, bq_content)
            blocks.append({"type": block_type, "content": stripped_bq})
            continue

        # Example blocks (lines starting with **Example**)
        if re.match(r"^\*\*Example", line.strip()):
            example_lines = [line]
            i += 1
            blank_count = 0
            while i < len(lines):
                next_line = lines[i]
                # Hard stops: new heading, new Example block, fenced code opens
                if (next_line.startswith("#") or
                    re.match(r"^\*\*(Example|Tip|Note|CSE|Common|Warning|Error)", next_line.strip()) or
                    next_line.strip().startswith("```") or
                    next_line.strip().startswith("> ") or
                    re.match(r"^#{3,4}\s+Check Your Understanding", next_line, re.IGNORECASE)):
                    break
                # Allow up to 2 consecutive blank lines inside the example
                if not next_line.strip():
                    blank_count += 1
                    if blank_count > 2:
                        break
                    example_lines.append(next_line)
                else:
                    blank_count = 0
                    example_lines.append(next_line)
                i += 1
            # Strip trailing blank lines from the captured content
            while example_lines and not example_lines[-1].strip():
                example_lines.pop()
            blocks.append({"type": BLOCK_TYPE_EXAMPLE, "content": "\n".join(example_lines)})
            continue

        # Step-by-step (lines starting with Step 1, Step 2, etc.)
        if re.match(r"^(Step\s+\d|step\s+\d)", line.strip()):
            step_lines = [line]
            i += 1
            while i < len(lines) and (
                re.match(r"^(Step\s+\d|step\s+\d)", lines[i].strip()) or
                (lines[i].strip() and not lines[i].startswith("#") and not lines[i].strip().startswith("|"))
            ):
                step_lines.append(lines[i])
                i += 1
            blocks.append({"type": BLOCK_TYPE_STEP_BY_STEP, "content": "\n".join(step_lines)})
            continue

        # Bullet/numbered list
        if re.match(r"^(\d+\.|[-*])\s", line.strip()):
            list_lines = [line]
            i += 1
            while i < len(lines) and (
                re.match(r"^(\d+\.|[-*])\s", lines[i].strip()) or
                (lines[i].startswith("  ") and lines[i].strip())
            ):
                list_lines.append(lines[i])
                i += 1
            blocks.append({"type": BLOCK_TYPE_LIST, "content": "\n".join(list_lines)})
            continue

        # Regular prose — collect consecutive non-empty, non-special lines
        if line.strip():
            prose_lines = [line]
            i += 1
            while i < len(lines):
                next_line = lines[i]
                # Stop at empty lines, headings, tables, code blocks, special patterns, SVG
                if (not next_line.strip() or
                    next_line.startswith("#") or
                    next_line.strip().startswith("|") or
                    next_line.strip().startswith("```") or
                    re.match(r"^\s*<svg[\s>]", next_line, re.IGNORECASE) or
                    re.match(r"^\*\*(Example|Tip|Note|CSE|Common|Warning|Error)", next_line.strip()) or
                    next_line.strip().startswith("> ") or
                    re.match(r"^(Step\s+\d)", next_line.strip()) or
                    re.match(r"^(\d+\.|[-*])\s", next_line.strip())):
                    break
                prose_lines.append(next_line)
                i += 1
            blocks.append({"type": BLOCK_TYPE_PROSE, "content": "\n".join(prose_lines)})
            continue

        # Empty line — skip
        i += 1

    return blocks


def _is_formula(content: str) -> bool:
    """Heuristic: is this code block actually a math formula/computation?"""
    # If it contains arithmetic operators and numbers but no programming keywords
    math_indicators = ["+", "-", "×", "÷", "=", "→", "carry", "borrow"]
    code_indicators = ["def ", "class ", "import ", "return ", "if ", "for ", "while "]

    has_math = any(ind in content for ind in math_indicators)
    has_code = any(ind in content for ind in code_indicators)

    return has_math and not has_code


def _parse_table(lines: list[str]) -> dict[str, Any] | None:
    """Parse markdown table lines into structured data.

    Ensures all rows have the same number of cells as the header
    to prevent 'undefined' values in the frontend.
    """
    if len(lines) < 2:
        return None

    rows: list[list[str]] = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    if len(rows) < 2:
        return None

    # Second row is typically the separator (---|---|---)
    # Check if it's a separator row
    header = rows[0]
    col_count = len(header)

    if all(re.match(r"^[-:]+$", cell.strip()) for cell in rows[1] if cell.strip()):
        data_rows = rows[2:]
    else:
        data_rows = rows[1:]

    # Normalize: pad short rows with empty strings, trim long rows
    normalized_rows: list[list[str]] = []
    for row in data_rows:
        if len(row) < col_count:
            row = row + [""] * (col_count - len(row))
        elif len(row) > col_count:
            row = row[:col_count]
        normalized_rows.append(row)

    return {
        "headers": header,
        "rows": normalized_rows,
    }


def _detect_section_difficulty(text: str) -> list[str]:
    """Detect which difficulty levels are covered in a section."""
    difficulties = []
    lower = text.lower()
    if "**easy" in lower or "easy:" in lower or "(easy)" in lower:
        difficulties.append("easy")
    if "**medium" in lower or "medium:" in lower or "(medium)" in lower:
        difficulties.append("medium")
    if "**hard" in lower or "hard:" in lower or "(hard)" in lower:
        difficulties.append("hard")
    return difficulties


def _parse_practice_problems(text: str) -> list[dict[str, Any]]:
    """Parse the Mini Practice Set into interactive quiz items."""
    if not text.strip():
        return []

    problems: list[dict[str, Any]] = []

    # Pattern: **N.** or N. followed by question, then **Answer:** line
    # Split by problem number patterns
    problem_pattern = re.compile(r"^\*\*(\d+)\.\*\*\s*(.+?)$", re.MULTILINE)
    answer_pattern = re.compile(r"^\*\*Answer:\*\*\s*(.+?)$", re.MULTILINE)
    explanation_pattern = re.compile(r"^\*\*Explanation:\*\*\s*(.+?)$", re.MULTILINE)

    # Try structured format first (numbered with bold)
    matches = list(problem_pattern.finditer(text))

    if matches:
        for idx, match in enumerate(matches):
            num = match.group(1)
            question = match.group(2).strip()

            # Find the region between this problem and the next
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            region = text[start:end]

            answer = ""
            explanation = ""

            ans_match = answer_pattern.search(region)
            if ans_match:
                answer = ans_match.group(1).strip()

            exp_match = explanation_pattern.search(region)
            if exp_match:
                explanation = exp_match.group(1).strip()

            problems.append({
                "number": int(num),
                "question": question,
                "answer": answer,
                "explanation": explanation,
                "difficulty": _guess_problem_difficulty(idx, len(matches)),
            })
    else:
        # Try simpler format: **1.** question \n answer on next line
        simple_pattern = re.compile(
            r"^\*\*(\d+)\.\*\*\s*(.+?)(?:\n|$)", re.MULTILINE
        )
        simple_matches = list(simple_pattern.finditer(text))

        if not simple_matches:
            # Even simpler: just numbered lines
            line_pattern = re.compile(r"^(\d+)\.\s*(.+?)$", re.MULTILINE)
            simple_matches = list(line_pattern.finditer(text))

        for idx, match in enumerate(simple_matches):
            num = match.group(1)
            question = match.group(2).strip()

            # Look for answer in subsequent lines
            start = match.end()
            end = simple_matches[idx + 1].start() if idx + 1 < len(simple_matches) else len(text)
            region = text[start:end].strip()

            answer = ""
            explanation = ""

            # Look for "Answer:" or just the next non-empty line
            for line in region.split("\n"):
                line = line.strip()
                if line.lower().startswith("answer:"):
                    answer = line.split(":", 1)[1].strip()
                elif line.lower().startswith("explanation:"):
                    explanation = line.split(":", 1)[1].strip()
                elif not answer and line and not line.startswith("*"):
                    answer = line

            problems.append({
                "number": int(num),
                "question": question,
                "answer": answer,
                "explanation": explanation,
                "difficulty": _guess_problem_difficulty(idx, len(simple_matches)),
            })

    return problems


def _guess_problem_difficulty(index: int, total: int) -> str:
    """Guess difficulty based on position (problems typically go easy→hard)."""
    if total <= 3:
        return "medium"
    third = total / 3
    if index < third:
        return "easy"
    elif index < 2 * third:
        return "medium"
    else:
        return "hard"


def _extract_bullets_or_paragraphs(text: str) -> list[str]:
    """Extract bullet points or meaningful paragraphs from text."""
    if not text.strip():
        return []

    items: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            items.append(stripped[2:].strip())
        elif stripped.startswith("✅ "):
            items.append(stripped[2:].strip())
        elif re.match(r"^\d+\.\s", stripped):
            items.append(re.sub(r"^\d+\.\s*", "", stripped))

    # If no bullets found, split by paragraphs
    if not items:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        items = [p for p in paragraphs if len(p) > 10]

    return items


def _extract_checklist(text: str) -> list[str]:
    """Extract checklist items (✅ prefixed lines)."""
    if not text.strip():
        return []

    items: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("✅"):
            # Remove the checkmark and any trailing whitespace
            item = stripped.lstrip("✅").strip()
            if item:
                items.append(item)
        elif stripped.startswith("- "):
            items.append(stripped[2:].strip())

    return items


def _blocks_to_markdown(blocks: list[dict[str, Any]]) -> str:
    """Convert content blocks back to markdown for legacy compatibility."""
    parts: list[str] = []
    for block in blocks:
        if block["type"] == BLOCK_TYPE_CODE or block["type"] == BLOCK_TYPE_FORMULA:
            lang = block.get("language", "")
            parts.append(f"```{lang}\n{block['content']}\n```")
        elif block["type"] == BLOCK_TYPE_SVG:
            parts.append(block["content"])
        elif block["type"] == BLOCK_TYPE_TABLE:
            table = block["content"]
            if table and "headers" in table:
                col_count = len(table["headers"])
                table_lines = []
                table_lines.append("| " + " | ".join(table["headers"]) + " |")
                table_lines.append("| " + " | ".join(["---"] * col_count) + " |")
                for row in table["rows"]:
                    cells = [(c if c else "") for c in row]
                    while len(cells) < col_count:
                        cells.append("")
                    table_lines.append("| " + " | ".join(cells[:col_count]) + " |")
                parts.append("\n".join(table_lines))
        elif block["type"] == BLOCK_TYPE_CHECK_UNDERSTANDING:
            # Reconstruct check_understanding blocks as markdown Q&A lines
            checks = block["content"]
            if isinstance(checks, list):
                lines = ["**Check Your Understanding**"]
                for i, check in enumerate(checks, start=1):
                    if isinstance(check, dict):
                        q = check.get("question", "")
                        a = check.get("answer", "")
                        r = check.get("rationale", "")
                        line = f"**{i}.** {q} → **{a}**"
                        if r:
                            line += f" ({r})"
                        lines.append(line)
                parts.append("\n".join(lines))
        else:
            content = block["content"]
            if isinstance(content, str):
                parts.append(content)
    return "\n\n".join(parts)


def _build_summary(sections: list[dict[str, Any]]) -> str:
    """Build a summary from the first section's first prose block."""
    for section in sections[:3]:
        for block in section["blocks"]:
            if block["type"] == BLOCK_TYPE_PROSE and len(block["content"]) > 50:
                # Take first 2-3 sentences
                sentences = re.split(r"(?<=[.!?])\s+", block["content"])
                summary = " ".join(sentences[:3])
                if len(summary) > 300:
                    summary = " ".join(sentences[:2])
                return summary
    return ""


# ---------------------------------------------------------------------------
# Inline check extraction
# ---------------------------------------------------------------------------

def _extract_inline_checks(text: str) -> list[dict[str, Any]]:
    """Extract Q&A pairs from a 'Check Your Understanding' block.

    Supports two formats found in clerical-ability lessons:

    Format 1 — bold numbered items with arrow answers:
        **1.** Are "Gonzales" and "Gonzalez" identical? → **No** (reason)

    Format 2 — plain numbered lines with answer on same line after →:
        1. What type of error is "Reyes" → "Reyse"? → **Transposition**

    Returns a list of {"question": str, "answer": str, "rationale": str} dicts.
    """
    if not text.strip():
        return []

    checks: list[dict[str, Any]] = []

    # Pattern: optional bold markers, number, question text, → answer, optional (rationale)
    # Matches both "**1.**" and "1." prefixes
    line_pattern = re.compile(
        r"^\*{0,2}(\d+)\.\*{0,2}\s+"   # number
        r"(.+?)"                          # question text (non-greedy)
        r"\s*→\s*"                        # arrow separator
        r"\*{0,2}(.+?)\*{0,2}"           # answer (strip bold markers)
        r"(?:\s+\(([^)]+)\))?\s*$",       # optional (rationale)
        re.MULTILINE,
    )

    for match in line_pattern.finditer(text):
        question = match.group(2).strip()
        answer = match.group(3).strip()
        rationale = match.group(4).strip() if match.group(4) else ""
        if question and answer:
            checks.append({
                "question": question,
                "answer": answer,
                "rationale": rationale,
            })

    return checks


# ---------------------------------------------------------------------------
# Segment builder
# ---------------------------------------------------------------------------

def _is_break_section(title: str) -> bool:
    """Return True if this section title always starts a new segment."""
    lower = title.lower().strip()
    return any(lower == b or lower.startswith(b) for b in _SEGMENT_BREAK_TITLES)


def _build_segments(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Group sections into timed segments of ~_SEGMENT_TARGET_WORDS words.

    Rules:
    1. Preamble sections (Introduction, Why Tested, Learning Objectives,
       Common Mistakes) are always grouped into the first segment regardless
       of word count — they frame what follows.
    2. Content sections accumulate until word count would exceed the target,
       then a new segment begins.
    3. Certain section titles (Exam Strategies, Memory Aids, Guided Practice,
       Mini Practice Set, etc.) always start a new segment — they represent
       a mode shift from reading to applying.
    4. Each segment's checks are extracted from check_understanding blocks
       embedded within its sections, then removed from the section blocks so
       they don't render twice.

    Returns a list of segment dicts:
        {
            "index": int,
            "sections": [...],   # LessonSection dicts (blocks stripped of checks)
            "estimated_minutes": int,
            "checks": [...]      # InlineCheck dicts
        }
    """
    _preamble_patterns = (
        "introduction",
        "why ",
        "learning objective",
        "common mistakes",
        "focus areas",
    )

    def is_preamble(title: str) -> bool:
        lower = title.lower()
        return any(lower.startswith(p) or lower == p.strip() for p in _preamble_patterns)

    segments: list[dict[str, Any]] = []
    current_sections: list[dict[str, Any]] = []
    current_words = 0
    current_checks: list[dict[str, Any]] = []

    def _flush(secs: list[dict[str, Any]], chks: list[dict[str, Any]], words: int) -> None:
        if not secs:
            return
        minutes = max(1, math.ceil(words / _WORDS_PER_MINUTE))
        segments.append({
            "index": len(segments),
            "sections": secs,
            "estimated_minutes": minutes,
            "checks": chks,
        })

    def _strip_and_collect_checks(section: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        """Pull check_understanding blocks out of a section's blocks.

        Returns (clean_section, extracted_checks).
        The clean_section has those blocks removed so they won't render inline —
        the segment gate panel renders them instead.
        """
        clean_blocks = []
        extracted: list[dict[str, Any]] = []
        for block in section.get("blocks", []):
            if block["type"] == BLOCK_TYPE_CHECK_UNDERSTANDING:
                if isinstance(block["content"], list):
                    extracted.extend(block["content"])
            else:
                clean_blocks.append(block)
        clean_section = {**section, "blocks": clean_blocks}
        return clean_section, extracted

    for section in sections:
        title = section.get("title", "")
        word_count = section.get("word_count", 0)

        # "Check Your Understanding" sections: their content becomes gate checks
        # for the *current* segment rather than a segment of their own.
        if title.lower().strip() == "check your understanding":
            raw_text = "\n".join(
                block["content"]
                for block in section.get("blocks", [])
                if block["type"] in ("prose", "list") and isinstance(block["content"], str)
            )
            extracted = _extract_inline_checks(raw_text)
            if extracted:
                current_checks.extend(extracted)
            continue

        # Strip check_understanding blocks early so the result is available
        # for all branches below.
        clean_section, section_checks = _strip_and_collect_checks(section)

        # Mode-shift titles always flush the current reading segment, then the
        # break sections themselves accumulate together into a single "Practice
        # & Review" tail segment (prevents micro-segments of 1 min each).
        if _is_break_section(title):
            # Only flush if we have non-break content accumulated
            current_is_all_breaks = all(
                _is_break_section(s.get("title", "")) for s in current_sections
            ) if current_sections else True

            if not current_is_all_breaks:
                _flush(current_sections, current_checks, current_words)
                current_sections = [clean_section]
                current_words = word_count
                current_checks = list(section_checks)
            else:
                # Already in a break-section accumulation — keep collecting
                current_sections.append(clean_section)
                current_words += word_count
                current_checks.extend(section_checks)
            continue

        if not current_sections:
            # Starting a new segment — always add regardless of word count
            current_sections.append(clean_section)
            current_words += word_count
            current_checks.extend(section_checks)
        elif is_preamble(title) and len(segments) == 0:
            # Preamble sections stay in segment 0 even if they exceed target
            current_sections.append(clean_section)
            current_words += word_count
            current_checks.extend(section_checks)
        elif current_words + word_count > _SEGMENT_TARGET_WORDS and not is_preamble(title):
            # Would exceed target — flush and start fresh
            _flush(current_sections, current_checks, current_words)
            current_sections = [clean_section]
            current_words = word_count
            current_checks = list(section_checks)
        else:
            current_sections.append(clean_section)
            current_words += word_count
            current_checks.extend(section_checks)

    # Flush the final in-progress segment
    _flush(current_sections, current_checks, current_words)

    return segments
