"""Операции с юзерами"""
from models.mdl_pagers import Pager
from models.mdl_users import ROLES, ServiceRole, User

from db.connection import Session

# TODO в Users добавить поле active


def get_admins():
    """Все админы"""
    session = Session()
    values_tuple = session.query(User).join(ServiceRole, ServiceRole.id_user == User.id).filter(
        ServiceRole.id_role == ROLES['admin']).all()  # TODO ... Users.active==1
    session.close()
    return values_tuple


def get_user_pagers(id_user: int) -> Pager:  # TODO many-to-many
    session = Session()
    user = session.query(User).get(id_user)
    pagers = None
    if user:
        pagers = user.pagers
    session.close()
    return pagers
