"""Repository tests for the explanations feature — real DB, no mocks."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.features.explanations.models import QuestionExplanation
from app.features.explanations.repository import ExplanationRepository
from app.features.users.models import User
from app.features.content.models import Module, Topic, Subtopic, Question


def _seed_user(db: Session) -> User:
    user = User(
        email="explain@test.com",
        display_name="Explain Tester",
        age=25,
        category="PROFESSIONAL",
        role="LEARNER",
        account_state="VERIFIED",
        password_hash="$2b$10$fakehash",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _seed_question(db: Session, stem: str = "What is 2+2?") -> Question:
    mod = Module(category="PROFESSIONAL", slug="mod-exp", title="Mod", order_index=0)
    db.add(mod)
    db.commit()
    db.refresh(mod)

    topic = Topic(module_id=mod.id, slug="top-exp", title="Top", order_index=0)
    db.add(topic)
    db.commit()
    db.refresh(topic)

    sub = Subtopic(topic_id=topic.id, slug="sub-exp", title="Sub", order_index=0)
    db.add(sub)
    db.commit()
    db.refresh(sub)

    q = Question(
        subtopic_id=sub.id,
        topic_id=topic.id,
        module_id=mod.id,
        category="PROFESSIONAL",
        level_scope="SUBTOPIC",
        stem=stem,
        options=["3", "4", "5", "6"],
        correct_answer="4",
        explanation="Basic arithmetic.",
        difficulty="EASY",
        qtype="MULTIPLE_CHOICE",
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def _seed_questions(db: Session, count: int) -> list[Question]:
    """Seed multiple questions sharing the same module/topic/subtopic."""
    mod = Module(category="PROFESSIONAL", slug="mod-bulk", title="Mod Bulk", order_index=1)
    db.add(mod)
    db.commit()
    db.refresh(mod)

    topic = Topic(module_id=mod.id, slug="top-bulk", title="Top Bulk", order_index=0)
    db.add(topic)
    db.commit()
    db.refresh(topic)

    sub = Subtopic(topic_id=topic.id, slug="sub-bulk", title="Sub Bulk", order_index=0)
    db.add(sub)
    db.commit()
    db.refresh(sub)

    questions: list[Question] = []
    for i in range(count):
        q = Question(
            subtopic_id=sub.id,
            topic_id=topic.id,
            module_id=mod.id,
            category="PROFESSIONAL",
            level_scope="SUBTOPIC",
            stem=f"Question {i}?",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation=f"Explanation {i}.",
            difficulty="EASY",
            qtype="MULTIPLE_CHOICE",
        )
        db.add(q)
    db.commit()
    for q in questions:
        db.refresh(q)
    # Re-query to get all with IDs
    questions = []
    from sqlalchemy import select
    stmt = select(Question).where(Question.subtopic_id == sub.id)
    questions = list(db.execute(stmt).scalars().all())
    return questions


def _seed_explanation(db: Session, question_id: int) -> QuestionExplanation:
    explanation = QuestionExplanation(
        question_id=question_id,
        explanation_text="This is a detailed explanation that meets the minimum length requirement for the field.",
        key_concept="Basic Arithmetic",
        related_subtopics="[1, 2, 3]",
        cache_version=1,
    )
    db.add(explanation)
    db.commit()
    db.refresh(explanation)
    return explanation


def test_get_by_question_id_returns_explanation(db_session: Session) -> None:
    q = _seed_question(db_session)
    _seed_explanation(db_session, q.id)
    repo = ExplanationRepository(db=db_session)

    result = repo.get_by_question_id(q.id)

    assert result is not None
    assert result.question_id == q.id
    assert result.key_concept == "Basic Arithmetic"
    assert result.cache_version == 1


def test_get_by_question_id_returns_none_when_missing(db_session: Session) -> None:
    repo = ExplanationRepository(db=db_session)

    result = repo.get_by_question_id(9999)

    assert result is None


def test_get_bulk_returns_all_explanations(db_session: Session) -> None:
    questions = _seed_questions(db_session, 3)
    for q in questions:
        _seed_explanation(db_session, q.id)
    repo = ExplanationRepository(db=db_session)

    question_ids = [q.id for q in questions]
    result = repo.get_bulk(question_ids)

    assert len(result) == 3
    for qid in question_ids:
        assert qid in result
        assert result[qid] is not None
        assert result[qid].question_id == qid


def test_get_bulk_returns_none_for_missing(db_session: Session) -> None:
    questions = _seed_questions(db_session, 2)
    # Only seed an explanation for the first question
    _seed_explanation(db_session, questions[0].id)
    repo = ExplanationRepository(db=db_session)

    question_ids = [q.id for q in questions]
    result = repo.get_bulk(question_ids)

    assert len(result) == 2
    assert result[questions[0].id] is not None
    assert result[questions[1].id] is None


def test_get_bulk_with_nonexistent_ids(db_session: Session) -> None:
    repo = ExplanationRepository(db=db_session)

    result = repo.get_bulk([9990, 9991, 9992])

    assert len(result) == 3
    assert all(v is None for v in result.values())


def test_get_bulk_empty_list(db_session: Session) -> None:
    repo = ExplanationRepository(db=db_session)

    result = repo.get_bulk([])

    assert result == {}
