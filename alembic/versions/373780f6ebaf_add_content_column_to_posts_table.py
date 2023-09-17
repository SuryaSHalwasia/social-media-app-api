"""Add content column to posts table

Revision ID: 373780f6ebaf
Revises: 6fd547b9eb78
Create Date: 2023-09-17 16:45:57.091517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '373780f6ebaf'
down_revision: Union[str, None] = '6fd547b9eb78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts","content")
