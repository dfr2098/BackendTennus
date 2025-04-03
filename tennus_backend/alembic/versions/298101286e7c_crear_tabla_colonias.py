"""crear tabla colonias

Revision ID: 298101286e7c
Revises: 1024ef70174e
Create Date: 2024-10-23 10:53:28.607008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '298101286e7c'
down_revision: Union[str, None] = '1024ef70174e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('colonias',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('codigo_postal', sa.String(10), nullable=False),
                    sa.Column('nombre', sa.String(255), nullable=False),
                    sa.Column('municipio', sa.String(255)),
                    sa.Column('ciudad', sa.String(255)),
                    sa.Column('estado_id',sa.Integer(), sa.ForeignKey('estados.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP()),
                    )



def downgrade() -> None:
    op.drop_table('colonias')
