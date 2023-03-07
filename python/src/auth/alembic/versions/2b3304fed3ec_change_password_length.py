"""change password length

Revision ID: 2b3304fed3ec
Revises: 466f5d151e97
Create Date: 2023-03-05 21:10:31.024447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b3304fed3ec'
down_revision = '466f5d151e97'
branch_labels = None
depends_on = None


def upgrade():
    # Alter the 'users' table
    with op.batch_alter_table('user') as batch_op:
        # Make the 'email' field unique
        batch_op.alter_column('email', unique=True)
        # Change the length of the 'password' field to 100
        batch_op.alter_column('password', type_=sa.String(length=150))


def downgrade():
    pass
