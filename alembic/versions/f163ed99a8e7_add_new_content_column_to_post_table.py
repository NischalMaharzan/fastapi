"""add new CONTENT column to post table

Revision ID: f163ed99a8e7
Revises: 760af359f7f6
Create Date: 2024-05-01 23:52:44.513742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f163ed99a8e7'
down_revision: Union[str, None] = '760af359f7f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("author", sa.String(), nullable = False))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("now()")))

def downgrade() -> None:
    op.drop_column("posts", "content")
    op.drop_column("posts", "created_at")
    # pass