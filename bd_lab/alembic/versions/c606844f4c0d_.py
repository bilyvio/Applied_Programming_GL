"""empty message

Revision ID: c606844f4c0d
Revises: 79700b91ffc3
Create Date: 2020-12-08 23:02:17.627934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c606844f4c0d'
down_revision = '79700b91ffc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('homePage', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('location', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('announcement',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('releaseDate', sa.VARCHAR(length=30), nullable=True),
    sa.Column('local', sa.Integer(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=30), nullable=True),
    sa.Column('manufacturer_uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['manufacturer_uid'], ['category.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('announcement')
    op.drop_table('users')
    op.drop_table('category')
    # ### end Alembic commands ###
