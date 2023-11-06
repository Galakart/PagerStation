"""auth

Revision ID: 5ae91184982d
Revises: 2232867f8e72
Create Date: 2023-11-06 11:11:12.953471

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5ae91184982d'
down_revision: Union[str, None] = '2232867f8e72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('api_login', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('api_password', sa.String(length=200), nullable=True))
        batch_op.create_unique_constraint('uniq_users_login', ['api_login'])


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uniq_users_login', type_='unique')
        batch_op.drop_column('api_password')
        batch_op.drop_column('api_login')
