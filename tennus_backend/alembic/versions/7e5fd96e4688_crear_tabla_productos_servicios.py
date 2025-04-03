"""crear tabla  productos_servicios

Revision ID: 7e5fd96e4688
Revises: 1e9dc40dd3ff
Create Date: 2024-10-28 12:06:35.628073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e5fd96e4688'
down_revision: Union[str, None] = '1e9dc40dd3ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('productos_servicios',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(128), nullable=False),
                    sa.Column('descripcion', sa.String(200), nullable=False),
                    sa.Column('tipo_muestra', sa.String(200), nullable=False),
                    sa.Column('precio_compra', sa.Float(), nullable=False),
                    sa.Column('precio_venta', sa.Float(), nullable=False),
                    sa.Column('tiempo_entrega', sa.Integer(), nullable=False),
                    sa.Column('codigo', sa.String(128)),
                    sa.Column('volumen', sa.String(128)),
                    sa.Column('presentacion', sa.String(200)),
                    sa.Column('conservacion', sa.String(120)),
                    sa.Column('contenido', sa.String(200)),
                    sa.Column('utilidad', sa.String(128)),
                    sa.Column('categoria_id', sa.Integer(), sa.ForeignKey('categorias.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('productos_servicios')
