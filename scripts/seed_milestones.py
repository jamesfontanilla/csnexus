"""Seed competence milestone definitions into the database.

Creates 8 milestone definitions:
- Verbal Mastery, Numerical Mastery, Analytical Mastery (mastery category)
- Full Spectrum (mastery category — all modules)
- Exam Ready: Sub-Professional, Exam Ready: Professional (readiness category)
- Comeback, Resilient Learner (recovery category)

Idempotent: skips existing milestones by slug.

Requirements: 13.1, 13.2, 13.3
"""

from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.features.gamification.models import CompetenceMilestone
from app.infrastructure.database.base import Base
from app.infrastructure.database.session import SessionLocal, engine


MILESTONE_DEFINITIONS = [
    {
        "slug": "verbal-mastery",
        "name": "Verbal Mastery",
        "description": "Achieve mastery (≥0.8) in all Verbal Ability subtopics.",
        "category": "mastery",
        "threshold_config": json.dumps({
            "module_slug": "verbal-ability",
            "threshold": 0.8,
            "required_count": 999,  # All in module — evaluated dynamically
        }),
    },
    {
        "slug": "numerical-mastery",
        "name": "Numerical Mastery",
        "description": "Achieve mastery (≥0.8) in all Numerical Ability subtopics.",
        "category": "mastery",
        "threshold_config": json.dumps({
            "module_slug": "numerical-ability",
            "threshold": 0.8,
            "required_count": 999,
        }),
    },
    {
        "slug": "analytical-mastery",
        "name": "Analytical Mastery",
        "description": "Achieve mastery (≥0.8) in all Analytical Ability subtopics.",
        "category": "mastery",
        "threshold_config": json.dumps({
            "module_slug": "analytical-ability",
            "threshold": 0.8,
            "required_count": 999,
        }),
    },
    {
        "slug": "full-spectrum",
        "name": "Full Spectrum",
        "description": "Achieve mastery (≥0.8) in all subtopics across every module.",
        "category": "mastery",
        "threshold_config": json.dumps({
            "module_slug": None,
            "threshold": 0.8,
            "required_count": 999,
        }),
    },
    {
        "slug": "exam-ready-sub-professional",
        "name": "Exam Ready: Sub-Professional",
        "description": "Maintain a readiness score of ≥70 for 7 consecutive days.",
        "category": "readiness",
        "threshold_config": json.dumps({
            "min_score": 70,
            "consecutive_days": 7,
        }),
    },
    {
        "slug": "exam-ready-professional",
        "name": "Exam Ready: Professional",
        "description": "Maintain a readiness score of ≥80 for 7 consecutive days.",
        "category": "readiness",
        "threshold_config": json.dumps({
            "min_score": 80,
            "consecutive_days": 7,
        }),
    },
    {
        "slug": "comeback",
        "name": "Comeback",
        "description": "Recover a subtopic from <0.5 to ≥0.8 mastery within 14 days.",
        "category": "recovery",
        "threshold_config": json.dumps({
            "low_threshold": 0.5,
            "high_threshold": 0.8,
            "window_days": 14,
        }),
    },
    {
        "slug": "resilient-learner",
        "name": "Resilient Learner",
        "description": "Earn the Comeback milestone 3 times across different subtopics.",
        "category": "recovery",
        "threshold_config": json.dumps({
            "required_comebacks": 3,
        }),
    },
]


def seed_milestones(session: Session) -> int:
    """Seed milestone definitions. Returns count of newly created milestones."""
    created = 0
    for defn in MILESTONE_DEFINITIONS:
        existing = (
            session.query(CompetenceMilestone)
            .filter(CompetenceMilestone.slug == defn["slug"])
            .first()
        )
        if existing is None:
            milestone = CompetenceMilestone(
                slug=defn["slug"],
                name=defn["name"],
                description=defn["description"],
                category=defn["category"],
                threshold_config=defn["threshold_config"],
            )
            session.add(milestone)
            created += 1

    if created > 0:
        session.commit()

    return created


def main() -> None:
    """Run milestone seeding standalone."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        count = seed_milestones(session)
        print(f"Seeded {count} milestone definitions (skipped {len(MILESTONE_DEFINITIONS) - count} existing).")
    finally:
        session.close()


if __name__ == "__main__":
    main()
