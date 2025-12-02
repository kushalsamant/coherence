"""Add subscription tracking fields
Revision ID: 008
Revises: 007
Create Date: 2025-01-16 18:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '008'
down_revision = '007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add subscription tracking fields to users table
    op.add_column('users', sa.Column('razorpay_subscription_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('subscription_auto_renew', sa.Boolean(), nullable=True, server_default='false'))
    op.create_index(op.f('ix_users_razorpay_subscription_id'), 'users', ['razorpay_subscription_id'], unique=False)


def downgrade() -> None:
    # Remove subscription tracking fields
    op.drop_index(op.f('ix_users_razorpay_subscription_id'), table_name='users')
    op.drop_column('users', 'subscription_auto_renew')
    op.drop_column('users', 'razorpay_subscription_id')

