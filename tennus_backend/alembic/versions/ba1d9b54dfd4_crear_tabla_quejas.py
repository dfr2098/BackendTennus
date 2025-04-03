"""crear tabla quejas

Revision ID: ba1d9b54dfd4
Revises: 4534deaf8730
Create Date: 2024-12-30 21:03:51.309656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba1d9b54dfd4'
down_revision: Union[str, None] = '4534deaf8730'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('quejas',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(220)),
                    sa.Column('correo', sa.String(200), nullable=False),
                    sa.Column('observacion', sa.Text(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('quejas')
