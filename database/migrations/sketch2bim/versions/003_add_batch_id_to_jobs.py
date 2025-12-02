"""Add batch_id to jobs

Revision ID: 003
Revises: 002
Create Date: 2025-01-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add batch_id column to jobs table
    op.add_column('jobs', sa.Column('batch_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_jobs_batch_id'), 'jobs', ['batch_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_jobs_batch_id'), table_name='jobs')
    op.drop_column('jobs', 'batch_id')

