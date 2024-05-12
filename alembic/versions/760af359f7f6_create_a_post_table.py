"""create a post table

Revision ID: 760af359f7f6
Revises: 
Create Date: 2024-05-01 23:37:55.566887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '760af359f7f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id",sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable = False))

 
def downgrade() -> None:
    op.drop_table("posts")
 