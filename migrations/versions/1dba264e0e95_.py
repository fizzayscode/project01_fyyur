"""empty message

Revision ID: 1dba264e0e95
Revises: 64d5e5055e0b
Create Date: 2022-08-08 01:59:28.178948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dba264e0e95'
down_revision = '64d5e5055e0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'start_time')
    # ### end Alembic commands ###
