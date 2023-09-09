"""remove roles

Revision ID: 1c849e54d818
Revises: b9638b078aa7
Create Date: 2023-02-26 19:45:22.534750

"""
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision = '1c849e54d818'
down_revision = 'b9638b078aa7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('service_roles')
    op.drop_index('name', table_name='n_role')
    op.drop_table('n_role')


def downgrade() -> None:
    op.create_table('n_role',
                    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
                    sa.Column('name', mysql.VARCHAR(length=25), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    comment='Список доступных дополнительных ролей пользователй',
                    mysql_collate='utf8mb4_general_ci',
                    mysql_comment='Список доступных дополнительных ролей пользователй',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
    op.create_index('name', 'n_role', ['name'], unique=False)
    op.create_table('service_roles',
                    sa.Column('id_user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
                    sa.Column('id_role', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(['id_role'], ['n_role.id'], name='service_roles_ibfk_1'),
                    sa.ForeignKeyConstraint(['id_user'], ['users.id'], name='service_roles_ibfk_2'),
                    sa.PrimaryKeyConstraint('id_user', 'id_role'),
                    comment='Дополнительные роли пользователей',
                    mysql_collate='utf8mb4_general_ci',
                    mysql_comment='Дополнительные роли пользователей',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
