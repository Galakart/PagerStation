"""rss id int

Revision ID: 4394e36b4330
Revises: 39b873b95ba7
Create Date: 2023-10-02 20:02:39.808745

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4394e36b4330'
down_revision: Union[str, None] = '39b873b95ba7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('rss_feeds')

    op.create_table('rss_feeds',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('id_maildrop_type', sa.Integer(), nullable=False),
                    sa.Column('feed_link', sa.Text(), nullable=False),
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['id_maildrop_type'], ['n_maildrop_types.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id_maildrop_type'),
                    comment='RSS-ленты'
                    )

    op.execute('INSERT INTO rss_feeds (id_maildrop_type, feed_link, datetime_create) VALUES \
               (4, "https://habr.com/ru/rss/news/?fl=ru", CURRENT_TIMESTAMP)')


def downgrade() -> None:
    pass
