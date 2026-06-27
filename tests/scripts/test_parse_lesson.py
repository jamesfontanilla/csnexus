from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.parse_lesson import parse_lesson_markdown


def read_lesson(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def find_section(sections: list[dict[str, object]], title: str) -> dict[str, object]:
    for section in sections:
        if section.get("title") == title:
            return section
    raise AssertionError(f"Section not found: {title}")


def test_parse_lesson_preserves_nested_subsections_and_summary() -> None:
    content = read_lesson(
        "data/seed/lessons/verbal-ability/grammar/subject-verb-agreement/lesson.md"
    )

    result = parse_lesson_markdown(content)

    assert result["metadata"]["title"] == "Subject-Verb Agreement"
    assert result["summary"].startswith("Subject-verb agreement is one of the most important grammar topics")
    assert not result["summary"].lstrip().startswith("###")

    section = find_section(result["sections"], "4.3 Compound Subjects")
    subsections = section.get("subsections") or []
    subsection_titles = [subsection.get("title") for subsection in subsections]

    assert "Rule 1: Subjects Joined by \"And\" — Plural Verb" in subsection_titles
    assert "Exceptions to the \"And\" Rule" in subsection_titles

    exceptions = find_section(subsections, "Exceptions to the \"And\" Rule")
    nested_titles = [child.get("title") for child in (exceptions.get("subsections") or [])]
    assert "Exception 1 — Same Person or Thing" in nested_titles


def test_parse_lesson_keeps_segmented_clerical_lesson_intact() -> None:
    content = read_lesson(
        "data/seed/lessons/clerical-ability/alphabetical-filing/basic-alphabetizing/lesson.md"
    )

    result = parse_lesson_markdown(content, category="clerical-ability")

    assert result["is_segmented"] is True
    assert result["metadata"]["segment_count"] == 3
    assert result["metadata"]["section_count"] == len(result["sections"])
    assert find_section(result["sections"], "4.1 Understanding Alphabetical Order")


def test_parse_lesson_classifies_common_callout_labels() -> None:
    content = read_lesson(
        "data/seed/lessons/analytical-ability/word-analogy/synonym-and-antonym-analogies/lesson.md"
    )

    result = parse_lesson_markdown(content)
    section = find_section(result["sections"], "4.1 What Is a Word Analogy?")
    blocks = section["blocks"]

    assert any(
        block["type"] == "tip" and "Why does this work" in str(block["content"])
        for block in blocks
    )
    assert any(
        block["type"] == "warning" and "Misconception" in str(block["content"])
        for block in blocks
    )
    assert any(
        block["type"] == "warning" and "Why it fails" in str(block["content"])
        for block in blocks
    )
    assert any(
        block["type"] == "tip" and "Correct model" in str(block["content"])
        for block in blocks
    )
