"""rss maildrop

Revision ID: d141a0e990ff
Revises: cd2dafdd2c79
Create Date: 2023-01-14 21:59:47.656942

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'd141a0e990ff'
down_revision = 'cd2dafdd2c79'
branch_labels = None
depends_on = None


def upgrade() -> None:
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


def downgrade() -> None:
    op.drop_table('rss_feeds')
