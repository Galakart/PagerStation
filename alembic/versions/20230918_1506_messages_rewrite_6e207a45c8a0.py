"""messages rewrite

Revision ID: 6e207a45c8a0
Revises: 208c80e9d793
Create Date: 2023-09-18 15:06:16.025487

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6e207a45c8a0'
down_revision: Union[str, None] = '208c80e9d793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('n_group_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы групповых сообщений'
                    )
    op.create_table('n_message_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы сообщений'
                    )
    op.create_table('channels_group',
                    sa.Column('id_transmitter', sa.Integer(), nullable=False),
                    sa.Column('capcode', sa.Integer(), nullable=False),
                    sa.Column('id_fbit', sa.Integer(), nullable=False),
                    sa.Column('id_group_type', sa.Integer(), nullable=False),
                    sa.Column('id_codepage', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id_codepage'], ['n_codepages.id'], ),
                    sa.ForeignKeyConstraint(['id_fbit'], ['n_fbits.id'], ),
                    sa.ForeignKeyConstraint(['id_group_type'], ['n_group_types.id'], ),
                    sa.ForeignKeyConstraint(['id_transmitter'], ['transmitters.id'], ),
                    sa.PrimaryKeyConstraint('id_transmitter', 'capcode', 'id_fbit'),
                    comment='Групповые каналы трансмиттера'
                    )
    op.create_table('channels_maildrop',
                    sa.Column('id_transmitter', sa.Integer(), nullable=False),
                    sa.Column('capcode', sa.Integer(), nullable=False),
                    sa.Column('id_fbit', sa.Integer(), nullable=False),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=False),
                    sa.Column('id_codepage', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id_codepage'], ['n_codepages.id'], ),
                    sa.ForeignKeyConstraint(['id_fbit'], ['n_fbits.id'], ),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.ForeignKeyConstraint(['id_transmitter'], ['transmitters.id'], ),
                    sa.PrimaryKeyConstraint('id_transmitter', 'capcode', 'id_fbit'),
                    comment='Новостные каналы трансмиттера, и их капкоды'
                    )
    op.create_table('messages',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('id_message_type', sa.Integer(), nullable=False),
                    sa.Column('id_pager', sa.Integer(), nullable=True,
                              comment='указывается если сообщение личное (id_message_type=1)'
                              ),
                    sa.Column('id_group_type', sa.Integer(), nullable=True,
                              comment='указывается если сообщение групповое (id_message_type=2)'
                              ),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=True,
                              comment='указывается если сообщение новостное (id_message_type=3)'
                              ),
                    sa.Column('message', sa.String(length=950), nullable=False),
                    sa.Column('sent', sa.Boolean(), nullable=False),
                    sa.Column('datetime_send_after', sa.DateTime(), nullable=True,
                              comment='Отправить после указанной даты-времени'
                              ),
                    sa.Column('date_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_group_type'], ['n_group_types.id'], ),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.ForeignKeyConstraint(['id_message_type'], ['n_message_types.id'], ),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Сообщения'
                    )
    op.drop_table('maildrop_channels')
    op.drop_table('messages_private')
    op.drop_table('messages_maildrop')

    op.execute('INSERT INTO n_message_types VALUES (1, "Личное")')
    op.execute('INSERT INTO n_message_types VALUES (2, "Групповое")')
    op.execute('INSERT INTO n_message_types VALUES (3, "Новостное")')

    op.execute('INSERT INTO n_group_types VALUES (1, "Обычное")')
    op.execute('INSERT INTO n_group_types VALUES (2, "Экстренное")')


def downgrade() -> None:
    op.create_table('messages_maildrop',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('id_maildrop_type', sa.INTEGER(), nullable=False),
                    sa.Column('message', sa.VARCHAR(length=950), nullable=False),
                    sa.Column('sent', sa.BOOLEAN(), nullable=False),
                    sa.Column('date_create', sa.DATETIME(), nullable=False),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('messages_private',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('id_pager', sa.INTEGER(), nullable=False),
                    sa.Column('message', sa.VARCHAR(length=950), nullable=False),
                    sa.Column('sent', sa.BOOLEAN(), nullable=False),
                    sa.Column('datetime_send_after', sa.DATETIME(), nullable=True),
                    sa.Column('date_create', sa.DATETIME(), nullable=False),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('maildrop_channels',
                    sa.Column('id_transmitter', sa.INTEGER(), nullable=False),
                    sa.Column('capcode', sa.INTEGER(), nullable=False),
                    sa.Column('id_fbit', sa.INTEGER(), nullable=False),
                    sa.Column('id_maildrop_type', sa.INTEGER(), nullable=False),
                    sa.Column('id_codepage', sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['id_codepage'], ['n_codepages.id'], ),
                    sa.ForeignKeyConstraint(['id_fbit'], ['n_fbits.id'], ),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.ForeignKeyConstraint(['id_transmitter'], ['transmitters.id'], ),
                    sa.PrimaryKeyConstraint('id_transmitter', 'capcode', 'id_fbit')
                    )
    op.drop_table('messages')
    op.drop_table('channels_maildrop')
    op.drop_table('channels_group')
    op.drop_table('n_message_types')
    op.drop_table('n_group_types')
