"""crear tabla contactos

Revision ID: c8a8f0a6c74f
Revises: ee736cc45909
Create Date: 2024-10-29 12:25:59.266287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8a8f0a6c74f'
down_revision: Union[str, None] = 'ee736cc45909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contactos',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('nombre', sa.String(128), nullable=False),
                    sa.Column('apellidos', sa.String(255), nullable=False),
                    sa.Column('telefono', sa.String(15), nullable=False),
                    sa.Column('correo', sa.String(128), nullable=False),
                    sa.Column('comentario', sa.Text(), nullable=False),
                    sa.Column('receta_url', sa.Text()),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('contactos')
