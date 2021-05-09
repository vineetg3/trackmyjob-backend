"""empty message

Revision ID: 8297af31c2ba
Revises: de572cc64232
Create Date: 2021-05-04 01:27:59.909492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8297af31c2ba'
down_revision = 'de572cc64232'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userJobs', sa.Column('status', sa.Enum('saved', 'applied', 'interviewing', 'hired', 'rejected', 'archived', name='statustypes'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userJobs', 'status')
    # ### end Alembic commands ###