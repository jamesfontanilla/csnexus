"""Validate enhanced lesson files for structural compliance.

Checks all lesson.md files under data/seed/lessons/ for the presence of
required pedagogical sections and verifies parser compatibility.

Usage:
    python scripts/validate_enhanced_lessons.py
"""

import re
import sys
from pathlib import Path
from typing import Any

# Ensure the project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.parse_lesson import parse_lesson_markdown

LESSONS_DIR = PROJECT_ROOT / "data" / "seed" / "lessons"


def discover_lesson_files(base_dir: Path) -> list[Path]:
    """Find all lesson.md files under the given directory."""
    return sorted(base_dir.rglob("lesson.md"))


def check_required_sections(content: str) -> list[str]:
    """Check for required enhanced sections in the markdown content.

    Returns a list of failure messages for missing/insufficient sections.
    """
    failures: list[str] = []

    # Check Your Understanding (â‰¥1)
    cyu_count = len(re.findall(r"^###\s+Check Your Understanding", content, re.MULTILINE))
    if cyu_count < 1:
        failures.append("Missing: Check Your Understanding (found 0, need â‰¥1)")

    # Elaborative Interrogation (â‰¥1) â€” detected by "> ðŸ¤”" blockquote
    ei_count = len(re.findall(r"^>\s*.*Why does this work\?", content, re.MULTILINE))
    if ei_count < 1:
        failures.append("Missing: Elaborative Interrogation (found 0, need â‰¥1)")

    # Misconception Confrontation (â‰¥2) â€” detected by "> âš ï¸" blockquote
    mc_count = len(re.findall(r"^>\s*.*Misconception", content, re.MULTILINE))
    if mc_count < 2:
        failures.append(
            f"Missing: Misconception Confrontation (found {mc_count}, need â‰¥2)"
        )

    # Guided Practice heading
    if not re.search(r"^###\s+Guided Practice", content, re.MULTILINE):
        failures.append("Missing: Guided Practice")

    # Which Method? or Discrimination Practice heading
    if not re.search(
        r"^###\s+(Which Method\?|Discrimination Practice)", content, re.MULTILINE
    ):
        failures.append("Missing: Which Method? / Discrimination Practice")

    # Before You Practice heading
    if not re.search(r"^###\s+Before You Practice", content, re.MULTILINE):
        failures.append("Missing: Before You Practice")

    # Connections heading
    if not re.search(r"^###\s+Connections", content, re.MULTILINE):
        failures.append("Missing: Connections")

    # Mastery Checklist heading
    if not re.search(r"^###\s+Mastery Checklist", content, re.MULTILINE):
        failures.append("Missing: Mastery Checklist")

    return failures


def check_parser_output(content: str) -> list[str]:
    """Run parse_lesson_markdown() and verify non-empty output fields.

    Returns a list of failure messages for parser issues.
    """
    failures: list[str] = []

    try:
        result: dict[str, Any] = parse_lesson_markdown(content)
    except Exception as e:
        failures.append(f"Parser error: {e}")
        return failures

    if not result.get("explanations"):
        failures.append("Parser error: empty explanations")

    if not result.get("worked_examples"):
        failures.append("Parser error: empty worked_examples")

    if not result.get("key_takeaways"):
        failures.append("Parser error: empty key_takeaways")

    summary = result.get("summary", "")
    if not summary or not summary.strip():
        failures.append("Parser error: empty summary")

    return failures


def validate_lesson(file_path: Path) -> list[str]:
    """Validate a single lesson file. Returns list of failure messages."""
    content = file_path.read_text(encoding="utf-8")
    failures = check_required_sections(content)
    failures.extend(check_parser_output(content))
    return failures


def run_validation() -> int:
    """Run validation on all lesson files and print a summary report.

    Returns 0 if all lessons pass, 1 if any fail.
    """
    lesson_files = discover_lesson_files(LESSONS_DIR)

    if not lesson_files:
        print("ERROR: No lesson.md files found under", LESSONS_DIR)
        return 1

    results: dict[Path, list[str]] = {}
    for file_path in lesson_files:
        results[file_path] = validate_lesson(file_path)

    passing = sum(1 for f in results.values() if not f)
    failing = sum(1 for f in results.values() if f)
    total = len(results)

    # Section coverage tracking
    section_names = [
        "Check Your Understanding",
        "Elaborative Interrogation",
        "Misconception Confrontation",
        "Guided Practice",
        "Which Method?",
        "Before You Practice",
        "Connections",
        "Mastery Checklist",
    ]
    section_pass_counts: dict[str, int] = {name: 0 for name in section_names}

    for file_path, failures in results.items():
        failure_text = " ".join(failures)
        for name in section_names:
            if name not in failure_text:
                section_pass_counts[name] += 1

    # Print report
    print("=" * 50)
    print("  Enhanced Lesson Validation Report")
    print("=" * 50)
    print()
    print(f"Total lessons: {total}")
    print(f"Passing: {passing}")
    print(f"Failing: {failing}")
    print()

    if failing > 0:
        print("FAILURES:")
        for file_path, failures in results.items():
            if failures:
                relative_path = file_path.relative_to(PROJECT_ROOT)
                print(f"  {relative_path}")
                for failure in failures:
                    print(f"    âœ— {failure}")
                print()

    print("SECTION COVERAGE:")
    max_name_len = max(len(name) for name in section_names)
    for name in section_names:
        count = section_pass_counts[name]
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {name:<{max_name_len}}  {count}/{total} ({pct:.0f}%)")

    print()
    return 0 if failing == 0 else 1


if __name__ == "__main__":
    sys.exit(run_validation())


