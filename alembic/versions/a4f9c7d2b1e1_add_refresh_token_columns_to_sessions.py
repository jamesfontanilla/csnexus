"""add_refresh_token_columns_to_sessions

Revision ID: a4f9c7d2b1e1
Revises: 97ae7cd488ca
Create Date: 2026-06-09 15:25:00.000000

Adds refresh-token tracking columns to auth sessions so the backend can
rotate refresh tokens and keep Android/native clients signed in safely.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4f9c7d2b1e1"
down_revision: Union[str, Sequence[str], None] = "97ae7cd488ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sessions",
        sa.Column("refresh_jti", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "sessions",
        sa.Column("refresh_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f("ix_sessions_refresh_jti"), "sessions", ["refresh_jti"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_sessions_refresh_jti"), table_name="sessions")
    op.drop_column("sessions", "refresh_expires_at")
    op.drop_column("sessions", "refresh_jti")
