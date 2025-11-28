"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('google_id', sa.String(), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('subscription_tier', sa.String(), nullable=True, server_default='trial'),
        sa.Column('subscription_status', sa.String(), nullable=True, server_default='inactive'),
        sa.Column('stripe_customer_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)
    op.create_index(op.f('ix_users_stripe_customer_id'), 'users', ['stripe_customer_id'], unique=True)

    # Create jobs table
    op.create_table(
        'jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=True, server_default='queued'),
        sa.Column('progress', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('sketch_filename', sa.String(), nullable=True),
        sa.Column('sketch_url', sa.String(), nullable=True),
        sa.Column('sketch_format', sa.String(), nullable=True),
        sa.Column('reader_type', sa.String(), nullable=True),
        sa.Column('detection_confidence', sa.Float(), nullable=True),
        sa.Column('plan_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ifc_url', sa.String(), nullable=True),
        sa.Column('dwg_url', sa.String(), nullable=True),
        sa.Column('rvt_url', sa.String(), nullable=True),
        sa.Column('model_3dm_url', sa.String(), nullable=True),
        sa.Column('preview_image_url', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('qc_report_path', sa.String(), nullable=True),
        sa.Column('requires_review', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('cost_usd', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)

    # Create api_keys table
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
    op.create_index(op.f('ix_api_keys_key'), 'api_keys', ['key'], unique=True)

    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('stripe_payment_intent_id', sa.String(), nullable=True),
        sa.Column('stripe_checkout_session_id', sa.String(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True, server_default='usd'),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('product_type', sa.String(), nullable=True),
        sa.Column('credits_added', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_stripe_payment_intent_id'), 'payments', ['stripe_payment_intent_id'], unique=True)
    op.create_index(op.f('ix_payments_stripe_checkout_session_id'), 'payments', ['stripe_checkout_session_id'], unique=True)

    # Create project_versions table
    op.create_table(
        'project_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_name', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=True),
        sa.Column('job_id', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_versions_project_name'), 'project_versions', ['project_name'], unique=False)

    # Create organizations table
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slug', sa.String(), nullable=True),
        sa.Column('stripe_customer_id', sa.String(), nullable=True),
        sa.Column('subscription_tier', sa.String(), nullable=True, server_default='trial'),
        sa.Column('shared_credits', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_slug'), 'organizations', ['slug'], unique=True)
    op.create_index(op.f('ix_organizations_stripe_customer_id'), 'organizations', ['stripe_customer_id'], unique=True)

    # Create organization_members table
    op.create_table(
        'organization_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=True, server_default='member'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('organization_id', 'user_id', name='uq_org_user')
    )


def downgrade() -> None:
    op.drop_table('organization_members')
    op.drop_table('organizations')
    op.drop_table('project_versions')
    op.drop_table('payments')
    op.drop_table('api_keys')
    op.drop_table('jobs')
    op.drop_table('users')

