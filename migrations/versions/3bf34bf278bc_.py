"""empty message

Revision ID: 3bf34bf278bc
Revises: 51c4decc4834
Create Date: 2024-04-03 23:56:17.201530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf34bf278bc'
down_revision = '51c4decc4834'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workbook', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workbook', schema=None) as batch_op:
        batch_op.drop_column('amount')

    # ### end Alembic commands ###