"""Descrição da migração

Revision ID: d57bdbd64fd8
Revises: 8e3c4ddf385a
Create Date: 2024-07-08 14:31:32.332383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd57bdbd64fd8'
down_revision: Union[str, None] = '8e3c4ddf385a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
