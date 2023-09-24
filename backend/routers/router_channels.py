from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db import db_channels
from backend.db.connection import get_session
from backend.models.model_channels import (GroupChannelSchema,
                                           MailDropChannelSchema)

router = APIRouter(
    prefix="/channels",
    tags=["channels"],
)

# TODO все ли REST методы нужны


@router.get("/group/", response_model=list[GroupChannelSchema])
def get_group_channels(session: Session = Depends(get_session)):
    """Вывод всех групповых каналов"""
    group_channels_tuple = db_channels.get_group_channels(session)
    return group_channels_tuple


@router.post("/group/", response_model=GroupChannelSchema, status_code=status.HTTP_201_CREATED)
def create_group_channel(group_channel_schema_item: GroupChannelSchema, session: Session = Depends(get_session)):
    """Создание группового канала"""
    channel_item = db_channels.create_group_channel(session, group_channel_schema_item)
    if not channel_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка создания группового канала")
    return channel_item


@router.delete("/group/", response_model=GroupChannelSchema)
def delete_group_channel(id_transmitter: int, capcode: int, id_fbit: int, session: Session = Depends(get_session)):
    """Удаление группового канала"""
    channel_item = db_channels.get_group_channel(session, id_transmitter, capcode, id_fbit)
    if not channel_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Канал не найден")

    result = db_channels.delete_group_channel(session, id_transmitter, capcode, id_fbit)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления канала")
    return channel_item


@router.get("/maildrop/", response_model=list[MailDropChannelSchema])
def get_maildrop_channels(session: Session = Depends(get_session)):
    """Вывод всех новостных каналов"""
    maildrop_channels_tuple = db_channels.get_maildrop_channels(session)
    return maildrop_channels_tuple


@router.post("/maildrop/", response_model=MailDropChannelSchema, status_code=status.HTTP_201_CREATED)
def create_maildrop_channel(maildrop_channel_schema_item: MailDropChannelSchema, session: Session = Depends(get_session)):
    """Создание группового канала"""
    channel_item = db_channels.create_maildrop_channel(session, maildrop_channel_schema_item)
    if not channel_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка создания новостного канала")
    return channel_item


@router.delete("/maildrop/", response_model=MailDropChannelSchema)
def delete_maildrop_channel(id_transmitter: int, capcode: int, id_fbit: int, session: Session = Depends(get_session)):
    """Удаление новостного канала"""
    channel_item = db_channels.get_maildrop_channel(session, id_transmitter, capcode, id_fbit)
    if not channel_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Канал не найден")

    result = db_channels.delete_maildrop_channel(session, id_transmitter, capcode, id_fbit)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления канала")
    return channel_item
