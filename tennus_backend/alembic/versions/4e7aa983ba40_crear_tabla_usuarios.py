"""crear tabla usuarios

Revision ID: 4e7aa983ba40
Revises: 
Create Date: 2024-10-22 21:33:24.238212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4e7aa983ba40'
down_revision: Union[str, None] = '3bbbb997b54e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('usuarios',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre_completo', sa.String(128), nullable=False),
                    sa.Column('correo', sa.String(128), nullable=False, unique=True),
                    sa.Column('password', sa.String(128), nullable=False),
                    sa.Column('hashed_password', sa.Text, nullable=False),
                    sa.Column('telefono', sa.String(32)),
                    sa.Column('rol_id', sa.Integer(),sa.ForeignKey('roles.id')),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('usuarios')
