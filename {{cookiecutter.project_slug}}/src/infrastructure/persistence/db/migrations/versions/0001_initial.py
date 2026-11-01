"""initial: example item table

Revision ID: 0001_initial
Revises:
Create Date: 2026-11-01

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS {{ cookiecutter.db_schema }}')
    op.create_table(
        't_item',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=256), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='{{ cookiecutter.db_schema }}',
    )


def downgrade() -> None:
    op.drop_table('t_item', schema='{{ cookiecutter.db_schema }}')
