"""empty message

Revision ID: 5a206e553bfb
Revises: ce23b08c6aa3
Create Date: 2024-04-24 15:34:07.975790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a206e553bfb'
down_revision = 'ce23b08c6aa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pupil', schema=None) as batch_op:
        batch_op.alter_column('communication_pupil',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('communication_tutor1',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('communication_tutor2',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String(length=50),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tutoring', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('contact', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('contact')
        batch_op.drop_column('tutoring')

    with op.batch_alter_table('pupil', schema=None) as batch_op:
        batch_op.alter_column('communication_tutor2',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)
        batch_op.alter_column('communication_tutor1',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)
        batch_op.alter_column('communication_pupil',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)

    # ### end Alembic commands ###
