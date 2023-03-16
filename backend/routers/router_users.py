from fastapi import APIRouter, HTTPException, status

import db
from models.model_users import UserSchema

LIMIT_GET = 50

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/users", response_model=list[UserSchema])
def users_items_get(skip: int = 0, limit: int = LIMIT_GET):
    """Вывод всех юзеров"""
    all_users_tuple = db.db_users.get_all_users(skip, limit)
    return all_users_tuple


@router.get("/users/{id_user}", response_model=UserSchema)
def user_get(id_user: int):
    """Вывод конкретного юзера"""
    user_item = db.db_users.get_user(id_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user_item


@router.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def user_add(user_schema_item: UserSchema):
    """Добавление юзера"""
    user_item = db.db_users.create_user(user_schema_item)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка добавления пользователя")
    return user_item


@router.put("/users/{id_user}", response_model=UserSchema)
def user_update(user_schema_item: UserSchema, id_user: int):
    """Редактирование юзера"""
    user_item = db.db_users.get_user(id_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    user_item = db.db_users.update_user(user_schema_item, id_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка редактирования пользователя")
    return user_item


@router.delete("/users/{id_user}", response_model=UserSchema)
def user_delete(id_user: int):
    """Удаление юзера"""
    user_item = db.db_users.get_user(id_user)
    if not user_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    result = db.db_users.delete_user(id_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления пользователя")
    return user_item
