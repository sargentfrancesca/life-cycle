"""empty message

Revision ID: 53a73e499be0
Revises: 4ff2a7add324
Create Date: 2015-02-10 15:41:46.984054

"""

# revision identifiers, used by Alembic.
revision = '53a73e499be0'
down_revision = '4ff2a7add324'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
#    op.create_table('page',
 #   sa.Column('id', sa.Integer(), nullable=False),
  #  sa.Column('pagetype', sa.String(length=64), nullable=True),
   # sa.Column('title', sa.String(length=64), nullable=True),
    #sa.Column('publish', sa.Boolean(), nullable=True),
    #sa.Column('content', sa.Text(), nullable=True),
    #sa.Column('content_html', sa.Text(), nullable=True),
    #sa.Column('author_id', sa.Integer(), nullable=True),
    #sa.Column('project_name', sa.String(length=100), nullable=True),
    #sa.Column('image_url', sa.String(length=100), nullable=True),
    #sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    #sa.ForeignKeyConstraint(['image_url'], ['uploads.filename'], ),
    #sa.ForeignKeyConstraint(['project_name'], ['projects.urlname'], ),
    #sa.PrimaryKeyConstraint('id')
    #)
    #op.create_index('ix_page_id', 'page', ['id'], unique=False)
    #op.drop_index('fkplantspecies', 'plant')
    #op.drop_index('id_2', 'species')
    pass
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index('id_2', 'species', [u'id'], unique=False)
    op.create_index('fkplantspecies', 'plant', [u'species_id'], unique=False)
    op.drop_index('ix_page_id', 'page')
    op.drop_table('page')
    ### end Alembic commands ###