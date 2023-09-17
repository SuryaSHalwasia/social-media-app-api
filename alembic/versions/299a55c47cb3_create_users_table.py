"""Create users table

Revision ID: 299a55c47cb3
Revises: 373780f6ebaf
Create Date: 2023-09-17 16:54:27.305069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '299a55c47cb3'
down_revision: Union[str, None] = '373780f6ebaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column("email",sa.String(), nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                              sa.PrimaryKeyConstraint("id"),
                              sa.UniqueConstraint("email"))


def downgrade() -> None:
    op.drop_table("users")
