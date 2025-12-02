"""Add sketchup_url to jobs

Revision ID: 005
Revises: 004
Create Date: 2025-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add sketchup_url column to jobs table
    op.add_column('jobs', sa.Column('sketchup_url', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove sketchup_url column
    op.drop_column('jobs', 'sketchup_url')

