"""create user table

Revision ID: c0e51d989491
Revises: 69f8822e072b
Create Date: 2026-05-29 18:47:16.161560

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c0e51d989491"
down_revision: Union[str, Sequence[str], None] = "69f8822e072b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TYPE role AS ENUM ('USER', 'ADMIN');
        CREATE TYPE status AS ENUM ('ENABLED', 'DISABLED');

        CREATE TABLE IF NOT EXISTS "_user" (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            username VARCHAR(255) NOT NULL UNIQUE,
            hashed_password VARCHAR(255) NOT NULL,
            role role NOT NULL,
            status status NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP TABLE IF EXISTS "_user";
        DROP TYPE IF EXISTS role;
        DROP TYPE IF EXISTS status;
        """
    )
