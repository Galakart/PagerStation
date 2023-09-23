import datetime
import logging
import uuid

from sqlalchemy import and_, extract, select
from sqlalchemy.orm import Session

from backend.models.model_user import User, UserSchema

LOGGER = logging.getLogger()


def get_users(session: Session, offset=None, limit=None):
    result = session.execute(
        select(User)
        .offset(offset)
        .limit(limit)
    )
    users = result.scalars().all()
    return users


def get_user(session: Session, uid_user: uuid.UUID) -> User:
    user = session.get(User, uid_user)
    return user


def create_user(session: Session, user_schema_item: UserSchema) -> User:
    user = User(
        uid=uuid.uuid4(),
        fio=user_schema_item.fio,
        datar=user_schema_item.datar,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, uid_user: uuid.UUID, user_schema_item: UserSchema) -> User:
    user = session.get(User, uid_user)
    if user:
        user.fio = user_schema_item.fio
        user.datar = user_schema_item.datar

        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def delete_user(session: Session, uid_user: uuid.UUID) -> bool:
    result = False
    user = session.get(User, uid_user)
    if user:
        session.delete(user)
        session.commit()
        result = True
    return result


def get_users_with_birthday(session: Session, offset=None, limit=None):
    today_date = datetime.date.today()
    result = session.execute(
        select(User)
        .where(
            and_(
                extract('month', User.datar) == today_date.month,
                extract('day', User.datar) == today_date.day,
                User.pagers != None,
            )
        )
        .offset(offset)
        .limit(limit)
    )
    users = result.scalars().all()
    return users
