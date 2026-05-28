"""Validate lesson proper quality against research-backed refinement rules.

This complements scripts/validate_enhanced_lessons.py. The older validator checks
section presence; this one checks quality artifacts, domain-fit wording, line
counts, and parser compatibility.

Usage:
    python scripts/validate_lesson_proper_quality.py
    python scripts/validate_lesson_proper_quality.py --lesson data/seed/lessons/verbal-ability/grammar/subject-verb-agreement/lesson.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.parse_lesson import parse_lesson_markdown

LESSONS_DIR = PROJECT_ROOT / "data" / "seed" / "lessons"


PLACEHOLDER_PATTERNS = [
    re.compile(r"\[Brief rationale\]", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"^\s*> \?\?", re.MULTILINE),
]

GRAMMAR_BANNED_PATTERNS = [
    re.compile(r"set up the equation", re.IGNORECASE),
    re.compile(r"computed answer", re.IGNORECASE),
    re.compile(r"\bpart-whole\b", re.IGNORECASE),
    re.compile(r"\binverse proportion\b", re.IGNORECASE),
]

MATH_BANNED_PATTERNS = [
    re.compile(r"\bantecedent\b", re.IGNORECASE),
    re.compile(r"\bsubordinate clause\b", re.IGNORECASE),
    re.compile(r"\bmodifier phrase\b", re.IGNORECASE),
]


def line_number(content: str, pos: int) -> int:
    return content.count("\n", 0, pos) + 1


def lesson_domain(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    if "grammar" in parts:
        return "grammar"
    if "numerical-ability" in parts:
        return "math"
    if "analytical-ability" in parts:
        return "analytical"
    if "verbal-ability" in parts:
        return "verbal"
    return "general"


def count_which_method_items(content: str) -> int:
    match = re.search(
        r"^###\s+(?:Which Method\?|Discrimination Practice)\s*$(.*?)(^###\s+|^##\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return 0

    body = match.group(1)
    numbered = len(re.findall(r"^\s*(?:\*\*)?\d+[\.)]", body, re.MULTILINE))
    bullets = len(re.findall(r"^\s*[-*]\s+\S", body, re.MULTILINE))
    return max(numbered, bullets)


def has_faded_practice(content: str) -> bool:
    match = re.search(
        r"^###\s+Guided Practice\s*$(.*?)(^###\s+|^##\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return False
    body = match.group(1)
    return bool(
        re.search(r"_____|blank|complete the missing|fill in|step\s+\d+:", body, re.IGNORECASE)
    )


def parser_failures(content: str) -> list[str]:
    failures: list[str] = []
    try:
        parsed: dict[str, Any] = parse_lesson_markdown(content)
    except Exception as exc:
        return [f"Parser error: {exc}"]

    for key in ("explanations", "worked_examples", "key_takeaways", "summary"):
        value = parsed.get(key)
        if not value:
            failures.append(f"Parser output missing or empty: {key}")
    return failures


def pattern_failures(path: Path, content: str) -> list[str]:
    failures: list[str] = []
    lines = content.splitlines()

    line_count = len(lines)
    if line_count < 800:
        failures.append(f"Line count below spec: {line_count} < 800")
    if line_count > 2000:
        failures.append(f"Line count above spec: {line_count} > 2000")

    why_count = len(re.findall(r"Why does this work\?", content, re.IGNORECASE))
    if why_count < 2:
        failures.append(f"Need at least 2 elaborative callouts; found {why_count}")

    misconception_count = len(re.findall(r"Misconception:", content, re.IGNORECASE))
    if misconception_count < 2:
        failures.append(f"Need at least 2 misconception blocks; found {misconception_count}")

    for heading in (
        "Guided Practice",
        "Which Method?",
        "Before You Practice",
        "Connections",
        "Mastery Checklist",
    ):
        if not re.search(rf"^###\s+{re.escape(heading)}\s*$", content, re.MULTILINE):
            failures.append(f"Missing section: {heading}")

    if not has_faded_practice(content):
        failures.append("Guided Practice lacks faded-example cues")

    which_items = count_which_method_items(content)
    if which_items < 6:
        failures.append(f"Which Method? should include at least 6 items; found {which_items}")

    for pattern in PLACEHOLDER_PATTERNS:
        for match in pattern.finditer(content):
            failures.append(
                f"Placeholder/artifact at line {line_number(content, match.start())}: {match.group(0)}"
            )

    domain = lesson_domain(path)
    domain_patterns = []
    if domain == "grammar":
        domain_patterns = GRAMMAR_BANNED_PATTERNS
    elif domain == "math":
        domain_patterns = MATH_BANNED_PATTERNS

    for pattern in domain_patterns:
        for match in pattern.finditer(content):
            failures.append(
                f"Domain-mismatched wording at line {line_number(content, match.start())}: {match.group(0)}"
            )

    return failures


def validate_lesson(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    failures = pattern_failures(path, content)
    failures.extend(parser_failures(content))
    return failures


def discover_lessons(lesson: str | None) -> list[Path]:
    if lesson:
        path = Path(lesson)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return [path]
    return sorted(LESSONS_DIR.rglob("lesson.md"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", help="Validate a single lesson.md file")
    args = parser.parse_args()

    lesson_paths = discover_lessons(args.lesson)
    results = {path: validate_lesson(path) for path in lesson_paths}

    passing = sum(1 for failures in results.values() if not failures)
    failing = len(results) - passing

    print("=" * 58)
    print("  Lesson Proper Quality Validation Report")
    print("=" * 58)
    print(f"Total lessons: {len(results)}")
    print(f"Passing: {passing}")
    print(f"Failing: {failing}")
    print()

    if failing:
        print("FAILURES:")
        for path, failures in results.items():
            if not failures:
                continue
            rel = path.relative_to(PROJECT_ROOT)
            print(f"  {rel}")
            for failure in failures:
                print(f"    - {failure}")
            print()

    return 0 if failing == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
