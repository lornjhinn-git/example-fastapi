"""add content column to posts table

Revision ID: 1b5e3d372d32
Revises: eb162b3d9cbc
Create Date: 2023-03-21 17:07:35.144785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b5e3d372d32'
down_revision = 'eb162b3d9cbc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
