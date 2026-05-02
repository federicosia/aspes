"""init db

Revision ID: 69f8822e072b
Revises:
Create Date: 2026-05-02 22:39:37.363551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "69f8822e072b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TYPE repetition AS ENUM ('DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY');

        CREATE TABLE IF NOT EXISTS "category" (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS "transaction" (
            id SERIAL PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            description TEXT,
            repetition repetition,
            category_id int NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DROP TABLE IF EXISTS "transaction";
        DROP TABLE IF EXISTS "category";
        DROP TYPE IF EXISTS repetition;
        """
    )
