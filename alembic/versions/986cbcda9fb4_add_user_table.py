"""add user table

Revision ID: 986cbcda9fb4
Revises: a27bbc8aa194
Create Date: 2022-01-04 00:31:18.437385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '986cbcda9fb4'
down_revision = 'a27bbc8aa194'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),sa.PrimaryKeyConstraint('id'),sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass

