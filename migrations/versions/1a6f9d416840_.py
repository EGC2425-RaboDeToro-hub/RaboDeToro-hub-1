"""empty message

Revision ID: 1a6f9d416840
Revises: c652e9f03381
Create Date: 2024-11-12 19:00:46.190695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a6f9d416840'
down_revision = 'c652e9f03381'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('community', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=10), nullable=False))
        batch_op.create_unique_constraint(None, ['code'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('community', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('code')

    # ### end Alembic commands ###
