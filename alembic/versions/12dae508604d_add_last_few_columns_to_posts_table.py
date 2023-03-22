"""add last few columns to posts table

Revision ID: 12dae508604d
Revises: c2dc6f2d714e
Create Date: 2023-03-21 17:44:29.457873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12dae508604d'
down_revision = 'c2dc6f2d714e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=True, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
