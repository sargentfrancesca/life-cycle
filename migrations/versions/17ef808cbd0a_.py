"""empty message

Revision ID: 17ef808cbd0a
Revises: 348eb6cc6b34
Create Date: 2015-02-05 14:47:47.653024

"""

# revision identifiers, used by Alembic.
revision = '17ef808cbd0a'
down_revision = '348eb6cc6b34'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('plantspecies', 'plant', [u'species_id'], unique=False)
    ### end Alembic commands ###
