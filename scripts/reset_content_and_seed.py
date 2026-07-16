"""Reset content tables and seed lessons plus question banks.

This script is the canonical content reset path for the app:

- it clears the content hierarchy and content-dependent tables
- it leaves users/auth/other app data alone
- it seeds every ``lesson.md`` found under ``data/seed/lessons``
- it seeds every ``questions.json`` found under ``data/seed/questions``

The lesson tree is discovered dynamically, so any new ``lesson.md`` files
added under ``data/seed/lessons`` are picked up automatically.

The question banks are discovered dynamically under the question tree, so any
new ``questions.json`` files added there are picked up automatically.

Usage:
    python scripts/reset_content_and_seed.py
    python scripts/reset_content_and_seed.py --category professional
    python scripts/reset_content_and_seed.py --category sub-professional
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import inspect, select, text
from sqlalchemy.orm import Session

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.features.content.models import (
    Difficulty,
    Lesson,
    LessonStatus,
    LevelScope,
    Module,
    Question,
    QuestionType,
    Subtopic,
    Topic,
)
from app.features.content.schemas import LessonContent
from app.features.users.models import Category
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import SessionLocal, engine
from scripts.parse_lesson import parse_lesson_file


LESSON_ROOT = PROJECT_ROOT / "data" / "seed" / "lessons"
QUESTION_ROOT = PROJECT_ROOT / "data" / "seed" / "questions"
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
    ("verbal-ability", "word-meaning", "antonyms"): (
        "Verbal Ability",
        "Word Meanings",
        "Antonyms",
    ),
    ("verbal-ability", "word-meaning", "context-clues"): (
        "Verbal Ability",
        "Word Meanings",
        "Context Clues",
    ),
    ("verbal-ability", "word-meaning", "connotation"): (
        "Verbal Ability",
        "Word Meanings",
        "Connotation",
    ),
    ("verbal-ability", "word-meaning", "multiple-meaning-words"): (
        "Verbal Ability",
        "Word Meanings",
        "Multiple Meaning Words",
    ),
    ("verbal-ability", "word-meaning", "idioms-and-figurative-phrases"): (
        "Verbal Ability",
        "Word Meanings",
        "Idioms and Figurative Phrases",
    ),
    ("verbal-ability", "word-meaning", "synonyms"): (
        "Verbal Ability",
        "Word Meanings",
        "Synonyms",
    ),
    ("verbal-ability", "word-meaning", "prefixes"): (
        "Verbal Ability",
        "Word Meanings",
        "Prefixes",
    ),
    ("verbal-ability", "word-meaning", "suffixes"): (
        "Verbal Ability",
        "Word Meanings",
        "Suffixes",
    ),
    ("verbal-ability", "word-meaning", "root-words"): (
        "Verbal Ability",
        "Word Meanings",
        "Root Words",
    ),
    ("verbal-ability", "word-meaning", "word-families"): (
        "Verbal Ability",
        "Word Meanings",
        "Word Families",
    ),
    ("verbal-ability", "sentence-completion", "cause-and-effect"): (
        "Verbal Ability",
        "Sentence Completion",
        "Cause and Effect",
    ),
    ("verbal-ability", "error-recognition", "subject-verb-agreement"): (
        "Verbal Ability",
        "Error Recognition",
        "Subject-Verb Agreement",
    ),
    ("verbal-ability", "error-recognition", "pronoun-agreement"): (
        "Verbal Ability",
        "Error Recognition",
        "Pronoun Agreement",
    ),
    ("verbal-ability", "error-recognition", "tense-consistency"): (
        "Verbal Ability",
        "Error Recognition",
        "Tense Consistency",
    ),
    ("verbal-ability", "error-recognition", "articles-and-determiners"): (
        "Verbal Ability",
        "Error Recognition",
        "Articles and Determiners",
    ),
    ("verbal-ability", "error-recognition", "prepositions"): (
        "Verbal Ability",
        "Error Recognition",
        "Prepositions",
    ),
    ("verbal-ability", "error-recognition", "modifier-placement"): (
        "Verbal Ability",
        "Error Recognition",
        "Modifier Placement",
    ),
}

QUESTION_CATEGORY_MAP: dict[str, Category] = {
    "professional": Category.PROFESSIONAL,
    "sub-professional": Category.SUB_PROFESSIONAL,
}


@dataclass(frozen=True)
class LessonSpec:
    path: Path
    subtest_slug: str
    topic_slug: str
    subtopic_slug: str


@dataclass(frozen=True)
class QuestionSpec:
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


def _discover_question_specs(question_root: Path) -> list[QuestionSpec]:
    if not question_root.exists():
        raise FileNotFoundError(f"question root not found: {question_root}")

    specs: list[QuestionSpec] = []
    for path in sorted(question_root.rglob("questions.json")):
        relative = path.relative_to(question_root)
        if len(relative.parts) != 4:
            continue
        subtest_slug, topic_slug, subtopic_slug, filename = relative.parts
        if filename != "questions.json":
            continue
        specs.append(
            QuestionSpec(
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
        session.execute(text(f"TRUNCATE TABLE {quoted} RESTART IDENTITY CASCADE"))
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


def _load_question_bank(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"question bank must be a list: {path}")
    return data


def _normalize_difficulty(raw: str) -> str:
    value = raw.strip().upper()
    try:
        return Difficulty(value).value
    except ValueError as exc:
        raise ValueError(f"invalid difficulty value: {raw!r}") from exc


def _resolve_question_categories(
    raw_categories: list[str] | None, selected: list[Category]
) -> list[Category]:
    if raw_categories:
        resolved: list[Category] = []
        seen: set[Category] = set()
        for raw in raw_categories:
            category = QUESTION_CATEGORY_MAP.get(raw.strip().lower())
            if category is not None and category not in seen:
                resolved.append(category)
                seen.add(category)
    else:
        resolved = list(selected)

    selected_values = {category.value for category in selected}
    return [category for category in resolved if category.value in selected_values]


def _seed_lessons(
    session: Session,
    *,
    categories: list[Category],
    lesson_root: Path,
) -> dict[str, int]:
    specs = _discover_lesson_specs(lesson_root)
    if not specs:
        raise FileNotFoundError(f"no lesson.md files found under {lesson_root}")

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


def _seed_question_banks(
    session: Session,
    *,
    categories: list[Category],
    question_root: Path,
) -> dict[str, Any]:
    specs = _discover_question_specs(question_root)
    if not specs:
        raise FileNotFoundError(f"no question banks found under {question_root}")

    modules = {
        module.slug: module for module in session.execute(select(Module)).scalars().all()
    }
    topics = {
        (topic.module_id, topic.slug): topic
        for topic in session.execute(select(Topic)).scalars().all()
    }
    subtopics = {
        (subtopic.topic_id, subtopic.slug): subtopic
        for subtopic in session.execute(select(Subtopic)).scalars().all()
    }

    seeded_files = 0
    seeded_rows = 0
    seeded_by_category: dict[str, int] = {category.value: 0 for category in categories}

    for spec in specs:
        bank = _load_question_bank(spec.path)
        if not bank:
            raise ValueError(f"question bank is empty: {spec.path}")

        raw_categories: list[str] | None = None
        category_field = bank[0].get("category")
        if isinstance(category_field, list):
            raw_categories = [str(item) for item in category_field]
        elif isinstance(category_field, str):
            raw_categories = [category_field]

        resolved_categories = _resolve_question_categories(raw_categories, categories)
        if not resolved_categories:
            continue

        seeded_files += 1
        for category in resolved_categories:
            module_slug = _module_slug(spec.subtest_slug, category)
            module = modules.get(module_slug)
            if module is None:
                raise RuntimeError(f"missing module for slug {module_slug}")

            topic = topics.get((module.id, spec.topic_slug))
            if topic is None:
                raise RuntimeError(
                    f"missing topic for module {module_slug} and topic {spec.topic_slug}"
                )

            subtopic = subtopics.get((topic.id, spec.subtopic_slug))
            if subtopic is None:
                raise RuntimeError(
                    f"missing subtopic for topic {spec.topic_slug} and subtopic {spec.subtopic_slug}"
                )

            question_rows: list[Question] = []
            for raw in bank:
                stem = str(raw.get("question", "")).strip()
                explanation = str(raw.get("explanation", "")).strip()
                if not stem:
                    raise ValueError(f"blank question text in {spec.path}")
                if not explanation:
                    raise ValueError(f"blank explanation in {spec.path}")

                choices = raw.get("choices") or []
                if not isinstance(choices, list):
                    raise ValueError(f"choices must be a list in {spec.path}")
                if not (2 <= len(choices) <= 6):
                    raise ValueError(
                        f"invalid choice count in {spec.path}: {len(choices)}"
                    )

                options = [str(choice).strip() for choice in choices]
                if any(not option for option in options):
                    raise ValueError(f"blank choice found in {spec.path}")

                answer = str(raw.get("answer", "")).strip()
                if answer not in options:
                    raise ValueError(
                        f"correct answer {answer!r} is not one of the choices in {spec.path}"
                    )

                question_rows.append(
                    Question(
                        subtopic_id=subtopic.id,
                        topic_id=topic.id,
                        module_id=module.id,
                        category=category.value,
                        level_scope=LevelScope.SUBTOPIC.value,
                        stem=stem,
                        options=options,
                        correct_answer=answer,
                        explanation=explanation,
                        difficulty=_normalize_difficulty(str(raw.get("difficulty", ""))),
                        qtype=QuestionType.MULTIPLE_CHOICE.value,
                        is_active=True,
                    )
                )

            session.add_all(question_rows)
            session.flush()
            seeded_rows += len(question_rows)
            seeded_by_category[category.value] += len(question_rows)

    return {
        "files": seeded_files,
        "rows": seeded_rows,
        "by_category": seeded_by_category,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reset content tables and seed lessons plus question banks."
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
    parser.add_argument(
        "--question-root",
        type=Path,
        default=QUESTION_ROOT,
        help="Root folder that contains question bank folders.",
    )
    args = parser.parse_args(argv)

    categories = _parse_categories(args.category)
    lesson_root = args.lesson_root.resolve()
    question_root = args.question_root.resolve()

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        with session.begin():
            _reset_content_tables(session)
            lesson_summary = _seed_lessons(
                session,
                categories=categories,
                lesson_root=lesson_root,
            )
            question_summary = _seed_question_banks(
                session,
                categories=categories,
                question_root=question_root,
            )

    category_list = ", ".join(category.value for category in categories)
    print(f"Reset complete for categories: {category_list}")
    print(f"Seeded modules: {lesson_summary['modules']}")
    print(f"Seeded topics: {lesson_summary['topics']}")
    print(f"Seeded subtopics: {lesson_summary['subtopics']}")
    print(f"Seeded lessons: {lesson_summary['lessons']}")
    print(f"Seeded question files: {question_summary['files']}")
    print(f"Seeded questions: {question_summary['rows']}")
    for category_name, count in question_summary["by_category"].items():
        print(f"Seeded questions for {category_name}: {count}")
    print(f"Lesson root: {lesson_root}")
    print(f"Question root: {question_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
