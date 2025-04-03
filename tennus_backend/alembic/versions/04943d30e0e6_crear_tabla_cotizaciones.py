"""crear tabla cotizaciones

Revision ID: 04943d30e0e6
Revises: 7e5fd96e4688
Create Date: 2024-10-28 15:31:01.506524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04943d30e0e6'
down_revision: Union[str, None] = '7e5fd96e4688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cotizaciones',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('costo', sa.Float(), nullable=False),
                    sa.Column('fecha_elaboracion', sa.Date(), nullable=False),
                    sa.Column('tratamiento', sa.Text()),
                    sa.Column('empleado_id',sa.Integer(), sa.ForeignKey('empleados.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('cotizaciones')
