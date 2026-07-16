"""Generate the Verbal Ability / Paragraph Organization / Topic Sentence question bank.

This wrapper reuses the validated main-idea bank generator so the new
topic-sentence bank keeps the same CSE-style mix, structure, and audit checks.
"""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import generate_main_idea_bank as base


OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "paragraph-organization"
    / "topic-sentence"
    / "questions.json"
)


def main() -> None:
    base.SUBTOPIC = "Topic Sentence"
    base.OUTPUT_PATH = OUTPUT_PATH
    items = base._generate_bank()
    base._validate_bank(items)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(base.json.dumps(items, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
