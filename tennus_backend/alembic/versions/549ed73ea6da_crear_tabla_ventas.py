"""crear tabla ventas

Revision ID: 549ed73ea6da
Revises: e126a1cad0bf
Create Date: 2024-10-30 16:37:33.503682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '549ed73ea6da'
down_revision: Union[str, None] = 'e126a1cad0bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ventas',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('costo', sa.Float(), nullable=False),
                    sa.Column('fecha', sa.DATETIME(), nullable=False),
                    sa.Column('cita_id', sa.Integer(), sa.ForeignKey('citas.id'), nullable=False),
                    sa.Column('empleado_id', sa.Integer(), sa.ForeignKey('empleados.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('ventas')
