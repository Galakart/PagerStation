"""Роутер - пейджинговые сообщения"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_messages
from backend.db.connection import get_session
from backend.models.enums import MessageTypeEnum
from backend.models.model_messages import MessageSchema
from backend.routers.dependencies import check_user_token_dependency

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    dependencies=[Depends(check_user_token_dependency)],
)


@router.get("/", response_model=list[MessageSchema])
def get_messages(
    offset: int = 0,
    limit: int = const.LIMIT_GET,
    session: Session = Depends(get_session)
):
    """Вывод всех сообщений"""
    messages = db_messages.get_messages(session, offset, limit)
    return messages


@router.get("/{uid_message}", response_model=MessageSchema)
def get_message(uid_message: uuid.UUID, session: Session = Depends(get_session)):
    """Вывод конкретного сообщения"""
    message_item = db_messages.get_message(session, uid_message)
    if not message_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сообщение не найдено")
    return message_item


@router.post("/", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
def create_message(message_schema_item: MessageSchema, session: Session = Depends(get_session)):
    """Создание сообщения"""
    if message_schema_item.id_message_type == MessageTypeEnum.PRIVATE \
            and not message_schema_item.id_pager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Для личных сообщений нужно обязательно указать абонентский номер (id_pager)"
        )

    if message_schema_item.id_message_type == MessageTypeEnum.GROUP \
            and not message_schema_item.id_group_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Для групповых сообщений нужно обязательно указать "
                "тип группового сообщения (id_group_type)"
            )
        )

    if message_schema_item.id_message_type == MessageTypeEnum.MAILDROP \
            and not message_schema_item.id_maildrop_type:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Для maildrop сообщений нужно обязательно указать "
                "тип новостного сообщения (id_maildrop_type)"
            )
        )

    message_item = db_messages.create_message(session, message_schema_item)
    if not message_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания сообщения"
        )
    return message_item


@router.delete("/{uid_message}", response_model=MessageSchema)
def delete_message(uid_message: uuid.UUID, session: Session = Depends(get_session)):
    """Удаление сообщения"""
    message_item = db_messages.get_message(session, uid_message)
    if not message_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сообщение не найдено")

    if message_item.sent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Сообщение уже было отправлено, его нельзя удалить"
        )

    result = db_messages.delete_message(session, uid_message)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления сообщения"
        )
    return message_item
