"""Seed ALL content (vocabulary, reading comprehension, numerical ability) into the database.

NON-DESTRUCTIVE: Only inserts new modules/topics/subtopics/lessons/questions.
Skips anything that already exists (matched by slug).

Creates the full hierarchy:
  Module: "Verbal Ability" (per category)
    Topic: "Vocabulary Development"
      Subtopics: synonyms, antonyms, analogies, context-clues, word-formation,
                 idioms-and-expressions, denotation-and-connotation, formal-and-informal-language
    Topic: "Reading Comprehension"
      Subtopics: fundamentals-of-reading-comprehension, vocabulary-in-context,
                 analytical-comprehension, authors-purpose-and-tone, organization-of-ideas
  Module: "Numerical Ability" (per category)
    Topic: "Basic Operations"
      Subtopics: fundamental-number-concepts, addition, subtraction, multiplication

Usage:
    DATABASE_URL=postgresql://... python scripts/seed_all_content.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session as SASession

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
from app.features.users.models import Category
from app.infrastructure.database.session import SessionLocal, engine
from app.infrastructure.database.base import Base
from scripts.parse_lesson import parse_lesson_markdown


SEED_BASE = Path(__file__).resolve().parent.parent / "data" / "seed"

DIFFICULTY_MAP = {
    "Easy": Difficulty.EASY.value,
    "Medium": Difficulty.MEDIUM.value,
    "Hard": Difficulty.HARD.value,
}

# ---------------------------------------------------------------------------
# Content hierarchy configuration
# ---------------------------------------------------------------------------

# Each entry: (topic_slug, topic_title, subtopics_list)
# Each subtopic: (slug, title, order_index)

VERBAL_ABILITY_TOPICS: list[tuple[str, str, list[tuple[str, str, int]]]] = [
    ("grammar-and-correct-usage", "Grammar and Correct Usage", [
        ("subject-verb-agreement", "Subject-Verb Agreement", 1),
        ("verb-tenses", "Verb Tenses", 2),
        ("pronouns", "Pronouns", 3),
        ("prepositions", "Prepositions", 4),
        ("conjunctions", "Conjunctions", 5),
        ("modifiers", "Modifiers", 6),
        ("parallelism", "Parallelism", 7),
        ("articles", "Articles", 8),
        ("active-and-passive-voice", "Active and Passive Voice", 9),
        ("direct-and-indirect-speech", "Direct and Indirect Speech", 10),
    ]),
    ("vocabulary-development", "Vocabulary Development", [
        ("synonyms", "Synonyms", 1),
        ("antonyms", "Antonyms", 2),
        ("analogies", "Analogies", 3),
        ("context-clues", "Context Clues", 4),
        ("word-formation", "Word Formation", 5),
        ("idioms-and-expressions", "Idioms and Expressions", 6),
        ("denotation-and-connotation", "Denotation and Connotation", 7),
        ("formal-and-informal-language", "Formal and Informal Language", 8),
    ]),
    ("reading-comprehension", "Reading Comprehension", [
        ("fundamentals-of-reading-comprehension", "Fundamentals of Reading Comprehension", 1),
        ("vocabulary-in-context", "Vocabulary in Context", 2),
        ("analytical-comprehension", "Analytical Comprehension", 3),
        ("authors-purpose-and-tone", "Author's Purpose and Tone", 4),
        ("organization-of-ideas", "Organization of Ideas", 5),
    ]),
]

NUMERICAL_ABILITY_TOPICS: list[tuple[str, str, list[tuple[str, str, int]]]] = [
    ("basic-operations", "Basic Operations", [
        ("fundamental-number-concepts", "Fundamental Number Concepts", 1),
        ("addition", "Addition", 2),
        ("subtraction", "Subtraction", 3),
        ("multiplication", "Multiplication", 4),
    ]),
]

# Map topic slugs to their lesson/question directories
LESSON_DIRS = {
    "grammar-and-correct-usage": SEED_BASE / "lessons" / "verbal-ability" / "grammar",
    "vocabulary-development": SEED_BASE / "lessons" / "verbal-ability" / "vocabulary-development",
    "reading-comprehension": SEED_BASE / "lessons" / "verbal-ability" / "reading-comprehension",
    "basic-operations": SEED_BASE / "lessons" / "numerical-ability" / "basic-operations",
}

QUESTION_DIRS = {
    "grammar-and-correct-usage": SEED_BASE / "questions" / "verbal-ability" / "grammar",
    "vocabulary-development": SEED_BASE / "questions" / "verbal-ability" / "vocabulary-development",
    "reading-comprehension": SEED_BASE / "questions" / "verbal-ability" / "reading-comprehension",
    "basic-operations": SEED_BASE / "questions" / "numerical-ability" / "basic-operations",
}


def get_or_create_module(
    session: SASession, slug: str, title: str, category: str, order_index: int
) -> Module:
    """Get existing module or create new one."""
    module = session.query(Module).filter(Module.slug == slug).first()
    if module:
        print(f"  [EXISTS] Module: {slug}")
        return module

    module = Module(
        category=category,
        slug=slug,
        title=title,
        order_index=order_index,
        is_published=True,
    )
    session.add(module)
    session.flush()
    print(f"  [CREATED] Module: {slug} (id={module.id})")
    return module


def get_or_create_topic(
    session: SASession, module_id: int, slug: str, title: str, order_index: int
) -> Topic:
    """Get existing topic or create new one."""
    topic = session.query(Topic).filter(
        Topic.module_id == module_id, Topic.slug == slug
    ).first()
    if topic:
        print(f"    [EXISTS] Topic: {slug}")
        return topic

    topic = Topic(
        module_id=module_id,
        slug=slug,
        title=title,
        order_index=order_index,
    )
    session.add(topic)
    session.flush()
    print(f"    [CREATED] Topic: {slug} (id={topic.id})")
    return topic


def seed_subtopic(
    session: SASession,
    topic: Topic,
    module: Module,
    slug: str,
    title: str,
    order_index: int,
    lesson_dir: Path,
    question_dir: Path,
) -> int:
    """Seed a single subtopic with its lesson and questions. Returns questions added."""
    # Check if subtopic already exists
    existing = session.query(Subtopic).filter(
        Subtopic.topic_id == topic.id, Subtopic.slug == slug
    ).first()
    if existing:
        # Check if lesson needs updating
        lesson = session.query(Lesson).filter(
            Lesson.subtopic_id == existing.id
        ).first()
        lesson_path = lesson_dir / slug / "lesson.md"
        if lesson and lesson_path.exists():
            md_text = lesson_path.read_text(encoding="utf-8")
            new_content = parse_lesson_markdown(md_text)
            lesson.content_json = new_content
            print(f"      [UPDATED] {slug} lesson content")
        else:
            print(f"      [EXISTS] {slug}")
        return 0

    # Create subtopic
    subtopic = Subtopic(
        topic_id=topic.id,
        slug=slug,
        title=title,
        order_index=order_index,
    )
    session.add(subtopic)
    session.flush()

    # Load and create lesson
    lesson_path = lesson_dir / slug / "lesson.md"
    if lesson_path.exists():
        md_text = lesson_path.read_text(encoding="utf-8")
        lesson_content = parse_lesson_markdown(md_text)
        lesson = Lesson(
            subtopic_id=subtopic.id,
            content_json=lesson_content,
            status=LessonStatus.PUBLISHED.value,
        )
        session.add(lesson)
    else:
        print(f"      [WARN] No lesson.md for {slug}")

    # Load and create questions
    questions_path = question_dir / slug / "questions.json"
    questions_added = 0
    if questions_path.exists():
        questions_raw = json.loads(questions_path.read_text(encoding="utf-8"))
        for q in questions_raw:
            question = Question(
                subtopic_id=subtopic.id,
                topic_id=topic.id,
                module_id=module.id,
                category=module.category,
                level_scope=LevelScope.SUBTOPIC.value,
                stem=q["question"],
                options=q["choices"],
                correct_answer=q["answer"],
                explanation=q["explanation"],
                difficulty=DIFFICULTY_MAP.get(q["difficulty"], Difficulty.EASY.value),
                qtype=QuestionType.MULTIPLE_CHOICE.value,
                is_active=True,
            )
            session.add(question)
        questions_added = len(questions_raw)
    else:
        print(f"      [WARN] No questions.json for {slug}")

    print(f"      [CREATED] {slug} ({questions_added} questions)")
    return questions_added


def main() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    total_questions = 0

    try:
        for cat_key, cat_value in [
            ("professional", Category.PROFESSIONAL.value),
            ("sub-professional", Category.SUB_PROFESSIONAL.value),
        ]:
            print(f"\n{'='*60}")
            print(f"Category: {cat_key}")
            print(f"{'='*60}")

            # --- Verbal Ability module ---
            va_module = get_or_create_module(
                session,
                slug=f"verbal-ability-{cat_key}",
                title="Verbal Ability",
                category=cat_value,
                order_index=10,
            )

            for topic_idx, (topic_slug, topic_title, subtopics) in enumerate(VERBAL_ABILITY_TOPICS, start=1):
                topic = get_or_create_topic(
                    session, va_module.id, topic_slug, topic_title,
                    order_index=topic_idx,
                )

                lesson_dir = LESSON_DIRS[topic_slug]
                question_dir = QUESTION_DIRS[topic_slug]

                for slug, title, order_idx in subtopics:
                    added = seed_subtopic(
                        session, topic, va_module,
                        slug, title, order_idx,
                        lesson_dir, question_dir,
                    )
                    total_questions += added

            # --- Numerical Ability module ---
            na_module = get_or_create_module(
                session,
                slug=f"numerical-ability-{cat_key}",
                title="Numerical Ability",
                category=cat_value,
                order_index=20,
            )

            for topic_slug, topic_title, subtopics in NUMERICAL_ABILITY_TOPICS:
                topic = get_or_create_topic(
                    session, na_module.id, topic_slug, topic_title,
                    order_index=1,
                )

                lesson_dir = LESSON_DIRS[topic_slug]
                question_dir = QUESTION_DIRS[topic_slug]

                for slug, title, order_idx in subtopics:
                    added = seed_subtopic(
                        session, topic, na_module,
                        slug, title, order_idx,
                        lesson_dir, question_dir,
                    )
                    total_questions += added

        session.commit()
        print(f"\n{'='*60}")
        print(f"DONE. Total new questions added: {total_questions}")
        print(f"{'='*60}")

    except Exception as e:
        session.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
