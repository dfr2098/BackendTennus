"""agregar campo paciente id a tabla cotizaciones

Revision ID: 71fa35080fbc
Revises: 1069693ee2b0
Create Date: 2024-10-29 13:50:18.487554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71fa35080fbc'
down_revision: Union[str, None] = '1069693ee2b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('cotizaciones',
                  sa.Column('paciente_id', sa.Integer(), sa.ForeignKey('pacientes.id'), nullable=False)
                  )


def downgrade() -> None:
    op.drop_constraint('cotizaciones_ibfk_2','cotizaciones', type_='foreignkey')
    op.drop_column('cotizaciones','paciente_id')
