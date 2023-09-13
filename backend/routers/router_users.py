from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_user
from backend.db.connection import get_session
from backend.models.model_user import UserSchema

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserSchema])
def get_users(session: Session = Depends(get_session), offset: int = 0, limit: int = const.LIMIT_GET):
    """Вывод всех пользователей"""
    users_tuple = db_user.get_users(session, offset, limit)
    return users_tuple


@router.get("/{id_user}", response_model=UserSchema)
def get_user(session: Session = Depends(get_session), id_user: int = 0):
    """Вывод конкретного пользователя"""
    user_item = db_user.get_user(session, id_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user_item


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(session: Session = Depends(get_session), user_schema_item: UserSchema = None):
    """Добавление пользователя"""
    user_item = db_user.create_user(session, user_schema_item)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка добавления пользователя")
    return user_item


@router.put("/{id_user}", response_model=UserSchema)
def update_user(session: Session = Depends(get_session), user_schema_item: UserSchema = None):
    """Редактирование пользователя"""
    user_item = db_user.get_user(session, user_schema_item.id)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    user_item = db_user.update_user(session, user_schema_item)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка редактирования пользователя")
    return user_item


@router.delete("/{id_user}", response_model=UserSchema)
def delete_user(session: Session = Depends(get_session), id_user: int = 0):
    """Удаление пользователя"""
    user_item = db_user.get_user(session, id_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    result = db_user.delete_user(session, id_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления пользователя")
    return user_item


@router.get("/birthdays/", response_model=list[UserSchema])
def get_users_with_birthdays(session: Session = Depends(get_session), offset: int = 0, limit: int = const.LIMIT_GET):
    """Вывод всех пользователей, у кого сегодня день рождения"""
    users_tuple = db_user.get_users_with_birthday(session, offset, limit)
    return users_tuple
