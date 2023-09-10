from backend.models.model_user import User
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression as sql

def get_all_users(db: Session, skip: int = 0, limit: int = 0):
    query = sql.select(User)
    users = db.execute(query)
    users = users.scalars().all()
    return users



# def get_user(id_user: int) -> User:
#     session = Session()
#     value = session.query(User).get(id_user)
#     session.close()
#     return value


# def create_user(user_schema_item: UserSchema) -> User:
#     session = Session()
#     try:
#         user_item = User(
#             fio=user_schema_item.fio,
#             datar=user_schema_item.datar,
#         )
#         session.add(user_item)
#         session.commit()
#         session.refresh(user_item)
#         return user_item
#     except Exception as ex:
#         LOGGER.error(ex)
#     finally:
#         session.close()


# def update_user(user_schema_item: UserSchema, id_user: int) -> User:
#     session = Session()
#     try:
#         user_item = session.query(User).get(id_user)
#         if user_item:
#             user_item.fio = user_schema_item.fio
#             user_item.datar = user_schema_item.datar
#             session.add(user_item)
#             session.commit()
#             session.refresh(user_item)
#         else:
#             user_item = None
#         return user_item
#     except Exception as ex:
#         LOGGER.error(ex)
#     finally:
#         session.close()


# def delete_user(id_user: int) -> bool:
#     session = Session()
#     result = False
#     try:
#         user_item = session.query(User).get(id_user)
#         if user_item:
#             session.delete(user_item)
#             session.commit()
#             result = True
#     except Exception as ex:
#         LOGGER.error(ex)
#     finally:
#         session.close()
#     return result


# def get_user_pagers(id_user: int):
#     session = Session()
#     user = session.query(User).get(id_user)
#     pagers = None
#     if user:
#         pagers = user.pagers
#     session.close()
#     return pagers


# def get_users_with_birthday():
#     session = Session()
#     today_date = datetime.date.today()
#     values_tuple = session.query(User).filter(
#         extract('month', User.datar) == today_date.month,
#         extract('day', User.datar) == today_date.day
#     ).all()
#     return values_tuple
