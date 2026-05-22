"""Add missing subtopics (Active/Passive Voice, Direct/Indirect Speech) to existing modules.

NON-DESTRUCTIVE: Only inserts new subtopics, lessons, and questions.
Does NOT touch existing user data, progress, leaderboard, etc.

Usage:
    python scripts/add_missing_subtopics.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

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
from app.infrastructure.database.session import SessionLocal
from scripts.seed_content import parse_lesson_markdown

SEED_BASE = Path(__file__).resolve().parent.parent / "data" / "seed"
GRAMMAR_LESSONS = SEED_BASE / "lessons" / "verbal-ability" / "grammar"
GRAMMAR_QUESTIONS = SEED_BASE / "questions" / "verbal-ability" / "grammar"

DIFFICULTY_MAP = {
    "Easy": Difficulty.EASY.value,
    "Medium": Difficulty.MEDIUM.value,
    "Hard": Difficulty.HARD.value,
}

# Subtopics to add (slug, title, folder, desired_order_index)
NEW_SUBTOPICS = [
    ("active-and-passive-voice", "Active and Passive Voice", "active-and-passive-voice", 9),
    ("direct-and-indirect-speech", "Direct and Indirect Speech", "direct-and-indirect-speech", 10),
]


def add_subtopics_to_topic(session: SASession, topic: Topic, module: Module, category_value: str) -> int:
    """Add missing subtopics to a topic. Returns number of questions added."""
    questions_added = 0

    for slug, title, folder, order_idx in NEW_SUBTOPICS:
        # Check if already exists
        existing = session.query(Subtopic).filter(
            Subtopic.topic_id == topic.id,
            Subtopic.slug == slug,
        ).first()
        if existing:
            print(f"  [SKIP] {title} already exists in topic {topic.id}")
            continue

        # Load lesson content
        lesson_path = GRAMMAR_LESSONS / folder / "lesson.md"
        questions_path = GRAMMAR_QUESTIONS / folder / "questions.json"

        if not lesson_path.exists():
            print(f"  [ERROR] Lesson file not found: {lesson_path}")
            continue
        if not questions_path.exists():
            print(f"  [ERROR] Questions file not found: {questions_path}")
            continue

        lesson_md = lesson_path.read_text(encoding="utf-8")
        lesson_content = parse_lesson_markdown(lesson_md)
        questions_raw = json.loads(questions_path.read_text(encoding="utf-8"))

        # Create subtopic
        subtopic = Subtopic(
            topic_id=topic.id,
            slug=slug,
            title=title,
            order_index=order_idx,
        )
        session.add(subtopic)
        session.flush()

        # Create lesson
        lesson = Lesson(
            subtopic_id=subtopic.id,
            content_json=lesson_content,
            status=LessonStatus.PUBLISHED.value,
        )
        session.add(lesson)

        # Create questions
        for q in questions_raw:
            question = Question(
                subtopic_id=subtopic.id,
                topic_id=topic.id,
                module_id=module.id,
                category=category_value,
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

        questions_added += len(questions_raw)
        print(f"  [ADDED] {title} ({len(questions_raw)} questions)")

    return questions_added


def main():
    session = SessionLocal()
    total_questions = 0

    try:
        # Find both Verbal Ability modules (Professional + Sub-Professional)
        modules = session.query(Module).filter(
            Module.slug.in_(["verbal-ability-professional", "verbal-ability-sub-professional"])
        ).all()

        if not modules:
            print("ERROR: No Verbal Ability modules found. Run seed_content first.")
            return

        for module in modules:
            print(f"\nModule: {module.title} ({module.slug})")

            # Find the Grammar topic
            topic = session.query(Topic).filter(
                Topic.module_id == module.id,
                Topic.slug == "grammar-and-correct-usage",
            ).first()

            if not topic:
                print(f"  ERROR: Grammar topic not found for module {module.slug}")
                continue

            category_value = module.category
            added = add_subtopics_to_topic(session, topic, module, category_value)
            total_questions += added

        session.commit()
        print(f"\nDone! Added {total_questions} questions total.")

    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
