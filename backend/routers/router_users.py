"""Роутер - пользователи"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_hardware, db_user
from backend.db.connection import get_session
from backend.models.model_user import UserSchema

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserSchema])
def get_users(
    offset: int = 0,
    limit: int = const.LIMIT_GET,
    session: Session = Depends(get_session)
):
    """Вывод всех пользователей"""
    users = db_user.get_users(session, offset, limit)
    return users


@router.get("/{uid_user}", response_model=UserSchema)
def get_user(uid_user: uuid.UUID, session: Session = Depends(get_session)):
    """Вывод конкретного пользователя"""
    user_item = db_user.get_user(session, uid_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user_item


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user_schema_item: UserSchema, session: Session = Depends(get_session)):
    """Добавление пользователя"""
    user_item = db_user.create_user(session, user_schema_item)
    if not user_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка добавления пользователя"
        )
    return user_item


@router.put("/{uid_user}", response_model=UserSchema)
def update_user(
    uid_user: uuid.UUID,
    user_schema_item: UserSchema,
    session: Session = Depends(get_session)
):
    """Редактирование пользователя"""
    user_item = db_user.get_user(session, uid_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    user_item = db_user.update_user(session, uid_user, user_schema_item)
    if not user_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка редактирования пользователя"
        )
    return user_item


@router.delete("/{uid_user}", response_model=UserSchema)
def delete_user(uid_user: uuid.UUID, session: Session = Depends(get_session)):
    """Удаление пользователя"""
    user_item = db_user.get_user(session, uid_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    result = db_user.delete_user(session, uid_user)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления пользователя"
        )
    return user_item


@router.put("/pagers/", response_model=UserSchema)
def register_user_pager(
    uid_user: uuid.UUID,
    id_pager: int,
    session: Session = Depends(get_session)
):
    """Привязка пейджера к пользователю"""
    user_item = db_user.get_user(session, uid_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")
    if pager_item in user_item.pagers:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пейджер уже зарегистрирован на пользователя"
        )

    user_item = db_user.register_user_pager(session, uid_user, id_pager)
    if not user_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка привязки пейджера"
        )
    return user_item


@router.delete("/pagers/", response_model=UserSchema)
def unregister_user_pager(
    uid_user: uuid.UUID,
    id_pager: int,
    session: Session = Depends(get_session)
):
    """Удаление пейджера у пользователя"""
    user_item = db_user.get_user(session, uid_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    user_item = db_user.unregister_user_pager(session, uid_user, id_pager)
    if not user_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка отвязки пейджера"
        )
    return user_item


@router.get("/birthdays/", response_model=list[UserSchema])
def get_users_with_birthdays(session: Session = Depends(get_session)):
    """Вывод всех пользователей, у кого сегодня день рождения"""
    users = db_user.get_users_with_birthday(session)
    return users
