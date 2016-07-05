"""empty message

Revision ID: 553b3a36d3fa
Revises: 76cb7483f80b
Create Date: 2016-07-05 17:15:36.994403

"""

# revision identifiers, used by Alembic.
revision = '553b3a36d3fa'
down_revision = '76cb7483f80b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('width', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('rotation', sa.Integer(), nullable=True),
    sa.Column('duration', sa.BigInteger(), nullable=True),
    sa.Column('size', sa.BigInteger(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('bitrate', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=True),
    sa.Column('video_type', sa.Enum('Edited', 'Recorded', 'Gallery', name='video_types'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    ### end Alembic commands ###
