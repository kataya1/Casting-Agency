"""empty message

Revision ID: 60713029ded0
Revises: 2268bb14e83a
Create Date: 2020-08-17 22:09:25.055069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60713029ded0'
down_revision = '2268bb14e83a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Actor', sa.Column('t', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Actor', 't')
    # ### end Alembic commands ###