"""Initial table creation

Revision ID: 3bf8c0d3d74c
Revises: None
Create Date: 2013-04-19 17:19:19.911280

"""

# revision identifiers, used by Alembic.
revision = '3bf8c0d3d74c'
down_revision = None

from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"



def upgrade():
    tweets = op.create_table(
        "tweets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=utcnow()),
        sa.Column("username", sa.String(50), nullable=False, unique=False),
        sa.Column("content", sa.String(200), nullable=False, unique=False),
        sa.Column("coordinates", sa.String(50), nullable=True)
    )
    op.create_index("ix_username", "tweets", ["username"])
    op.create_index("ix_content", "tweets", ["content"])



def downgrade():
    op.drop_table("tweets")
