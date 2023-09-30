"""maildrop types

Revision ID: 39b873b95ba7
Revises: edf088be4b6c
Create Date: 2023-09-30 11:55:37.802014

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '39b873b95ba7'
down_revision: Union[str, None] = 'edf088be4b6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('INSERT INTO n_maildrop_types VALUES (5, "Настраиваемое 5")')
    op.execute('INSERT INTO n_maildrop_types VALUES (6, "Настраиваемое 6")')
    op.execute('INSERT INTO n_maildrop_types VALUES (7, "Настраиваемое 7")')
    op.execute('INSERT INTO n_maildrop_types VALUES (8, "Настраиваемое 8")')
    op.execute('INSERT INTO n_maildrop_types VALUES (9, "Настраиваемое 9")')
    op.execute('INSERT INTO n_maildrop_types VALUES (10, "Настраиваемое 10")')
    op.execute('INSERT INTO n_maildrop_types VALUES (11, "Настраиваемое 11")')
    op.execute('INSERT INTO n_maildrop_types VALUES (12, "Настраиваемое 12")')
    op.execute('INSERT INTO n_maildrop_types VALUES (13, "Настраиваемое 13")')
    op.execute('INSERT INTO n_maildrop_types VALUES (14, "Настраиваемое 14")')
    op.execute('INSERT INTO n_maildrop_types VALUES (15, "Настраиваемое 15")')
    op.execute('INSERT INTO n_maildrop_types VALUES (16, "Настраиваемое 16")')


def downgrade() -> None:
    op.execute('DELETE FROM messages WHERE id_maildrop_type BETWEEN 5 AND 16')
    op.execute('DELETE FROM n_maildrop_types WHERE id BETWEEN 5 AND 16')
