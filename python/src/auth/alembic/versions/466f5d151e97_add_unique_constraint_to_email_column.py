"""Add unique constraint to email column

Revision ID: 466f5d151e97
Revises: 
Create Date: 2023-03-05 16:23:13.567730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '466f5d151e97'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id',sa.Integer, primary_key = True, autoincrement = True),
        sa.Column('email',sa.String(50),unique = True),
        sa.Column('password',sa.String(150)),
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
