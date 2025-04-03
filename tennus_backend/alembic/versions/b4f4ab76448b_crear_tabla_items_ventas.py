"""crear tabla items ventas

Revision ID: b4f4ab76448b
Revises: 549ed73ea6da
Create Date: 2024-10-30 16:55:14.722168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4f4ab76448b'
down_revision: Union[str, None] = '549ed73ea6da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('items_ventas',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('costo', sa.Float(), nullable=False),
                    sa.Column('cantidad', sa.Float(), nullable=False),
                    sa.Column('venta_id', sa.Integer(), sa.ForeignKey('ventas.id'), nullable=False),
                    sa.Column('producto_servicio_id', sa.Integer(), sa.ForeignKey('productos_servicios.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('items_ventas')
