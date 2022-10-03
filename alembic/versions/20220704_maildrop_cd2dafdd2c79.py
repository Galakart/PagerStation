"""maildrop

Revision ID: cd2dafdd2c79
Revises: 8e2f07c3f0ed
Create Date: 2022-07-04 20:44:18.115125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd2dafdd2c79'
down_revision = '8e2f07c3f0ed'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('n_maildrop_types',
                    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name'),
                    comment='Типы новостных рассылок'
                    )

    op.execute('INSERT INTO n_maildrop_types VALUES (1, "Уведомления")')
    op.execute('INSERT INTO n_maildrop_types VALUES (2, "Новости")')
    op.execute('INSERT INTO n_maildrop_types VALUES (3, "Погода")')
    op.execute('INSERT INTO n_maildrop_types VALUES (4, "Курс валют")')

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


def downgrade():
    op.drop_table('maildrop_channels')
    op.drop_table('messages_maildrop')
    op.drop_table('n_maildrop_types')
