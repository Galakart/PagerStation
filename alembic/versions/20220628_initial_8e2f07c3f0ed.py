"""initial

Revision ID: 8e2f07c3f0ed
Revises: 
Create Date: 2022-06-28 20:30:01.201368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e2f07c3f0ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
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

    op.create_table('n_role',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=25), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Список доступных дополнительных ролей пользователй'
                    )

    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('fio', sa.String(length=200), nullable=False),
                    sa.Column('datar', sa.Date(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Пользователи пейджеров'
                    )

    op.create_table('service_roles',
                    sa.Column('id_user', sa.Integer(), nullable=False),
                    sa.Column('id_role', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['id_role'], ['n_role.id'], ),
                    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id_user', 'id_role'),
                    comment='Дополнительные роли пользователей'
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
    op.execute('INSERT INTO n_baudrates VALUES (2, "1024")')
    op.execute('INSERT INTO n_baudrates VALUES (3, "2048")')

    op.execute('INSERT INTO n_codepages VALUES (1, "lat")')
    op.execute('INSERT INTO n_codepages VALUES (2, "cyr")')
    op.execute('INSERT INTO n_codepages VALUES (3, "linguist")')

    op.execute('INSERT INTO n_fbits VALUES (0, "0")')
    op.execute('INSERT INTO n_fbits VALUES (1, "1")')
    op.execute('INSERT INTO n_fbits VALUES (2, "2")')
    op.execute('INSERT INTO n_fbits VALUES (3, "3")')

    op.execute('INSERT INTO n_role VALUES (10, "Админ")')


def downgrade():
    op.drop_table('user_pagers')
    op.drop_table('messages_private')
    op.drop_table('pagers')
    op.drop_table('transmitters')
    op.drop_table('service_roles')
    op.drop_table('users')
    op.drop_table('n_role')
    op.drop_table('n_fbits')
    op.drop_table('n_codepages')
    op.drop_table('n_baudrates')
