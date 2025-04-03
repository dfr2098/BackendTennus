"""cambiar campo fecha citas

Revision ID: 4534deaf8730
Revises: eb83eec1ad07
Create Date: 2024-12-16 13:10:41.323543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4534deaf8730'
down_revision: Union[str, None] = 'eb83eec1ad07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('citas', 'fecha', type_=sa.DATETIME(), existing_nullable=False)


def downgrade() -> None:
    op.alter_column('citas', 'fecha', type_=sa.Date(), existing_nullable=False)
