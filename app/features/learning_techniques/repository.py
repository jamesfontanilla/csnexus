"""Repository for learning technique models.

Provides data access for PersonalNote, LessonReflection, RecallAnswer,
GoodnightReviewSession, SessionReflection, and ChallengeAttempt.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from app.features.learning_techniques.models import (
    ChallengeAttempt,
    GoodnightReviewSession,
    LessonReflection,
    PersonalNote,
    RecallAnswer,
    SessionReflection,
)


class PersonalNoteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, user_id: int, question_id: int, note_text: str) -> PersonalNote:
        note = PersonalNote(user_id=user_id, question_id=question_id, note_text=note_text)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def list_by_user(self, user_id: int) -> list[PersonalNote]:
        return (
            self.db.query(PersonalNote)
            .filter(PersonalNote.user_id == user_id)
            .order_by(PersonalNote.created_at.desc())
            .all()
        )

    def get_by_user_and_question(self, user_id: int, question_id: int) -> PersonalNote | None:
        return (
            self.db.query(PersonalNote)
            .filter(PersonalNote.user_id == user_id, PersonalNote.question_id == question_id)
            .order_by(PersonalNote.created_at.desc())
            .first()
        )


class LessonReflectionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self, *, user_id: int, lesson_id: int, section_index: int, reflection_text: str
    ) -> LessonReflection:
        reflection = LessonReflection(
            user_id=user_id,
            lesson_id=lesson_id,
            section_index=section_index,
            reflection_text=reflection_text,
        )
        self.db.add(reflection)
        self.db.commit()
        self.db.refresh(reflection)
        return reflection

    def list_by_user(self, user_id: int) -> list[LessonReflection]:
        return (
            self.db.query(LessonReflection)
            .filter(LessonReflection.user_id == user_id)
            .order_by(LessonReflection.created_at.desc())
            .all()
        )


class RecallAnswerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        question_id: int,
        user_response: str,
        is_correct: bool | None,
        match_type: str,
    ) -> RecallAnswer:
        answer = RecallAnswer(
            user_id=user_id,
            question_id=question_id,
            user_response=user_response,
            is_correct=is_correct,
            match_type=match_type,
        )
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer


class GoodnightReviewRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_for_today(self, user_id: int, today: date) -> GoodnightReviewSession | None:
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        return (
            self.db.query(GoodnightReviewSession)
            .filter(
                GoodnightReviewSession.user_id == user_id,
                GoodnightReviewSession.session_date >= start,
                GoodnightReviewSession.session_date <= end,
            )
            .first()
        )

    def create(
        self, *, user_id: int, session_date: datetime, items: list, bedtime_preference: str
    ) -> GoodnightReviewSession:
        session = GoodnightReviewSession(
            user_id=user_id,
            session_date=session_date,
            items=items,
            bedtime_preference=bedtime_preference,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def mark_completed(self, session: GoodnightReviewSession) -> GoodnightReviewSession:
        session.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(session)
        return session


class SessionReflectionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        session_date: datetime,
        hardest_item_id: int | None,
        confidence_rating: int,
        review_note: str | None,
    ) -> SessionReflection:
        reflection = SessionReflection(
            user_id=user_id,
            session_date=session_date,
            hardest_item_id=hardest_item_id,
            confidence_rating=confidence_rating,
            review_note=review_note,
        )
        self.db.add(reflection)
        self.db.commit()
        self.db.refresh(reflection)
        return reflection

    def list_by_user(self, user_id: int) -> list[SessionReflection]:
        return (
            self.db.query(SessionReflection)
            .filter(SessionReflection.user_id == user_id)
            .order_by(SessionReflection.created_at.desc())
            .all()
        )


class ChallengeAttemptRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        user_id: int,
        subtopic_id: int,
        question_id: int,
        pre_lesson_answer: str,
        pre_lesson_correct: bool,
    ) -> ChallengeAttempt:
        attempt = ChallengeAttempt(
            user_id=user_id,
            subtopic_id=subtopic_id,
            question_id=question_id,
            pre_lesson_answer=pre_lesson_answer,
            pre_lesson_correct=pre_lesson_correct,
        )
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def get(self, challenge_id: int, user_id: int) -> ChallengeAttempt | None:
        return (
            self.db.query(ChallengeAttempt)
            .filter(
                ChallengeAttempt.id == challenge_id,
                ChallengeAttempt.user_id == user_id,
            )
            .first()
        )

    def update_retest(
        self,
        attempt: ChallengeAttempt,
        post_answer: str,
        post_correct: bool,
    ) -> ChallengeAttempt:
        attempt.post_lesson_answer = post_answer
        attempt.post_lesson_correct = post_correct
        attempt.is_productive_failure_success = not attempt.pre_lesson_correct and post_correct
        self.db.commit()
        self.db.refresh(attempt)
        return attempt
