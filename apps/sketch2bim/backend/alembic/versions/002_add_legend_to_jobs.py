"""Add legend to jobs

Revision ID: 002
Revises: 001
Create Date: 2025-01-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add legend_data and legend_detected columns to jobs table
    op.add_column('jobs', sa.Column('legend_data', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('jobs', sa.Column('legend_detected', sa.Boolean(), nullable=True, server_default='false'))


def downgrade() -> None:
    # Remove legend columns from jobs table
    op.drop_column('jobs', 'legend_detected')
    op.drop_column('jobs', 'legend_data')

