"""Add subscription_expires_at to users

Revision ID: 007
Revises: 006
Create Date: 2025-01-16 15:30:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('subscription_expires_at', sa.DateTime(), nullable=True))
    # Optionally set existing active subscriptions to far future
    op.execute("""
        UPDATE users
        SET subscription_expires_at = NOW() + INTERVAL '30 days'
        WHERE subscription_status = 'active' AND subscription_expires_at IS NULL
    """)
    op.alter_column('organizations', 'subscription_tier', server_default='trial')
    op.execute("UPDATE organizations SET subscription_tier = 'trial' WHERE subscription_tier IS NULL OR subscription_tier = 'free'")


def downgrade() -> None:
    op.alter_column('organizations', 'subscription_tier', server_default='trial')
    op.drop_column('users', 'subscription_expires_at')

