"""mapped_column

Revision ID: edf088be4b6c
Revises: b974a5eb269d
Create Date: 2023-09-23 20:53:29.339189

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'edf088be4b6c'
down_revision: Union[str, None] = 'b974a5eb269d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('user_pagers', schema=None) as batch_op:
        batch_op.alter_column('uid_user',
                              existing_type=sa.CHAR(length=32),
                              nullable=False)
        batch_op.alter_column('id_pager',
                              existing_type=sa.INTEGER(),
                              nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('user_pagers', schema=None) as batch_op:
        batch_op.alter_column('id_pager',
                              existing_type=sa.INTEGER(),
                              nullable=True)
        batch_op.alter_column('uid_user',
                              existing_type=sa.CHAR(length=32),
                              nullable=True)
