"""empty message

Revision ID: 85092d6f4b92
Revises: 39a50df1a298
Create Date: 2023-05-01 17:39:13.303826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85092d6f4b92'
down_revision = '39a50df1a298'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('permission', sa.String(length=20), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('permission')

    # ### end Alembic commands ###
