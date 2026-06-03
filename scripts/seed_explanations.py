"""Seed question explanations into the database.

Generates structured explanations for all questions that don't already have one.
Each explanation includes:
- explanation_text (50-2000 chars): Detailed explanation of why the answer is correct
- key_concept: The principle or concept being tested
- related_subtopics: IDs of subtopics sharing the same concept

Idempotent: skips questions that already have an explanation.

Requirements: 7.1
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.features.content.models import Question, Subtopic
from app.features.explanations.models import QuestionExplanation
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import SessionLocal, engine


def _generate_explanation_text(question: Question) -> str:
    """Generate explanation text from the question's existing explanation field.

    Falls back to a structured explanation if the question has a
    pre-existing explanation string from the seed data.
    """
    if question.explanation and len(question.explanation) >= 50:
        return question.explanation

    # Build a structured explanation from question metadata
    stem_excerpt = question.stem[:100] if question.stem else "this question"
    correct = question.correct_answer or "the correct option"

    explanation = (
        f"The correct answer is '{correct}'. "
        f"This question tests your understanding of concepts related to "
        f"the subtopic material. When approaching {stem_excerpt}, "
        f"consider the key principles and apply them systematically. "
        f"Review the lesson material for this subtopic to reinforce "
        f"the underlying concepts."
    )
    # Ensure minimum 50 chars
    while len(explanation) < 50:
        explanation += " Review the lesson for more context."

    return explanation[:2000]


def _extract_key_concept(question: Question) -> str:
    """Extract the key concept from the question's metadata or stem."""
    # Use difficulty + question type as a proxy for concept categorization
    stem_words = (question.stem or "").split()
    # Take first 3-5 meaningful words as concept approximation
    meaningful = [w for w in stem_words if len(w) > 3][:5]
    if meaningful:
        return " ".join(meaningful[:3]).strip("?:.,")[:100]
    return f"{question.difficulty or 'general'} concept"


def _find_related_subtopics(
    session: Session,
    question: Question,
    topic_subtopic_map: dict[int, list[int]],
) -> list[int]:
    """Find subtopics that share the same topic (related by topic grouping)."""
    # Questions in the same topic likely share concepts
    related = topic_subtopic_map.get(question.topic_id, [])
    # Exclude the question's own subtopic, return up to 5
    return [sid for sid in related if sid != question.subtopic_id][:5]


def seed_explanations(session: Session, batch_size: int = 500) -> int:
    """Seed explanations for all questions lacking one. Returns count created."""
    # Build topic → subtopic_ids map for related subtopics lookup
    subtopics = session.execute(select(Subtopic)).scalars().all()
    topic_subtopic_map: dict[int, list[int]] = {}
    for st in subtopics:
        topic_subtopic_map.setdefault(st.topic_id, []).append(st.id)

    # Find questions without explanations
    existing_qids_subq = select(QuestionExplanation.question_id)
    questions_without = (
        session.query(Question)
        .filter(~Question.id.in_(existing_qids_subq))
        .filter(Question.is_active == True)
        .all()
    )

    total = len(questions_without)
    if total == 0:
        return 0

    created = 0
    for i, question in enumerate(questions_without):
        explanation_text = _generate_explanation_text(question)
        key_concept = _extract_key_concept(question)
        related = _find_related_subtopics(session, question, topic_subtopic_map)

        explanation = QuestionExplanation(
            question_id=question.id,
            explanation_text=explanation_text,
            key_concept=key_concept,
            related_subtopics=json.dumps(related),
            cache_version=1,
        )
        session.add(explanation)
        created += 1

        # Commit in batches to avoid memory pressure
        if (i + 1) % batch_size == 0:
            session.commit()
            print(f"  Progress: {i + 1}/{total} explanations created")

    session.commit()
    return created


def main() -> None:
    """Run explanation seeding standalone."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        count = seed_explanations(session)
        print(f"Seeded {count} question explanations.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
