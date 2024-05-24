"""empty message

Revision ID: 387360f58220
Revises: 
Create Date: 2024-03-31 16:54:40.158910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '387360f58220'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admonition', schema=None) as batch_op:
        batch_op.add_column(sa.Column('processed_file_url', sa.String(length=50), nullable=True))

    with op.batch_alter_table('school_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('authorized_users', sa.String(length=100), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_units', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('time_units')

    with op.batch_alter_table('school_list', schema=None) as batch_op:
        batch_op.drop_column('authorized_users')

    with op.batch_alter_table('admonition', schema=None) as batch_op:
        batch_op.drop_column('processed_file_url')

    # ### end Alembic commands ###
