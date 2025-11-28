"""Add project_type to jobs
Revision ID: 009
Revises: 008
Create Date: 2025-01-20 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add project_type column to jobs table with default 'architecture'
    op.add_column('jobs', sa.Column('project_type', sa.String(), nullable=True, server_default='architecture'))
    # Update existing rows to have 'architecture' as default
    op.execute("UPDATE jobs SET project_type = 'architecture' WHERE project_type IS NULL")


def downgrade() -> None:
    # Remove project_type column
    op.drop_column('jobs', 'project_type')

