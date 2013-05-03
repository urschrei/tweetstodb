"""Add Tweet ID field

Revision ID: 2d95d28e5ea7
Revises: 3bf8c0d3d74c
Create Date: 2013-04-23 14:59:04.570162

"""

# revision identifiers, used by Alembic.
revision = '2d95d28e5ea7'
down_revision = '3bf8c0d3d74c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "tweets",
        sa.Column("tweet_id", sa.String(20), nullable=False, unique=True))


def downgrade():
    op.remove_column(
        "tweets",
        "tweet_id")
