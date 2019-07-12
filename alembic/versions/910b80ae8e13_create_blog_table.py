"""create_blog_table

Revision ID: 910b80ae8e13
Revises: 50f6e34b891d
Create Date: 2019-07-11 16:33:30.382672

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, Integer, String, ForeignKey


# revision identifiers, used by Alembic.
revision = '910b80ae8e13'
down_revision = '50f6e34b891d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'blog_posts',
        Column('id', Integer, primary_key=True,
               autoincrement=True, default=0),
        Column('name', String(255), nullable=False),
        Column('content', String(10000), nullable=False),
        Column('author', Integer, ForeignKey('users.id'), nullable=False)
    )


def downgrade():
    op.drop_table("blog_posts")
