"""Create posts table

Revision ID: 6fd547b9eb78
Revises: 
Create Date: 2023-09-17 10:17:29.658040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fd547b9eb78'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title',sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_table('posts')
