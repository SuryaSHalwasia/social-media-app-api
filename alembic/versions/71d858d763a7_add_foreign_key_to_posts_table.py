"""Add foreign-key to posts table

Revision ID: 71d858d763a7
Revises: 299a55c47cb3
Create Date: 2023-09-17 17:05:01.461318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71d858d763a7'
down_revision: Union[str, None] = '299a55c47cb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("user_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk","posts","users",['user_id'],['id'],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk","posts")
    op.drop_column("posts","user_id")