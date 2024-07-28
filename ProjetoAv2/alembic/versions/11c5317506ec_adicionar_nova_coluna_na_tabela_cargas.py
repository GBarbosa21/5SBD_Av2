"""Adicionar nova coluna na tabela 'cargas'

Revision ID: 11c5317506ec
Revises: d57bdbd64fd8
Create Date: 2024-07-08 15:59:16.595944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11c5317506ec'
down_revision: Union[str, None] = 'd57bdbd64fd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
