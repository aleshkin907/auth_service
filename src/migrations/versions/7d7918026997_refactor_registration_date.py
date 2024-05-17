"""Refactor registration date

Revision ID: 7d7918026997
Revises: e9f7b142fadb
Create Date: 2024-05-12 23:56:24.970475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d7918026997'
down_revision: Union[str, None] = 'e9f7b142fadb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'registration_date', server_default=sa.func.now())

def downgrade() -> None:
    op.alter_column('users', 'registration_date', server_default=None)
    