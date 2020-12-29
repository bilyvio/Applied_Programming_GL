"""empty message

Revision ID: 214bb5420fe5
Revises: c02d0bd72204
Create Date: 2020-12-23 23:07:27.647816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '214bb5420fe5'
down_revision = 'c02d0bd72204'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('announcement', sa.Column('owner_uid', sa.Integer(), nullable=True))
    op.drop_constraint('announcement_manufacturer_uid_fkey', 'announcement', type_='foreignkey')
    op.create_foreign_key(None, 'announcement', 'users', ['owner_uid'], ['uid'])
    op.drop_column('announcement', 'manufacturer_uid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('announcement', sa.Column('manufacturer_uid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'announcement', type_='foreignkey')
    op.create_foreign_key('announcement_manufacturer_uid_fkey', 'announcement', 'category', ['manufacturer_uid'], ['uid'])
    op.drop_column('announcement', 'owner_uid')
    # ### end Alembic commands ###
