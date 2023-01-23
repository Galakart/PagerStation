"""send after

Revision ID: b9638b078aa7
Revises: 0f4846e4b211
Create Date: 2023-01-23 20:21:47.196019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9638b078aa7'
down_revision = '0f4846e4b211'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('messages_private', sa.Column('datetime_send_after', sa.DateTime(), nullable=True, comment='Отправить после указанной даты-времени'))


def downgrade() -> None:
    op.drop_column('messages_private', 'datetime_send_after')
