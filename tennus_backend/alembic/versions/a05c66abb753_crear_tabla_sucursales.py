"""crear tabla sucursales

Revision ID: a05c66abb753
Revises: 6e1c5754f340
Create Date: 2024-10-23 12:59:45.854466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a05c66abb753'
down_revision: Union[str, None] = '6e1c5754f340'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('sucursales',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(128), nullable=False),
                    sa.Column('telefono', sa.String(30)),
                    sa.Column('direccion_id', sa.Integer(), sa.ForeignKey('direcciones.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('sucursales')
