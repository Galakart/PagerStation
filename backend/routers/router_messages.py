from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_messages
from backend.db.connection import get_session
from backend.models.model_messages import MessageSchema

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.get("/messages/", response_model=list[MessageSchema])
def get_messages(session: Session = Depends(get_session), offset: int = 0, limit: int = const.LIMIT_GET):
    """Вывод всех сообщений"""
    messages_tuple = db_messages.get_messages(session, offset, limit)
    return messages_tuple


@router.get("/messages/{id_message}", response_model=MessageSchema)
def get_message(session: Session = Depends(get_session), id_message: int = 0):
    """Вывод конкретного сообщения"""
    message_item = db_messages.get_message(session, id_message)
    if not message_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сообщение не найдено")
    return message_item


@router.post("/messages/", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
def create_message(session: Session = Depends(get_session), message_schema_item: MessageSchema = None):
    """Создание сообщения"""
    message_item = db_messages.create_message(session, message_schema_item)
    if not message_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка создания сообщения")
    return message_item


@router.delete("/messages/{id_message}", response_model=MessageSchema)
def delete_message(session: Session = Depends(get_session), id_message: int = 0):
    """Удаление сообщения"""
    message_item = db_messages.get_message(session, id_message)
    if not message_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сообщение не найдено")

    result = db_messages.delete_message(session, id_message)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления сообщения")
    return message_item
