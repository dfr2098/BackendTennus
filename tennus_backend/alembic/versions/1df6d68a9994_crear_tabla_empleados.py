"""crear tabla empleados

Revision ID: 1df6d68a9994
Revises: a3e868311742
Create Date: 2024-10-23 13:19:30.709711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1df6d68a9994'
down_revision: Union[str, None] = 'a3e868311742'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('empleados',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre_completo', sa.String(228), nullable=False),
                    sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
                    sa.Column('telefono', sa.String(30), nullable=False),
                    sa.Column('correo', sa.String(200)),
                    sa.Column('sucursal_id', sa.Integer(), sa.ForeignKey('sucursales.id'), nullable=False),
                    sa.Column('direccion_id', sa.Integer(), sa.ForeignKey('direcciones.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('empleados')
