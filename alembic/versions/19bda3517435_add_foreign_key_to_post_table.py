"""add foreign key to post table

Revision ID: 19bda3517435
Revises: c91b79197841
Create Date: 2024-05-02 00:16:08.404613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19bda3517435'
down_revision: Union[str, None] = 'c91b79197841'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("is_published",sa.Boolean(True), nullable=False))
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),sa.ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "owner_id")
    op.drop_column("posts","is_published")
    # pass

