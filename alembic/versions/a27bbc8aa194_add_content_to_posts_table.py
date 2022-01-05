"""add content to posts table

Revision ID: a27bbc8aa194
Revises: 9de5114964e0
Create Date: 2022-01-04 00:30:14.377739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a27bbc8aa194'
down_revision = '9de5114964e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
