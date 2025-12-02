"""Add iterations, variations, and referrals

Revision ID: 004
Revises: 003
Create Date: 2025-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create iterations table
    op.create_table(
        'iterations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('parent_iteration_id', sa.String(), nullable=True),
        sa.Column('ifc_url', sa.String(), nullable=True),
        sa.Column('ifc_filename', sa.String(), nullable=True),
        sa.Column('changes_json', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
        sa.ForeignKeyConstraint(['parent_iteration_id'], ['iterations.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_iterations_id'), 'iterations', ['id'], unique=False)
    op.create_index(op.f('ix_iterations_job_id'), 'iterations', ['job_id'], unique=False)

    # Create layout_variations table
    op.create_table(
        'layout_variations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('variation_number', sa.Integer(), nullable=True),
        sa.Column('plan_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('ifc_url', sa.String(), nullable=True),
        sa.Column('preview_image_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_layout_variations_id'), 'layout_variations', ['id'], unique=False)
    op.create_index(op.f('ix_layout_variations_job_id'), 'layout_variations', ['job_id'], unique=False)

    # Create referrals table
    op.create_table(
        'referrals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('referrer_id', sa.Integer(), nullable=False),
        sa.Column('referred_id', sa.Integer(), nullable=True),
        sa.Column('referral_code', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('credits_awarded', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('rewarded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['referred_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referrals_id'), 'referrals', ['id'], unique=False)
    op.create_index(op.f('ix_referrals_referral_code'), 'referrals', ['referral_code'], unique=True)
    op.create_index(op.f('ix_referrals_referrer_id'), 'referrals', ['referrer_id'], unique=False)
    op.create_index(op.f('ix_referrals_referred_id'), 'referrals', ['referred_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_referrals_referred_id'), table_name='referrals')
    op.drop_index(op.f('ix_referrals_referrer_id'), table_name='referrals')
    op.drop_index(op.f('ix_referrals_referral_code'), table_name='referrals')
    op.drop_index(op.f('ix_referrals_id'), table_name='referrals')
    op.drop_table('referrals')
    
    op.drop_index(op.f('ix_layout_variations_job_id'), table_name='layout_variations')
    op.drop_index(op.f('ix_layout_variations_id'), table_name='layout_variations')
    op.drop_table('layout_variations')
    
    op.drop_index(op.f('ix_iterations_job_id'), table_name='iterations')
    op.drop_index(op.f('ix_iterations_id'), table_name='iterations')
    op.drop_table('iterations')

