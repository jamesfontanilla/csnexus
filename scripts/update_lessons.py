"""Update lesson content in-place without wiping user data.

Re-parses all lesson.md files and updates the content_json for existing
lessons. Does NOT touch users, progress, scores, or any other tables.

Scans the entire data/seed/lessons/ directory tree for lesson.md files,
matches them to existing subtopics by slug, and updates the content_json
using the enhanced parser.

Usage:
    python scripts/update_lessons.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.infrastructure.database.session import SessionLocal, engine
from app.infrastructure.database.base import Base
from app.features.content.models import Lesson, LessonStatus, Subtopic
from scripts.parse_lesson import parse_lesson_markdown


SEED_BASE = Path(__file__).resolve().parent.parent / "data" / "seed"
LESSONS_ROOT = SEED_BASE / "lessons"


def discover_lesson_files() -> list[tuple[str, Path]]:
    """Walk the lessons directory and return (slug, path) pairs.

    The slug is derived from the parent folder name of each lesson.md file.
    E.g., data/seed/lessons/verbal-ability/grammar/subject-verb-agreement/lesson.md
    yields slug "subject-verb-agreement".
    """
    results: list[tuple[str, Path]] = []
    if not LESSONS_ROOT.exists():
        return results

    for lesson_path in LESSONS_ROOT.rglob("lesson.md"):
        slug = lesson_path.parent.name
        results.append((slug, lesson_path))

    return results


def main() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        updated = 0
        skipped = 0
        errors = 0

        lesson_files = discover_lesson_files()
        print(f"Found {len(lesson_files)} lesson.md files to process.\n")

        for slug, lesson_path in lesson_files:
            try:
                md_text = lesson_path.read_text(encoding="utf-8")
                new_content = parse_lesson_markdown(md_text)

                # Find all subtopics with this slug (both categories)
                subtopics = session.query(Subtopic).filter(
                    Subtopic.slug == slug
                ).all()

                if not subtopics:
                    skipped += 1
                    continue

                for st in subtopics:
                    lesson = session.query(Lesson).filter(
                        Lesson.subtopic_id == st.id
                    ).first()
                    if lesson:
                        lesson.content_json = new_content
                        lesson.status = LessonStatus.PUBLISHED.value
                        updated += 1
                        print(f"  Updated: {slug} (subtopic_id={st.id})")
                    else:
                        # Create lesson if subtopic exists but lesson doesn't
                        lesson = Lesson(
                            subtopic_id=st.id,
                            content_json=new_content,
                            status=LessonStatus.PUBLISHED.value,
                        )
                        session.add(lesson)
                        updated += 1
                        print(f"  Created: {slug} (subtopic_id={st.id})")

            except Exception as e:
                errors += 1
                print(f"  ERROR {slug}: {e}")

        session.commit()
        print(f"\nDone. Updated {updated} lesson(s), skipped {skipped}, errors {errors}.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
