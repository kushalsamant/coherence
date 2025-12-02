"""Initial ASK database schema

Revision ID: 001
Revises: 
Create Date: 2025-12-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('google_id', sa.String(), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('subscription_tier', sa.String(), nullable=True, server_default='trial'),
        sa.Column('subscription_status', sa.String(), nullable=True, server_default='inactive'),
        sa.Column('razorpay_customer_id', sa.String(), nullable=True),
        sa.Column('subscription_expires_at', sa.DateTime(), nullable=True),
        sa.Column('razorpay_subscription_id', sa.String(), nullable=True),
        sa.Column('subscription_auto_renew', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)
    op.create_index(op.f('ix_users_razorpay_customer_id'), 'users', ['razorpay_customer_id'], unique=True)
    op.create_index(op.f('ix_users_razorpay_subscription_id'), 'users', ['razorpay_subscription_id'], unique=False)

    # Payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('razorpay_payment_id', sa.String(), nullable=True),
        sa.Column('razorpay_order_id', sa.String(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True, server_default='INR'),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('product_type', sa.String(), nullable=True),
        sa.Column('credits_added', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('processing_fee', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_razorpay_payment_id'), 'payments', ['razorpay_payment_id'], unique=True)
    op.create_index(op.f('ix_payments_razorpay_order_id'), 'payments', ['razorpay_order_id'], unique=True)

    # Groq Usage table
    op.create_table(
        'groq_usage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('input_tokens', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('output_tokens', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_tokens', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('cost_usd', sa.String(), nullable=True, server_default='0.0'),
        sa.Column('model', sa.String(), nullable=True, server_default='llama-3.1-70b-versatile'),
        sa.Column('request_type', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groq_usage_created_at'), 'groq_usage', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_groq_usage_created_at'), table_name='groq_usage')
    op.drop_table('groq_usage')
    op.drop_index(op.f('ix_payments_razorpay_order_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_razorpay_payment_id'), table_name='payments')
    op.drop_table('payments')
    op.drop_index(op.f('ix_users_razorpay_subscription_id'), table_name='users')
    op.drop_index(op.f('ix_users_razorpay_customer_id'), table_name='users')
    op.drop_index(op.f('ix_users_google_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

