"""Lesson Markdown parser CLI and convenience helpers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.features.content.lesson_engine import parse_lesson_markdown as _parse_lesson_markdown


def parse_lesson_markdown(markdown: str, category: str = "") -> dict[str, Any]:
    """Parse lesson Markdown into the compiled JSON content model."""

    return _parse_lesson_markdown(markdown, category=category)


def parse_lesson_file(path: str | Path, category: str = "") -> dict[str, Any]:
    """Parse a lesson file from disk."""

    lesson_path = Path(path)
    return parse_lesson_markdown(lesson_path.read_text(encoding="utf-8"), category=category)


def infer_category_from_path(path: str | Path) -> str:
    """Infer a category-like segment from a lesson path."""

    lesson_path = Path(path).resolve()
    parts = lesson_path.parts
    if "lessons" in parts:
        index = parts.index("lessons")
        tail = parts[index + 1 : -1]
        if tail:
            return tail[0]
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse lesson Markdown into JSON.")
    parser.add_argument("input", help="Path to a lesson markdown file.")
    parser.add_argument("-o", "--output", help="Write JSON to this path instead of stdout.")
    parser.add_argument("--category", default="", help="Optional category name used by the parser.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    category = args.category or infer_category_from_path(input_path)
    result = parse_lesson_file(input_path, category=category)

    payload = json.dumps(result, ensure_ascii=True, indent=2 if args.pretty else None)
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(payload + "\n", encoding="utf-8")
    else:
        sys.stdout.write(payload)
        if not payload.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
