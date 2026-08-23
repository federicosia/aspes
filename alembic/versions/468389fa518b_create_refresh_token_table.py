"""create refresh token table

Revision ID: 468389fa518b
Revises: c0e51d989491
Create Date: 2026-06-16 21:36:21.432660

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "468389fa518b"
down_revision: Union[str, Sequence[str], None] = "c0e51d989491"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TYPE FAMILY as ENUM (
            'MOBILE',
            'DESKTOP'
        );

        CREATE TABLE refresh_tokens (
            id          SERIAL PRIMARY KEY,
            token       TEXT NOT NULL UNIQUE,
            user_id     SERIAL NOT NULL REFERENCES _user(id) ON DELETE CASCADE,
            family      FAMILY NOT NULL,
            expires_at  TIMESTAMPTZ NOT NULL,
            revoked     BOOLEAN NOT NULL DEFAULT FALSE,
            created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
            user_agent  TEXT
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
