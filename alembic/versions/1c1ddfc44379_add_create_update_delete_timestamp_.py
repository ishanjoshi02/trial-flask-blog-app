"""add create update delete timestamp  column to blog table

Revision ID: 1c1ddfc44379
Revises: 1391c999868e
Create Date: 2019-07-11 16:45:50.920830

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '1c1ddfc44379'
down_revision = '1391c999868e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('blog_posts', Column(
        'created_on', TIMESTAMP, server_default=func.now()))
    op.add_column("blog_posts", Column(
        'edited_on', TIMESTAMP, nullable=True, onupdate=func.now()
    ))
    op.add_column("blog_posts", Column(
        'deleted_on', TIMESTAMP, nullable=True
    ))


def downgrade():
    op.drop_column('blog_posts', 'created_on')
    op.drop_column("blog_posts", "edited_on")
    op.drop_column("blog_posts", "deleted_on")
