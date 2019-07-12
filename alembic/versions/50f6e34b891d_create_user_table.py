"""create_user_table

Revision ID: 50f6e34b891d
Revises: 
Create Date: 2019-07-11 15:45:35.556041

"""
import pymysql
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String


# revision identifiers, used by Alembic.
revision = '50f6e34b891d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        Column('id', Integer, primary_key=True,
               autoincrement=True, default=0),
        Column('name', String(255), nullable=False),
        Column('password', String(1000), nullable=False),
        Column('username', String(256), nullable=False)
    )


def downgrade():
    op.drop_table('users')
