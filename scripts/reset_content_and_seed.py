"""Reset content tables and seed lessons from ``data/seed/lessons``.

This script is the lightweight "content reset" path for the app:

- it clears the content hierarchy and content-dependent tables
- it leaves users/auth/other app data alone
- it seeds every ``lesson.md`` found under ``data/seed/lessons``

The current repository only has one lesson file, so this will seed just
``Verbal Ability / Word Meanings / Synonyms`` for now.

Usage:
    python scripts/reset_content_and_seed.py
    python scripts/reset_content_and_seed.py --category professional
    python scripts/reset_content_and_seed.py --category sub-professional
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import inspect, select, text
from sqlalchemy.orm import Session

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.features.content.models import Lesson, LessonStatus, Module, Subtopic, Topic
from app.features.content.schemas import LessonContent
from app.features.users.models import Category
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import SessionLocal, engine
from scripts.parse_lesson import parse_lesson_file


LESSON_ROOT = PROJECT_ROOT / "data" / "seed" / "lessons"
ROOT_TABLES = {
    "modules",
    "topics",
    "subtopics",
    "lessons",
    "questions",
    "mock_exam_configs",
}

# The current lesson tree is named a little more naturally in the UI than
# the raw slug path. Keep the override small and local so future lesson trees
# can still fall back to slug-to-title conversion.
TITLE_OVERRIDES: dict[tuple[str, str, str], tuple[str, str, str]] = {
    ("verbal-ability", "word-meaning", "synonyms"): (
        "Verbal Ability",
        "Word Meanings",
        "Synonyms",
    ),
}


@dataclass(frozen=True)
class LessonSpec:
    path: Path
    subtest_slug: str
    topic_slug: str
    subtopic_slug: str


def _slug_to_title(slug: str) -> str:
    parts = [part for part in re.split(r"[-_]+", slug) if part]
    return " ".join(part.capitalize() for part in parts)


def _resolve_titles(spec: LessonSpec) -> tuple[str, str, str]:
    override = TITLE_OVERRIDES.get(
        (spec.subtest_slug, spec.topic_slug, spec.subtopic_slug)
    )
    if override is not None:
        return override
    return (
        _slug_to_title(spec.subtest_slug),
        _slug_to_title(spec.topic_slug),
        _slug_to_title(spec.subtopic_slug),
    )


def _module_slug(subtest_slug: str, category: Category) -> str:
    if category == Category.PROFESSIONAL:
        return subtest_slug
    suffix = category.value.lower().replace("_", "-")
    return f"{subtest_slug}-{suffix}"


def _discover_lesson_specs(lesson_root: Path) -> list[LessonSpec]:
    if not lesson_root.exists():
        raise FileNotFoundError(f"lesson root not found: {lesson_root}")

    specs: list[LessonSpec] = []
    for path in sorted(lesson_root.rglob("lesson.md")):
        relative = path.relative_to(lesson_root)
        if len(relative.parts) != 4:
            continue
        subtest_slug, topic_slug, subtopic_slug, filename = relative.parts
        if filename != "lesson.md":
            continue
        specs.append(
            LessonSpec(
                path=path,
                subtest_slug=subtest_slug,
                topic_slug=topic_slug,
                subtopic_slug=subtopic_slug,
            )
        )
    return specs


def _parse_categories(value: str) -> list[Category]:
    if value == "both":
        return [Category.PROFESSIONAL, Category.SUB_PROFESSIONAL]
    if value == "professional":
        return [Category.PROFESSIONAL]
    if value == "sub-professional":
        return [Category.SUB_PROFESSIONAL]
    raise ValueError(f"unsupported category selection: {value}")


def _collect_dependent_tables(inspector, root_tables: set[str]) -> set[str]:
    tables = set(inspector.get_table_names())
    foreign_keys: dict[str, set[str]] = {}
    for table in tables:
        refs: set[str] = set()
        for fk in inspector.get_foreign_keys(table):
            referred = fk.get("referred_table")
            if referred:
                refs.add(referred)
        foreign_keys[table] = refs

    closure = {table for table in root_tables if table in tables}
    changed = True
    while changed:
        changed = False
        for table, refs in foreign_keys.items():
            if table in closure:
                continue
            if refs & closure:
                closure.add(table)
                changed = True
    return closure


def _reset_content_tables(session: Session) -> None:
    bind = session.get_bind()
    if bind is None:
        raise RuntimeError("database bind is not available")

    inspector = inspect(bind)
    table_names = set(inspector.get_table_names())
    root_tables = {table for table in ROOT_TABLES if table in table_names}

    if bind.dialect.name == "postgresql":
        if not root_tables:
            return
        quoted = ", ".join(
            bind.dialect.identifier_preparer.quote(table) for table in sorted(root_tables)
        )
        session.execute(
            text(f"TRUNCATE TABLE {quoted} RESTART IDENTITY CASCADE")
        )
        return

    # SQLite path: disable FK enforcement for the wipe, delete the full
    # dependent closure, then re-enable enforcement before seeding.
    conn = session.connection()
    closure = _collect_dependent_tables(inspector, root_tables)
    # ``mock_exam_configs`` is content-related but not FK-linked, so add it
    # explicitly when present.
    if "mock_exam_configs" in table_names:
        closure.add("mock_exam_configs")

    conn.exec_driver_sql("PRAGMA foreign_keys = OFF")
    try:
        for table in sorted(closure):
            quoted = conn.dialect.identifier_preparer.quote(table)
            conn.exec_driver_sql(f"DELETE FROM {quoted}")
    finally:
        conn.exec_driver_sql("PRAGMA foreign_keys = ON")


def _seed_lessons(session: Session, *, categories: list[Category], lesson_root: Path) -> dict[str, int]:
    specs = _discover_lesson_specs(lesson_root)
    if not specs:
        raise FileNotFoundError(
            f"no lesson.md files found under {lesson_root}"
        )

    module_cache: dict[tuple[str, str], Module] = {}
    topic_cache: dict[tuple[str, str, str], Topic] = {}
    subtopic_cache: dict[tuple[str, str, str, str], Subtopic] = {}
    module_order: dict[str, int] = {category.value: 0 for category in categories}
    topic_order: dict[tuple[str, str], int] = {}
    subtopic_order: dict[tuple[str, str, str], int] = {}

    seeded_modules = 0
    seeded_topics = 0
    seeded_subtopics = 0
    seeded_lessons = 0

    for category in categories:
        for spec in specs:
            module_key = (category.value, spec.subtest_slug)
            topic_key = (category.value, spec.subtest_slug, spec.topic_slug)
            subtopic_key = (
                category.value,
                spec.subtest_slug,
                spec.topic_slug,
                spec.subtopic_slug,
            )

            module = module_cache.get(module_key)
            if module is None:
                module_title, _, _ = _resolve_titles(spec)
                module_order[category.value] += 1
                module = Module(
                    category=category.value,
                    slug=_module_slug(spec.subtest_slug, category),
                    title=module_title,
                    order_index=module_order[category.value],
                    is_published=True,
                )
                session.add(module)
                session.flush()
                module_cache[module_key] = module
                seeded_modules += 1

            topic = topic_cache.get(topic_key)
            if topic is None:
                _, topic_title, _ = _resolve_titles(spec)
                topic_counter_key = (category.value, spec.subtest_slug)
                topic_order[topic_counter_key] = topic_order.get(topic_counter_key, 0) + 1
                topic = Topic(
                    module_id=module.id,
                    slug=spec.topic_slug,
                    title=topic_title,
                    order_index=topic_order[topic_counter_key],
                )
                session.add(topic)
                session.flush()
                topic_cache[topic_key] = topic
                seeded_topics += 1

            subtopic = subtopic_cache.get(subtopic_key)
            if subtopic is None:
                _, _, subtopic_title = _resolve_titles(spec)
                subtopic_counter_key = (category.value, spec.subtest_slug, spec.topic_slug)
                subtopic_order[subtopic_counter_key] = (
                    subtopic_order.get(subtopic_counter_key, 0) + 1
                )
                subtopic = Subtopic(
                    topic_id=topic.id,
                    slug=spec.subtopic_slug,
                    title=subtopic_title,
                    order_index=subtopic_order[subtopic_counter_key],
                )
                session.add(subtopic)
                session.flush()
                subtopic_cache[subtopic_key] = subtopic
                seeded_subtopics += 1

            parsed = parse_lesson_file(spec.path, category=category.value)
            validated = LessonContent.model_validate(parsed).model_dump(mode="json")

            lesson = session.execute(
                select(Lesson).where(Lesson.subtopic_id == subtopic.id)
            ).scalar_one_or_none()
            if lesson is None:
                lesson = Lesson(
                    subtopic_id=subtopic.id,
                    content_json=validated,
                    status=LessonStatus.PUBLISHED.value,
                )
                session.add(lesson)
            else:
                lesson.content_json = validated
                lesson.status = LessonStatus.PUBLISHED.value
            seeded_lessons += 1

    return {
        "modules": seeded_modules,
        "topics": seeded_topics,
        "subtopics": seeded_subtopics,
        "lessons": seeded_lessons,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reset content tables and seed lessons from data/seed/lessons."
    )
    parser.add_argument(
        "--category",
        choices=["both", "professional", "sub-professional"],
        default="both",
        help="Which category tracks to seed. Default: both.",
    )
    parser.add_argument(
        "--lesson-root",
        type=Path,
        default=LESSON_ROOT,
        help="Root folder that contains lesson.md files.",
    )
    args = parser.parse_args(argv)

    categories = _parse_categories(args.category)
    lesson_root = args.lesson_root.resolve()

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        with session.begin():
            _reset_content_tables(session)
            summary = _seed_lessons(
                session,
                categories=categories,
                lesson_root=lesson_root,
            )

    category_list = ", ".join(category.value for category in categories)
    print(f"Reset complete for categories: {category_list}")
    print(f"Seeded modules: {summary['modules']}")
    print(f"Seeded topics: {summary['topics']}")
    print(f"Seeded subtopics: {summary['subtopics']}")
    print(f"Seeded lessons: {summary['lessons']}")
    print(f"Lesson root: {lesson_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
