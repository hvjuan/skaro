"""Initial URL and Log models

Revision ID: fefc1158305f
Revises: 
Create Date: 2019-10-10 12:19:08.913977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fefc1158305f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('custom', sa.Boolean(), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('short_url', sa.String(length=16), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_url_short_url'), 'url', ['short_url'], unique=False)
    op.create_index(op.f('ix_url_url'), 'url', ['url'], unique=False)
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=16), nullable=True),
    sa.Column('activity_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['url_id'], ['url.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    op.drop_index(op.f('ix_url_url'), table_name='url')
    op.drop_index(op.f('ix_url_short_url'), table_name='url')
    op.drop_table('url')
    # ### end Alembic commands ###
