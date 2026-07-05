"""milestone_enrichment

Revision ID: b3e1d5f9a2c8
Revises: a4f9c7d2b1e1
Create Date: 2026-07-05 00:00:00.000000

Enriches the milestones feature with:

1. competence_milestones.xp_reward (INTEGER NOT NULL DEFAULT 0)
   — XP bonus granted when a milestone is first awarded.

2. competence_milestone_awards.seen_at (DATETIME nullable)
   — NULL until the user retrieves their unseen awards; enables
     frontend toast notifications for newly earned milestones.

3. mastery_score_history table (append-only change log)
   — Replaces the updated_at-based recovery detection approximation.
     Written by MasteryService on every mastery_score change so
     MilestoneService can find genuine low→high recovery pairs.

4. xp_events source CHECK constraint extended with 'MILESTONE_AWARD'
   — Required for XPService.award(source=XPSource.MILESTONE_AWARD).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = "b3e1d5f9a2c8"
down_revision = "a4f9c7d2b1e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add xp_reward to competence_milestones
    op.add_column(
        "competence_milestones",
        sa.Column(
            "xp_reward",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # 2. Add seen_at to competence_milestone_awards
    op.add_column(
        "competence_milestone_awards",
        sa.Column(
            "seen_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # 3. Create mastery_score_history table
    op.create_table(
        "mastery_score_history",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "subtopic_id",
            sa.Integer(),
            sa.ForeignKey("subtopics.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("mastery_score", sa.Float(), nullable=False),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_mastery_score_history_user_subtopic_recorded",
        "mastery_score_history",
        ["user_id", "subtopic_id", "recorded_at"],
    )

    # 4. Extend xp_events source CHECK to include MILESTONE_AWARD
    # SQLite does not support ALTER TABLE DROP/ADD CONSTRAINT, so we
    # recreate the table only on non-SQLite engines. On SQLite (dev/test)
    # the CHECK is advisory and the enum guard in XPService is the backstop.
    bind = op.get_bind()
    if bind.dialect.name != "sqlite":
        op.drop_constraint("ck_xp_events_source", "xp_events", type_="check")
        op.create_check_constraint(
            "ck_xp_events_source",
            "xp_events",
            "source IN ("
            "'LESSON_FIRST_COMPLETE', 'QUIZ_PASS', 'QUIZ_PERFECT', "
            "'MOCK_PASS', 'STREAK_DAY', 'FLASHCARD_REVIEW', "
            "'ADMIN_CORRECTION', 'MILESTONE_AWARD')",
        )


def downgrade() -> None:
    # Reverse order

    # 4. Revert xp_events CHECK constraint
    bind = op.get_bind()
    if bind.dialect.name != "sqlite":
        op.drop_constraint("ck_xp_events_source", "xp_events", type_="check")
        op.create_check_constraint(
            "ck_xp_events_source",
            "xp_events",
            "source IN ("
            "'LESSON_FIRST_COMPLETE', 'QUIZ_PASS', 'QUIZ_PERFECT', "
            "'MOCK_PASS', 'STREAK_DAY', 'FLASHCARD_REVIEW', "
            "'ADMIN_CORRECTION')",
        )

    # 3. Drop mastery_score_history
    op.drop_index("ix_mastery_score_history_user_subtopic_recorded",
                  table_name="mastery_score_history")
    op.drop_table("mastery_score_history")

    # 2. Remove seen_at
    op.drop_column("competence_milestone_awards", "seen_at")

    # 1. Remove xp_reward
    op.drop_column("competence_milestones", "xp_reward")
