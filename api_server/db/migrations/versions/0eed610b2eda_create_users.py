"""Create users

Revision ID: 0eed610b2eda
Revises: 
Create Date: 2021-01-12 15:00:18.024335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0eed610b2eda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('users')
    # ### end Alembic commands ###
