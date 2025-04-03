"""crear tabla citas

Revision ID: a6849d9173bb
Revises: 9350dcd7d6cc
Create Date: 2024-10-30 15:22:08.042741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6849d9173bb'
down_revision: Union[str, None] = '9350dcd7d6cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('citas',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('fecha', sa.Date(), nullable=False),
                    sa.Column('fecha_confirmacion', sa.DATETIME(), nullable=False),
                    sa.Column('paciente_id', sa.Integer(), sa.ForeignKey('pacientes.id'), nullable=False),
                    sa.Column('cotizacion_id', sa.Integer(), sa.ForeignKey('cotizaciones.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('citas')
