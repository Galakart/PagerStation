"""mes length

Revision ID: f58e597a4dec
Revises: 4394e36b4330
Create Date: 2023-10-09 13:30:39.999488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f58e597a4dec'
down_revision: Union[str, None] = '4394e36b4330'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('DELETE FROM messages WHERE length(message) > 900')

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.alter_column('message',
               existing_type=sa.VARCHAR(length=950),
               type_=sa.String(length=900),
               existing_nullable=False)



def downgrade() -> None:
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.alter_column('message',
               existing_type=sa.String(length=900),
               type_=sa.VARCHAR(length=950),
               existing_nullable=False)

