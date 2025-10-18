"""add cat fact subscriptions table

Revision ID: add_cat_fact_subscriptions
Revises: cc8a358ea6f3
Create Date: 2025-10-18 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_cat_fact_subscriptions'
down_revision = 'cc8a358ea6f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create cat_fact_subscriptions table
    op.create_table('cat_fact_subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('preferred_time', sa.Time(), nullable=False),
    sa.Column('timezone', sa.String(length=50), nullable=False),
    sa.Column('last_sent_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('total_sent', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_cat_fact_subscriptions_id'), 'cat_fact_subscriptions', ['id'], unique=False)
    op.create_index(op.f('ix_cat_fact_subscriptions_user_id'), 'cat_fact_subscriptions', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop cat_fact_subscriptions table
    op.drop_index(op.f('ix_cat_fact_subscriptions_user_id'), table_name='cat_fact_subscriptions')
    op.drop_index(op.f('ix_cat_fact_subscriptions_id'), table_name='cat_fact_subscriptions')
    op.drop_table('cat_fact_subscriptions')
