"""Remove reader_type column from jobs

Revision ID: 010
Revises: 009
Create Date: 2025-01-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '010'
down_revision: Union[str, None] = '009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove reader_type column from jobs table
    # This column is deprecated - always uses OpenCV reader
    op.drop_column('jobs', 'reader_type')


def downgrade() -> None:
    # Re-add reader_type column for rollback
    op.add_column('jobs', sa.Column('reader_type', sa.String(), nullable=True))

