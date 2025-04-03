"""crear tabla pacientes

Revision ID: 1069693ee2b0
Revises: c8a8f0a6c74f
Create Date: 2024-10-29 13:07:10.793198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1069693ee2b0'
down_revision: Union[str, None] = 'c8a8f0a6c74f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('pacientes',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(128), nullable=False),
                    sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
                    sa.Column('edad', sa.SmallInteger(), nullable=False),
                    sa.Column('direccion_id', sa.Integer(), sa.ForeignKey('direcciones.id'), nullable=False),
                    sa.Column('numero_paciente', sa.Text(), nullable=False),
                    sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id')),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('pacientes')
