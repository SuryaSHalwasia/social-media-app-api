"""Add columns to posts table

Revision ID: fac3564d69d9
Revises: 71d858d763a7
Create Date: 2023-09-17 17:14:06.294338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fac3564d69d9'
down_revision: Union[str, None] = '71d858d763a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published", sa.Boolean(), server_default='TRUE', nullable=False),)
    op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('NOW()'),))


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
