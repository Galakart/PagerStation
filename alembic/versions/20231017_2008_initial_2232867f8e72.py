"""initial

Revision ID: 2232867f8e72
Revises: 
Create Date: 2023-10-17 20:08:46.655958

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2232867f8e72'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('n_baudrates',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=4), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('n_codepages',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=8), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('n_fbits',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=1), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('n_group_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('n_maildrop_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('n_message_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('stricts_ipaddresses',
                    sa.Column('ip_address', sa.String(length=16), nullable=False),
                    sa.Column('last_send', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('ip_address')
                    )
    op.create_table('users',
                    sa.Column('uid', sa.Uuid(), nullable=False),
                    sa.Column('fio', sa.String(length=200), nullable=False),
                    sa.Column('datar', sa.Date(), nullable=True),
                    sa.PrimaryKeyConstraint('uid')
                    )
    op.create_table('rss_feeds',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=False),
                    sa.Column('feed_link', sa.Text(), nullable=False),
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id_maildrop_type')
                    )
    op.create_table('transmitters',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('freq', sa.Integer(), nullable=False),
                    sa.Column('id_baudrate', sa.Integer(), nullable=False),
                    sa.Column('external', sa.Boolean(), nullable=False),
                    sa.Column('external_command', sa.String(length=512), nullable=True),
                    sa.ForeignKeyConstraint(['id_baudrate'], ['n_baudrates.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('freq'),
                    sa.UniqueConstraint('name')
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
                    sa.PrimaryKeyConstraint('id_transmitter', 'capcode', 'id_fbit')
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
                    sa.PrimaryKeyConstraint('id_transmitter', 'capcode', 'id_fbit')
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
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('messages',
                    sa.Column('uid', sa.Uuid(), nullable=False),
                    sa.Column('id_message_type', sa.Integer(), nullable=False),
                    sa.Column('id_pager', sa.Integer(), nullable=True),
                    sa.Column('id_group_type', sa.Integer(), nullable=True),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=True),
                    sa.Column('message', sa.String(length=900), nullable=False),
                    sa.Column('sent', sa.Boolean(), nullable=False),
                    sa.Column('datetime_send_after', sa.DateTime(), nullable=True),
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_group_type'], ['n_group_types.id'], ),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.ForeignKeyConstraint(['id_message_type'], ['n_message_types.id'], ),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.PrimaryKeyConstraint('uid')
                    )
    op.create_table('user_pagers',
                    sa.Column('uid_user', sa.Uuid(), nullable=False),
                    sa.Column('id_pager', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id_pager'], ['pagers.id'], ),
                    sa.ForeignKeyConstraint(['uid_user'], ['users.uid'], ),
                    sa.PrimaryKeyConstraint('uid_user', 'id_pager')
                    )

    op.execute('INSERT INTO n_baudrates VALUES (512, "baud_512")')
    op.execute('INSERT INTO n_baudrates VALUES (1200, "baud_1200")')
    op.execute('INSERT INTO n_baudrates VALUES (2400, "baud_2400")')

    op.execute('INSERT INTO n_fbits VALUES (1, "bit_1")')
    op.execute('INSERT INTO n_fbits VALUES (2, "bit_2")')
    op.execute('INSERT INTO n_fbits VALUES (3, "bit_3")')
    op.execute('INSERT INTO n_fbits VALUES (4, "bit_4")')

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

    op.execute('INSERT INTO rss_feeds (id_maildrop_type, feed_link, datetime_create) VALUES (4, "https://habr.com/ru/rss/news/?fl=ru", CURRENT_TIMESTAMP)')


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
