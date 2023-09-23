"""initial uuid ids

Revision ID: b974a5eb269d
Revises: 
Create Date: 2023-09-23 10:22:39.340265

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b974a5eb269d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('n_baudrates',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=4), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Скорости передачи данных'
                    )
    op.create_table('n_codepages',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=8), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Кодировки текста'
                    )
    op.create_table('n_fbits',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=1), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Источники (функциональные биты)'
                    )
    op.create_table('n_group_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы групповых сообщений'
                    )
    op.create_table('n_maildrop_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы новостных рассылок'
                    )
    op.create_table('n_message_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы сообщений'
                    )
    op.create_table('stricts_ipaddresses',
                    sa.Column('ip_address', sa.String(length=16), nullable=False),
                    sa.Column('last_send', sa.DateTime(), nullable=False, comment='Дата-время последней отправки'),
                    sa.PrimaryKeyConstraint('ip_address'),
                    comment='IP адреса для ограничений на количество сообщений за период'
                    )
    op.create_table('users',
                    sa.Column('uid', sa.Uuid(), nullable=False),
                    sa.Column('fio', sa.String(length=200), nullable=False),
                    sa.Column('datar', sa.Date(), nullable=True),
                    sa.PrimaryKeyConstraint('uid'),
                    comment='Пользователи пейджеров'
                    )
    op.create_table('rss_feeds',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=False),
                    sa.Column('feed_link', sa.Text(), nullable=False),
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id_maildrop_type'),
                    comment='RSS-ленты'
                    )
    op.create_table('transmitters',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('freq', sa.Integer(), nullable=False),
                    sa.Column('id_baudrate', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id_baudrate'], ['n_baudrates.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('freq'),
                    sa.UniqueConstraint('name'),
                    comment='Передатчики'
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
                    comment='Новостные каналы трансмиттера'
                    )
    op.create_table('pagers',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('capcode', sa.Integer(), nullable=False),
                    sa.Column('id_fbit', sa.Integer(), nullable=False),
                    sa.Column('id_codepage', sa.Integer(), nullable=False),
                    sa.Column('id_transmitter', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id_codepage'], ['n_codepages.id'], ),
                    sa.ForeignKeyConstraint(['id_fbit'], ['n_fbits.id'], ),
                    sa.ForeignKeyConstraint(['id_transmitter'], ['transmitters.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Пейджеры'
                    )
    op.create_table('messages',
                    sa.Column('uid', sa.Uuid(), nullable=False),
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
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_group_type'], ['n_group_types.id'], ),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.ForeignKeyConstraint(['id_message_type'], ['n_message_types.id'], ),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.PrimaryKeyConstraint('uid'),
                    comment='Сообщения'
                    )
    op.create_table('user_pagers',
                    sa.Column('uid_user', sa.Uuid(), nullable=True),
                    sa.Column('id_pager', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.ForeignKeyConstraint(['uid_user'], ['users.uid'], )
                    )

    op.execute('INSERT INTO n_baudrates VALUES (1, "512")')
    op.execute('INSERT INTO n_baudrates VALUES (2, "1200")')
    op.execute('INSERT INTO n_baudrates VALUES (3, "2400")')

    op.execute('INSERT INTO n_fbits VALUES (0, "0")')
    op.execute('INSERT INTO n_fbits VALUES (1, "1")')
    op.execute('INSERT INTO n_fbits VALUES (2, "2")')
    op.execute('INSERT INTO n_fbits VALUES (3, "3")')

    op.execute('INSERT INTO n_codepages VALUES (1, "lat")')
    op.execute('INSERT INTO n_codepages VALUES (2, "cyr")')
    op.execute('INSERT INTO n_codepages VALUES (3, "linguist")')

    op.execute('INSERT INTO n_message_types VALUES (1, "Личное")')
    op.execute('INSERT INTO n_message_types VALUES (2, "Групповое")')
    op.execute('INSERT INTO n_message_types VALUES (3, "Новостное")')

    op.execute('INSERT INTO n_group_types VALUES (1, "Обычное")')
    op.execute('INSERT INTO n_group_types VALUES (2, "Экстренное")')

    op.execute('INSERT INTO n_maildrop_types VALUES (1, "Уведомления")')
    op.execute('INSERT INTO n_maildrop_types VALUES (2, "Погода")')
    op.execute('INSERT INTO n_maildrop_types VALUES (3, "Курс валют")')
    op.execute('INSERT INTO n_maildrop_types VALUES (4, "Новости")')


def downgrade() -> None:
    op.drop_table('user_pagers')
    op.drop_table('messages')
    op.drop_table('pagers')
    op.drop_table('channels_maildrop')
    op.drop_table('channels_group')
    op.drop_table('transmitters')
    op.drop_table('rss_feeds')
    op.drop_table('users')
    op.drop_table('stricts_ipaddresses')
    op.drop_table('n_message_types')
    op.drop_table('n_maildrop_types')
    op.drop_table('n_group_types')
    op.drop_table('n_fbits')
    op.drop_table('n_codepages')
    op.drop_table('n_baudrates')
