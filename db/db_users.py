"""Операции с юзерами"""
import datetime
import logging

from sqlalchemy.sql.expression import extract

from db.connection import Session
from models.model_users import RoleEnum, ServiceRole, User, UserSchema

LOGGER = logging.getLogger('applog')
# TODO в Users добавить поле active


def get_all_users(skip: int, limit: int) -> tuple[User] | None:
    session = Session()
    values_tuple = session.query(User).offset(skip).limit(limit).all()
    session.close()
    return values_tuple


def get_user(id_user: int) -> User | None:
    session = Session()
    value = session.query(User).get(id_user)
    session.close()
    return value


def create_user(user_schema_item: UserSchema) -> User:
    session = Session()
    try:
        user_item = User(
            fio=user_schema_item.fio,
            datar=user_schema_item.datar,
        )
        session.add(user_item)
        session.commit()
        session.refresh(user_item)
        return user_item
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()


def update_user(user_schema_item: UserSchema, id_user: int) -> User:
    session = Session()
    try:
        user_item = session.query(User).get(id_user)
        if user_item:
            user_item.fio = user_schema_item.fio
            user_item.datar = user_schema_item.datar
            session.add(user_item)
            session.commit()
            session.refresh(user_item)
        else:
            user_item = None
        return user_item
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()


def delete_user(id_user: int) -> bool:
    session = Session()
    result = False
    try:
        user_item = session.query(User).get(id_user)
        if user_item:
            session.delete(user_item)
            session.commit()
            result = True
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()
    return result


def get_admins():
    """Все админы"""
    session = Session()
    values_tuple = session.query(User).join(ServiceRole, ServiceRole.id_user == User.id).filter(
        ServiceRole.id_role == RoleEnum.ADMIN.value).all()  # TODO ... Users.active==1
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
