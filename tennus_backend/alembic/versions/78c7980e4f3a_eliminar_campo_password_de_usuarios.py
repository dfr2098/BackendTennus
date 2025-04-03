"""eliminar campo password de usuarios

Revision ID: 78c7980e4f3a
Revises: ba1d9b54dfd4
Create Date: 2025-01-31 12:24:11.739715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78c7980e4f3a'
down_revision: Union[str, None] = 'ba1d9b54dfd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('usuarios', 'password')


def downgrade() -> None:
    pass
