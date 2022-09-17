"""empty message

Revision ID: 8caf87f09d07
Revises: 9e9789d4ae5d
Create Date: 2022-08-05 10:10:24.859351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8caf87f09d07'
down_revision = '9e9789d4ae5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('Artist', 'description')
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.drop_column('Venue', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_description')
    op.add_column('Artist', sa.Column('description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
