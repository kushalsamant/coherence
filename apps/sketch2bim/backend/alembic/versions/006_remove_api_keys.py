"""Remove api_keys table
Revision ID: 006
Revises: 005
Create Date: 2025-01-16 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop api_keys table
    op.drop_table('api_keys')


def downgrade() -> None:
    # Recreate api_keys table (for rollback)
    op.create_table(
        'api_keys',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('rate_limit_per_minute', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('rate_limit_per_hour', sa.Integer(), nullable=True, server_default='100'),
        sa.Column('total_requests', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api_keys_id'), 'api_keys', ['id'], unique=False)
    op.create_index(op.f('ix_api_keys_key'), 'api_keys', ['key'], unique=True)
    op.create_index(op.f('ix_api_keys_user_id'), 'api_keys', ['user_id'], unique=False)

