"""Refactor token name

Revision ID: a49e5363747d
Revises: 1d806addd633
Create Date: 2024-05-23 21:26:30.847225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a49e5363747d'
down_revision: Union[str, None] = '1d806addd633'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('id', sa.Uuid(), nullable=False))
    op.drop_column('tokens', 'jti')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('jti', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_column('tokens', 'id')
    # ### end Alembic commands ###
