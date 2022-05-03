"""initial

Revision ID: e95d0310ddcd
Revises: 
Create Date: 2022-05-03 20:02:05.974626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e95d0310ddcd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('n_baudrates',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=4), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.execute('INSERT INTO n_baudrates VALUES (1, "512")')
    op.execute('INSERT INTO n_baudrates VALUES (2, "1024")')
    op.execute('INSERT INTO n_baudrates VALUES (3, "2048")')

    op.create_table('n_codepages',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.execute('INSERT INTO n_codepages VALUES (1, "lat")')
    op.execute('INSERT INTO n_codepages VALUES (2, "cyr")')
    op.execute('INSERT INTO n_codepages VALUES (3, "linguist")')

    op.create_table('n_fbits',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    op.execute('INSERT INTO n_fbits VALUES (0, "0")')
    op.execute('INSERT INTO n_fbits VALUES (1, "1")')
    op.execute('INSERT INTO n_fbits VALUES (2, "2")')
    op.execute('INSERT INTO n_fbits VALUES (3, "3")')

    op.create_table('transmitters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('freq', sa.Integer(), nullable=False),
    sa.Column('baudrate', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['baudrate'], ['n_baudrates.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('freq'),
    sa.UniqueConstraint('name')
    )


def downgrade():
    op.drop_table('transmitters')
    op.drop_table('n_fbits')
    op.drop_table('n_codepages')
    op.drop_table('n_baudrates')
