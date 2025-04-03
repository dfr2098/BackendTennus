"""agregar campo forma pago id a tabla cotizaciones

Revision ID: a9389e9f822e
Revises: 7e7e9235159e
Create Date: 2024-10-30 14:51:26.812744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9389e9f822e'
down_revision: Union[str, None] = '7e7e9235159e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('cotizaciones',
                  sa.Column('forma_pago_id', sa.Integer(), sa.ForeignKey('formas_pagos.id'), nullable=False)
                  )


def downgrade() -> None:
    op.drop_constraint('cotizaciones_ibfk_3', 'cotizaciones', type_='foreignkey')
    op.drop_column('cotizaciones', 'forma_pago_id')
