"""initial

Revision ID: 208c80e9d793
Revises: 
Create Date: 2023-09-11 19:35:27.408138

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '208c80e9d793'
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
    op.create_table('n_maildrop_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы новостных рассылок'
                    )
    op.create_table('stricts_ipaddresses',
                    sa.Column('ip_address', sa.String(length=16), nullable=False),
                    sa.Column('last_send', sa.DateTime(), nullable=False, comment='Дата-время последней отправки'),
                    sa.PrimaryKeyConstraint('ip_address'),
                    comment='IP адреса для ограничений на количество сообщений за период'
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('fio', sa.String(length=200), nullable=False),
                    sa.Column('datar', sa.Date(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Пользователи пейджеров'
                    )
    op.create_table('messages_maildrop',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=False),
                    sa.Column('message', sa.String(length=950), nullable=False),
                    sa.Column('sent', sa.Boolean(), nullable=False),
                    sa.Column('date_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Сообщения - новостные'
                    )
    op.create_table('rss_feeds',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=False),
                    sa.Column('feed_link', sa.Text(), nullable=False),
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id_maildrop_type'),
                    comment='RSS-ленты. '
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
    op.create_table('maildrop_channels',
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
    op.create_table('pagers',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False, comment='Абонентский номер'),
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
    op.create_table('messages_private',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('id_pager', sa.Integer(), nullable=False),
                    sa.Column('message', sa.String(length=950), nullable=False),
                    sa.Column('sent', sa.Boolean(), nullable=False),
                    sa.Column('datetime_send_after', sa.DateTime(), nullable=True, comment='Отправить после указанной даты-времени'),
                    sa.Column('date_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Сообщения - личные'
                    )
    op.create_table('user_pagers',
                    sa.Column('id_user', sa.Integer(), nullable=True),
                    sa.Column('id_pager', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.ForeignKeyConstraint(['id_user'], ['users.id'], )
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

    op.execute('INSERT INTO n_maildrop_types VALUES (1, "Уведомления")')    
    op.execute('INSERT INTO n_maildrop_types VALUES (2, "Погода")')
    op.execute('INSERT INTO n_maildrop_types VALUES (3, "Курс валют")')
    op.execute('INSERT INTO n_maildrop_types VALUES (4, "Новости")')


def downgrade() -> None:
    op.drop_table('user_pagers')
    op.drop_table('messages_private')
    op.drop_table('pagers')
    op.drop_table('maildrop_channels')
    op.drop_table('transmitters')
    op.drop_table('rss_feeds')
    op.drop_table('messages_maildrop')
    op.drop_table('users')
    op.drop_table('stricts_ipaddresses')
    op.drop_table('n_maildrop_types')
    op.drop_table('n_fbits')
    op.drop_table('n_codepages')
    op.drop_table('n_baudrates')
