"""empty message

Revision ID: 64d5e5055e0b
Revises: 179da898b33d
Create Date: 2022-08-07 11:00:41.675121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d5e5055e0b'
down_revision = '179da898b33d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist_shows',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('shows_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['shows_id'], ['shows.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'shows_id')
    )
    op.drop_constraint('shows_artist_id_fkey', 'shows', type_='foreignkey')
    op.drop_column('shows', 'artist_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('shows_artist_id_fkey', 'shows', 'Artist', ['artist_id'], ['id'])
    op.drop_table('artist_shows')
    # ### end Alembic commands ###
