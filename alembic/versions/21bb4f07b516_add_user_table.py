"""add user table

Revision ID: 21bb4f07b516
Revises: 1b5e3d372d32
Create Date: 2023-03-21 17:13:40.878003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21bb4f07b516'
down_revision = '1b5e3d372d32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
