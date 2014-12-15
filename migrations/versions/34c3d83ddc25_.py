"""empty message

Revision ID: 34c3d83ddc25
Revises: 354700e006cf
Create Date: 2014-12-15 14:43:11.502921

"""

# revision identifiers, used by Alembic.
revision = '34c3d83ddc25'
down_revision = '354700e006cf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('urlname', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'urlname')
    ### end Alembic commands ###
