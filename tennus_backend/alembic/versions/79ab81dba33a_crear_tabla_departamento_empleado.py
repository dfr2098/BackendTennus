"""crear tabla departamento empleado

Revision ID: 79ab81dba33a
Revises: 1df6d68a9994
Create Date: 2024-10-23 13:29:59.756276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79ab81dba33a'
down_revision: Union[str, None] = '1df6d68a9994'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('departamento_empleado',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('empleado_id', sa.Integer(), sa.ForeignKey('empleados.id'), nullable=False),
                    sa.Column('departamento_id', sa.Integer(), sa.ForeignKey('departamentos.id'), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('updated_at', sa.TIMESTAMP(), onupdate=sa.func.now()),
                    sa.Column('deleted_at', sa.TIMESTAMP())
                    )


def downgrade() -> None:
    op.drop_table('departamento_empleado')
