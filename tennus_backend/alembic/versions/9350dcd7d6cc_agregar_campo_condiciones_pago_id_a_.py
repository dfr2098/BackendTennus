"""agregar campo condiciones pago id  a tabla cotizaciones

Revision ID: 9350dcd7d6cc
Revises: ba7185eb2702
Create Date: 2024-10-30 15:16:37.622741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9350dcd7d6cc'
down_revision: Union[str, None] = 'ba7185eb2702'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('cotizaciones',
                  sa.Column('condiciones_pago_id', sa.Integer(), sa.ForeignKey('condiciones_pagos.id'), nullable=False)
                  )


def downgrade() -> None:
    op.drop_constraint('cotizaciones_ibfk_4', 'cotizaciones', type_='foreignkey')
    op.drop_column('cotizaciones', 'condiciones_pago_id')
