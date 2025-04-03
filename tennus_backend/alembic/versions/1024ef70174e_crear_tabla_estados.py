"""crear tabla estados

Revision ID: 1024ef70174e
Revises: 4e7aa983ba40
Create Date: 2024-10-23 10:34:50.038840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1024ef70174e'
down_revision: Union[str, None] = '4e7aa983ba40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('estados',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(128), nullable=False)
                    )

def downgrade() -> None:
    op.drop_table('estados')
