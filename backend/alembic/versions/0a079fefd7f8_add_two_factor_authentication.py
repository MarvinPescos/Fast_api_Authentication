"""add_two_factor_authentication

Revision ID: 0a079fefd7f8
Revises: 0041a90393c1
Create Date: 2025-10-18 19:42:30.925032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a079fefd7f8'
down_revision = '0041a90393c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add two-factor authentication columns
    op.add_column('users', sa.Column('two_factor_enabled', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('two_factor_secret', sa.String(length=32), nullable=True))


def downgrade() -> None:
    # Remove two-factor authentication columns
    op.drop_column('users', 'two_factor_secret')
    op.drop_column('users', 'two_factor_enabled')
