"""БД - пользователи"""
import datetime
import logging
import uuid

from sqlalchemy import and_, extract, select
from sqlalchemy.orm import Session

from backend.db import auth
from backend.models.model_hardware import Pager
from backend.models.model_user import User, UserSchema

LOGGER = logging.getLogger()


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    result = session.execute(
        select(User)
        .where(
            User.api_login == username
        )
    )
    user = result.scalar()

    if not user:
        return None
    if not auth.verify_password(password, user.api_password):
        return None
    return user


def get_user_by_token(session: Session, token: str) -> User | None:
    username = auth.get_username_from_token(token)
    result = session.execute(
        select(User)
        .where(
            User.api_login == username
        )
    )
    user = result.scalar()

    if not user:
        return None
    return user


def get_users(session: Session, offset: int, limit: int):
    """Все пользователи"""
    result = session.execute(
        select(User)
        .offset(offset)
        .limit(limit)
    )
    users = result.scalars().all()
    return users


def get_user(session: Session, uid_user: uuid.UUID) -> User | None:
    """Пользователь по uid"""
    user = session.get(User, uid_user)
    return user


def create_user(session: Session, user_schema_item: UserSchema) -> User:
    """Создать пользователя"""
    user = User(
        uid=uuid.uuid4(),
        fio=user_schema_item.fio,
        datar=user_schema_item.datar,
        api_login=user_schema_item.api_login,
        api_password=auth.get_password_hash(user_schema_item.api_password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, uid_user: uuid.UUID, user_schema_item: UserSchema) -> User:
    """Изменить пользователя"""
    user = session.get(User, uid_user)
    if user:
        user.fio = user_schema_item.fio
        user.datar = user_schema_item.datar  # type: ignore
        if user_schema_item.api_login:
            user.api_login = user_schema_item.api_login
        if user_schema_item.api_password:
            user.api_password = auth.get_password_hash(user_schema_item.api_password)
        # TODO проверить правильное изменение логина/пароля api

        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def delete_user(session: Session, uid_user: uuid.UUID) -> bool:
    """Удалить пользователя"""
    user = session.get(User, uid_user)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False


def register_user_pager(session: Session, uid_user: uuid.UUID, id_pager: int) -> User:
    """Привязать пейджер к пользователю"""
    user = session.get(User, uid_user)
    pager = session.get(Pager, id_pager)
    if user:
        user.pagers.append(pager)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def unregister_user_pager(session: Session, uid_user: uuid.UUID, id_pager: int) -> User:
    """Отвязать пейджер от пользователя"""
    user = session.get(User, uid_user)
    pager = session.get(Pager, id_pager)
    if user:
        user.pagers.remove(pager)
        session.add(user)
        session.commit()
    return user


def get_users_with_birthday(session: Session):
    """Пользователи у которых сегодня днюха"""
    today_date = datetime.date.today()
    result = session.execute(
        select(User)
        .where(
            and_(
                extract('month', User.datar) == today_date.month,
                extract('day', User.datar) == today_date.day,
                User.pagers != None,  # pylint: disable=singleton-comparison
            )
        )
    )
    users = result.scalars().all()
    return users
