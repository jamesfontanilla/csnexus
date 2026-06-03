"""add_intelligent_learning_engine_tables

Revision ID: 97ae7cd488ca
Revises:
Create Date: 2026-06-03 11:49:10.858004

Creates all new tables for the Intelligent Learning Engine feature:
- readiness_score_history (Req 2.2)
- self_assessment_records (Req 19.2)
- daily_queues (Req 4.5)
- queue_items (Req 4.5, 5.1)
- question_explanations (Req 7.1)
- diagnostic_reports (Req 10.5)
- recommendation_records (Req 12.5)
- competence_milestones (Req 13.5)
- competence_milestone_awards (Req 13.5, 14.4)
- study_consistency (Req 14.4)
- onboarding_profiles (Req 16.4)

Adds new columns to study_plans (Req 17.4):
- exam_category, total_days, subtopics_per_week,
  mock_exams_scheduled, plan_data, estimated_readiness_at_exam
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '97ae7cd488ca'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create Intelligent Learning Engine tables and extend study_plans."""

    # --- Readiness Score History ---
    op.create_table(
        'readiness_score_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('mastery_component', sa.Float(), nullable=False),
        sa.Column('retention_component', sa.Float(), nullable=False),
        sa.Column('mock_component', sa.Float(), nullable=False),
        sa.Column('coverage_component', sa.Float(), nullable=False),
        sa.Column('weights_used', sa.String(length=100), nullable=False),
        sa.Column('computed_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_readiness_score_history_id', 'readiness_score_history', ['id'], unique=False)
    op.create_index('ix_readiness_score_history_user_id', 'readiness_score_history', ['user_id'], unique=False)
    op.create_index('ix_readiness_history_user_computed', 'readiness_score_history', ['user_id', 'computed_at'], unique=False)

    # --- Self Assessment Records ---
    op.create_table(
        'self_assessment_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('self_assessed_score', sa.Integer(), nullable=False),
        sa.Column('computed_score', sa.Integer(), nullable=False),
        sa.Column('delta', sa.Integer(), nullable=False),
        sa.Column('calibration_status', sa.String(length=20), nullable=False),
        sa.Column('assessed_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.CheckConstraint('self_assessed_score >= 0 AND self_assessed_score <= 100', name='ck_self_assessment_score_range'),
        sa.CheckConstraint("calibration_status IN ('overconfident', 'well_calibrated', 'underconfident')", name='ck_calibration_status'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_self_assessment_records_id', 'self_assessment_records', ['id'], unique=False)
    op.create_index('ix_self_assessment_user_assessed', 'self_assessment_records', ['user_id', 'assessed_at'], unique=False)

    # --- Daily Queues ---
    op.create_table(
        'daily_queues',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('queue_date', sa.Date(), nullable=False),
        sa.Column('time_budget_minutes', sa.Integer(), nullable=False),
        sa.Column('total_estimated_seconds', sa.Integer(), nullable=False),
        sa.Column('items_total', sa.Integer(), nullable=False),
        sa.Column('items_completed', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'queue_date', name='uq_daily_queue_user_date'),
    )
    op.create_index('ix_daily_queues_id', 'daily_queues', ['id'], unique=False)
    op.create_index('ix_daily_queues_user_id', 'daily_queues', ['user_id'], unique=False)

    # --- Queue Items ---
    op.create_table(
        'queue_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('queue_id', sa.Integer(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('item_type', sa.String(length=20), nullable=False),
        sa.Column('payload', sa.Text(), nullable=False),
        sa.Column('estimated_seconds', sa.Integer(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("item_type IN ('flashcard_review', 'quiz_practice', 'new_content')", name='ck_queue_items_type'),
        sa.ForeignKeyConstraint(['queue_id'], ['daily_queues.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_queue_items_id', 'queue_items', ['id'], unique=False)
    op.create_index('ix_queue_items_queue_id', 'queue_items', ['queue_id'], unique=False)
    op.create_index('ix_queue_items_queue_position', 'queue_items', ['queue_id', 'position'], unique=False)

    # --- Question Explanations ---
    op.create_table(
        'question_explanations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('explanation_text', sa.Text(), nullable=False),
        sa.Column('key_concept', sa.String(length=100), nullable=False),
        sa.Column('related_subtopics', sa.Text(), nullable=False),
        sa.Column('cache_version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_question_explanations_id', 'question_explanations', ['id'], unique=False)
    op.create_index('ix_question_explanations_question_id', 'question_explanations', ['question_id'], unique=True)

    # --- Diagnostic Reports ---
    op.create_table(
        'diagnostic_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('mock_exam_attempt_id', sa.Integer(), nullable=False),
        sa.Column('total_score', sa.Float(), nullable=False),
        sa.Column('subtopic_breakdowns', sa.Text(), nullable=False),
        sa.Column('highest_impact_areas', sa.Text(), nullable=False),
        sa.Column('regression_alerts', sa.Text(), nullable=False),
        sa.Column('difficulty_performance', sa.Text(), nullable=False),
        sa.Column('predicted_score_range', sa.Text(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['mock_exam_attempt_id'], ['mock_exam_attempts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('mock_exam_attempt_id'),
    )
    op.create_index('ix_diagnostic_reports_id', 'diagnostic_reports', ['id'], unique=False)
    op.create_index('ix_diagnostic_reports_user_id', 'diagnostic_reports', ['user_id'], unique=False)

    # --- Recommendation Records ---
    op.create_table(
        'recommendation_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('report_id', sa.Integer(), nullable=False),
        sa.Column('subtopic_id', sa.Integer(), nullable=False),
        sa.Column('subtopic_name', sa.String(length=255), nullable=False),
        sa.Column('current_accuracy', sa.Float(), nullable=False),
        sa.Column('target_accuracy', sa.Float(), nullable=False),
        sa.Column('estimated_point_gain', sa.Float(), nullable=False),
        sa.Column('recommended_action', sa.String(length=16), nullable=False),
        sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.CheckConstraint("recommended_action IN ('review', 'practice', 're-learn')", name='ck_recommendations_action'),
        sa.ForeignKeyConstraint(['report_id'], ['diagnostic_reports.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subtopic_id'], ['subtopics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_recommendation_records_id', 'recommendation_records', ['id'], unique=False)
    op.create_index('ix_recommendation_records_report_id', 'recommendation_records', ['report_id'], unique=False)

    # --- Competence Milestones ---
    op.create_table(
        'competence_milestones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=20), nullable=False),
        sa.Column('threshold_config', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('ix_competence_milestones_id', 'competence_milestones', ['id'], unique=False)

    # --- Competence Milestone Awards ---
    op.create_table(
        'competence_milestone_awards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('milestone_id', sa.Integer(), nullable=False),
        sa.Column('triggering_values', sa.Text(), nullable=False),
        sa.Column('awarded_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['milestone_id'], ['competence_milestones.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'milestone_id', name='uq_milestone_award_user_milestone'),
    )
    op.create_index('ix_competence_milestone_awards_id', 'competence_milestone_awards', ['id'], unique=False)
    op.create_index('ix_competence_milestone_awards_user_id', 'competence_milestone_awards', ['user_id'], unique=False)

    # --- Study Consistency ---
    op.create_table(
        'study_consistency',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('current_streak', sa.Integer(), server_default='0', nullable=False),
        sa.Column('longest_streak', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_consistent_days', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_qualifying_date', sa.Date(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index('ix_study_consistency_id', 'study_consistency', ['id'], unique=False)

    # --- Onboarding Profiles ---
    op.create_table(
        'onboarding_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exam_date', sa.Date(), nullable=False),
        sa.Column('exam_category', sa.String(length=20), nullable=False),
        sa.Column('time_budget_minutes', sa.Integer(), server_default='30', nullable=False),
        sa.Column('onboarding_completed_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.CheckConstraint("exam_category IN ('Professional', 'Sub-Professional')", name='ck_onboarding_category'),
        sa.CheckConstraint('time_budget_minutes IN (15, 30, 60)', name='ck_onboarding_time_budget'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.create_index('ix_onboarding_profiles_id', 'onboarding_profiles', ['id'], unique=False)

    # --- Add new columns to study_plans (Req 17.4) ---
    op.add_column('study_plans', sa.Column('exam_category', sa.String(length=20), nullable=True))
    op.add_column('study_plans', sa.Column('total_days', sa.Integer(), nullable=True))
    op.add_column('study_plans', sa.Column('subtopics_per_week', sa.Integer(), nullable=True))
    op.add_column('study_plans', sa.Column('mock_exams_scheduled', sa.Integer(), nullable=True))
    op.add_column('study_plans', sa.Column('plan_data', sa.Text(), nullable=True))
    op.add_column('study_plans', sa.Column('estimated_readiness_at_exam', sa.Float(), nullable=True))


def downgrade() -> None:
    """Remove Intelligent Learning Engine tables and study_plans columns."""

    # --- Remove study_plans columns ---
    op.drop_column('study_plans', 'estimated_readiness_at_exam')
    op.drop_column('study_plans', 'plan_data')
    op.drop_column('study_plans', 'mock_exams_scheduled')
    op.drop_column('study_plans', 'subtopics_per_week')
    op.drop_column('study_plans', 'total_days')
    op.drop_column('study_plans', 'exam_category')

    # --- Drop tables in reverse dependency order ---
    op.drop_index('ix_onboarding_profiles_id', table_name='onboarding_profiles')
    op.drop_table('onboarding_profiles')

    op.drop_index('ix_study_consistency_id', table_name='study_consistency')
    op.drop_table('study_consistency')

    op.drop_index('ix_competence_milestone_awards_user_id', table_name='competence_milestone_awards')
    op.drop_index('ix_competence_milestone_awards_id', table_name='competence_milestone_awards')
    op.drop_table('competence_milestone_awards')

    op.drop_index('ix_competence_milestones_id', table_name='competence_milestones')
    op.drop_table('competence_milestones')

    op.drop_index('ix_recommendation_records_report_id', table_name='recommendation_records')
    op.drop_index('ix_recommendation_records_id', table_name='recommendation_records')
    op.drop_table('recommendation_records')

    op.drop_index('ix_diagnostic_reports_user_id', table_name='diagnostic_reports')
    op.drop_index('ix_diagnostic_reports_id', table_name='diagnostic_reports')
    op.drop_table('diagnostic_reports')

    op.drop_index('ix_question_explanations_question_id', table_name='question_explanations')
    op.drop_index('ix_question_explanations_id', table_name='question_explanations')
    op.drop_table('question_explanations')

    op.drop_index('ix_queue_items_queue_position', table_name='queue_items')
    op.drop_index('ix_queue_items_queue_id', table_name='queue_items')
    op.drop_index('ix_queue_items_id', table_name='queue_items')
    op.drop_table('queue_items')

    op.drop_index('ix_daily_queues_user_id', table_name='daily_queues')
    op.drop_index('ix_daily_queues_id', table_name='daily_queues')
    op.drop_table('daily_queues')

    op.drop_index('ix_self_assessment_user_assessed', table_name='self_assessment_records')
    op.drop_index('ix_self_assessment_records_id', table_name='self_assessment_records')
    op.drop_table('self_assessment_records')

    op.drop_index('ix_readiness_history_user_computed', table_name='readiness_score_history')
    op.drop_index('ix_readiness_score_history_user_id', table_name='readiness_score_history')
    op.drop_index('ix_readiness_score_history_id', table_name='readiness_score_history')
    op.drop_table('readiness_score_history')
