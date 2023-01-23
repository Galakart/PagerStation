"""Операции с юзерами"""
import datetime

from sqlalchemy.sql.expression import extract

from db.connection import Session
from models.model_users import ROLES, ServiceRole, User

# TODO в Users добавить поле active


def get_admins():
    """Все админы"""
    session = Session()
    values_tuple = session.query(User).join(ServiceRole, ServiceRole.id_user == User.id).filter(
        ServiceRole.id_role == ROLES['admin']).all()  # TODO ... Users.active==1
    session.close()
    return values_tuple


def get_user_pagers(id_user: int):
    session = Session()
    user = session.query(User).get(id_user)
    pagers = None
    if user:
        pagers = user.pagers
    session.close()
    return pagers


def get_users_with_birthday():
    session = Session()
    today_date = datetime.date.today()
    values_tuple = session.query(User).filter(
        extract('month', User.datar) == today_date.month,
        extract('day', User.datar) == today_date.day
    ).all()
    return values_tuple
