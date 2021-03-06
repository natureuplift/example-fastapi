"""add phone number

Revision ID: 73dcbdc5a713
Revises: e610255d15dd
Create Date: 2022-01-04 00:45:40.310396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73dcbdc5a713'
down_revision = 'e610255d15dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
