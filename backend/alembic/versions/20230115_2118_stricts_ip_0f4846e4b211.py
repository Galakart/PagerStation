"""stricts ip

Revision ID: 0f4846e4b211
Revises: d141a0e990ff
Create Date: 2023-01-15 21:18:32.078812

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0f4846e4b211'
down_revision = 'd141a0e990ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('stricts_ipaddresses',
                    sa.Column('ip_address', sa.String(length=16), nullable=False),
                    sa.Column('last_send', sa.DateTime(), nullable=False, comment='Дата-время последней прямой отправки'),
                    sa.PrimaryKeyConstraint('ip_address'),
                    comment='IP адреса для ограничений на количество прямых сообщений'
                    )


def downgrade() -> None:
    op.drop_table('stricts_ipaddresses')
