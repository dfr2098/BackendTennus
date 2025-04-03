"""crear tabla departamentos

Revision ID: a3e868311742
Revises: a05c66abb753
Create Date: 2024-10-23 13:08:00.632288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3e868311742'
down_revision: Union[str, None] = 'a05c66abb753'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('departamentos',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(128), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('departamentos')
