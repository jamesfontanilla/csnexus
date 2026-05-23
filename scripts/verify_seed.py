"""Quick verification of seeded content."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import func
from app.infrastructure.database.session import SessionLocal
from app.features.content.models import Module, Topic, Subtopic, Lesson, Question

session = SessionLocal()

print("=" * 70)
print("DATABASE CONTENT VERIFICATION")
print("=" * 70)

modules = session.query(Module).order_by(Module.category, Module.order_index).all()
total_topics = session.query(func.count(Topic.id)).scalar()
total_subtopics = session.query(func.count(Subtopic.id)).scalar()
total_lessons = session.query(func.count(Lesson.id)).scalar()
total_questions = session.query(func.count(Question.id)).scalar()

print(f"\nTotal: {len(modules)} modules, {total_topics} topics, {total_subtopics} subtopics, {total_lessons} lessons, {total_questions} questions")

for m in modules:
    topics = session.query(Topic).filter(Topic.module_id == m.id).order_by(Topic.order_index).all()
    q_count = session.query(func.count(Question.id)).filter(Question.module_id == m.id).scalar()
    print(f"\n{'─'*70}")
    print(f"Module: {m.title} [{m.category}] (id={m.id}, questions={q_count})")
    for t in topics:
        subtopics = session.query(Subtopic).filter(Subtopic.topic_id == t.id).order_by(Subtopic.order_index).all()
        print(f"  Topic: {t.title} (id={t.id})")
        for s in subtopics:
            has_lesson = session.query(func.count(Lesson.id)).filter(Lesson.subtopic_id == s.id).scalar()
            q_sub = session.query(func.count(Question.id)).filter(Question.subtopic_id == s.id).scalar()
            print(f"    {s.slug}: lesson={'YES' if has_lesson else 'NO'}, questions={q_sub}")

session.close()
