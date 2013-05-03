"""Add partial index for geocoded tweets

Revision ID: 53d21b8f9a8c
Revises: 2d95d28e5ea7
Create Date: 2013-04-24 15:01:25.786430

"""

# revision identifiers, used by Alembic.
revision = '53d21b8f9a8c'
down_revision = '2d95d28e5ea7'

from alembic import op
from sqlalchemy.sql import text


def upgrade():
    op.create_index(
        'geocoded',
        'tweets',
        ['coordinates'],
        postgresql_where=text("tweets.coordinates != Null"))


def downgrade():
    op.drop_index("geocoded")
