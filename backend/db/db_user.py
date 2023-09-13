import datetime
import logging

from sqlalchemy import and_, desc, extract, or_, select
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


def get_user(session: Session, id_user: int) -> User:
    user = session.get(User, id_user)
    return user


def create_user(session: Session, user_schema_item: UserSchema) -> User:
    user = User(
        fio=user_schema_item.fio,
        datar=user_schema_item.datar,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user_schema_item: UserSchema) -> User:
    user = session.get(User, user_schema_item.id)
    if user:
        user.fio = user_schema_item.fio
        user.datar = user_schema_item.datar

        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def delete_user(session: Session, id_user: int) -> bool:
    result = False
    user = session.get(User, id_user)
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
                extract('day', User.datar) == today_date.day
            )
        )
        .offset(offset)
        .limit(limit)
    )
    users = result.scalars().all()
    return users


# def get_user_pagers(id_user: int):
#     session = Session()
#     user = session.query(User).get(id_user)
#     pagers = None
#     if user:
#         pagers = user.pagers
#     session.close()
#     return pagers
