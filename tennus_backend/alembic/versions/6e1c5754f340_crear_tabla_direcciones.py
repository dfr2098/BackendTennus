"""crear tabla direcciones

Revision ID: 6e1c5754f340
Revises: 298101286e7c
Create Date: 2024-10-23 12:33:06.635186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e1c5754f340'
down_revision: Union[str, None] = '298101286e7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('direcciones',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('calle', sa.String(250), nullable=False),
                    sa.Column('num_extrerior', sa.String(128), nullable=False),
                    sa.Column('num_interior', sa.String(128)),
                    sa.Column('colonia_id', sa.Integer(), sa.ForeignKey('colonias.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('direcciones')
