"""add edit column to blog table

Revision ID: 1391c999868e
Revises: 910b80ae8e13
Create Date: 2019-07-11 16:39:22.745559

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Boolean, Column


# revision identifiers, used by Alembic.
revision = '1391c999868e'
down_revision = '910b80ae8e13'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('blog_posts', Column('edited', Boolean, default=False))


def downgrade():
    op.drop_column('blog_posts', 'edited')
