"""empty message

Revision ID: ca6537cd4191
Revises: 78abdf87d56a
Create Date: 2023-05-01 20:50:57.094036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca6537cd4191'
down_revision = '78abdf87d56a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cell_number', sa.BigInteger(), nullable=False))
        batch_op.add_column(sa.Column('email_address', sa.String(length=30), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('email_address')
        batch_op.drop_column('cell_number')

    # ### end Alembic commands ###