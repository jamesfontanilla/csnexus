"""Enhanced lesson markdown parser.

Extracts rich structured content from lesson.md files for frontend rendering:
- Sections with table-of-contents metadata
- Practice problems as interactive quiz items
- Tables, formulas, tips, warnings, and memory aids as typed content blocks
- Difficulty-tagged examples
- Estimated reading time and section counts
- Key takeaways and exam strategies extracted into dedicated fields

The output JSON is designed so a frontend can render each content type
with a distinct UI component rather than dumping raw markdown.
"""

from __future__ import annotations

import math
import re
from typing import Any


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

# Average reading speed in words per minute for educational content
_WORDS_PER_MINUTE = 200


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def parse_lesson_markdown(md_text: str) -> dict[str, Any]:
    """Parse lesson markdown into a rich, UI-friendly JSON structure.

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
        sections.append({
            "title": sec_title,
            "blocks": blocks,
            "difficulty": difficulty,
            "word_count": word_count,
            "estimated_reading_seconds": math.ceil(word_count / _WORDS_PER_MINUTE * 60),
        })

    # Parse practice problems
    practice_problems = _parse_practice_problems(practice_raw)

    # Parse memory aids as bullet list
    memory_aids = _extract_bullets_or_paragraphs(memory_aids_raw)

    # Parse exam strategies
    exam_strategies = _extract_bullets_or_paragraphs(exam_strategies_raw)

    # Parse key takeaways from mastery checklist or recap
    key_takeaways = _extract_checklist(mastery_raw) or _extract_bullets_or_paragraphs(recap_raw)

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

    metadata = {
        "title": title,
        "estimated_reading_minutes": estimated_reading_minutes,
        "section_count": len(sections),
        "has_practice_problems": len(practice_problems) > 0,
        "practice_problem_count": len(practice_problems),
        "difficulty_distribution": difficulty_dist,
        "total_word_count": total_words,
    }

    # Build the legacy-compatible fields too (explanations/worked_examples)
    # so existing consumers don't break
    explanations_legacy = [
        {"heading": s["title"], "body": _blocks_to_markdown(s["blocks"])}
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
    if recap_raw.strip():
        # Try to get prose from recap, not tables or horizontal rules
        recap_lines = recap_raw.strip().split("\n")
        prose_parts = []
        for line in recap_lines:
            stripped = line.strip()
            if (stripped and
                not stripped.startswith("|") and
                not stripped.startswith("---") and
                len(stripped) > 5):
                prose_parts.append(stripped)
        if prose_parts:
            summary = " ".join(prose_parts[:3])

    if not summary and "Summary" in h2_sections:
        summary_text = h2_sections["Summary"].strip()
        if summary_text:
            # Take prose lines, skip tables
            summary_lines = [
                l for l in summary_text.split("\n")
                if l.strip() and not l.strip().startswith("|")
            ]
            summary = " ".join(summary_lines[:3])[:500]

    if not summary:
        summary = _build_summary(sections)

    if not summary:
        summary = f"Lesson covering {title} with {len(sections)} sections."

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
        "table_of_contents": toc,
        "sections": sections,
        "practice_problems": practice_problems,
        "memory_aids": memory_aids,
        "exam_strategies": exam_strategies,
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

        # Blockquote callouts (> 💡, > ⚠️, > 🧠) — classify by emoji/keyword
        if line.strip().startswith("> "):
            bq_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("> "):
                bq_lines.append(lines[i])
                i += 1
            bq_content = "\n".join(bq_lines)
            # Strip the "> " prefix for content storage
            stripped_bq = "\n".join(l.lstrip("> ").rstrip() for l in bq_lines)
            # Classify based on emoji or keywords
            if "💡" in bq_content or "tip" in bq_content.lower()[:40]:
                blocks.append({"type": BLOCK_TYPE_TIP, "content": stripped_bq})
            elif "⚠️" in bq_content or "warning" in bq_content.lower()[:40] or "caution" in bq_content.lower()[:40]:
                blocks.append({"type": BLOCK_TYPE_WARNING, "content": stripped_bq})
            elif "🧠" in bq_content or "mnemonic" in bq_content.lower()[:40] or "memory" in bq_content.lower()[:40]:
                blocks.append({"type": BLOCK_TYPE_TIP, "content": stripped_bq})
            else:
                blocks.append({"type": BLOCK_TYPE_EXAMPLE, "content": stripped_bq})
            continue

        # Example blocks (lines starting with **Example**)
        if re.match(r"^\*\*Example", line.strip()):
            example_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                # Continue collecting until empty line or new heading
                example_lines.append(lines[i])
                i += 1
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
                # Stop at empty lines, headings, tables, code blocks, special patterns
                if (not next_line.strip() or
                    next_line.startswith("#") or
                    next_line.strip().startswith("|") or
                    next_line.strip().startswith("```") or
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
        elif block["type"] == BLOCK_TYPE_TABLE:
            table = block["content"]
            if table and "headers" in table:
                header_line = "| " + " | ".join(table["headers"]) + " |"
                sep_line = "| " + " | ".join(["---"] * len(table["headers"])) + " |"
                parts.append(header_line)
                parts.append(sep_line)
                col_count = len(table["headers"])
                for row in table["rows"]:
                    # Ensure row has correct number of string cells
                    cells = [(c if c else "") for c in row]
                    while len(cells) < col_count:
                        cells.append("")
                    parts.append("| " + " | ".join(cells[:col_count]) + " |")
        else:
            parts.append(block["content"])
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
