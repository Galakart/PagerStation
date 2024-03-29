"""Модели сообщений"""
import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from backend.constants import MESSAGE_MAX_LENGTH

from .base import Base
from .enums import GroupTypeEnum, MaildropTypeEnum, MessageTypeEnum

# pylint: disable=too-few-public-methods


class MessageType(Base):
    """Классификатор - типы сообщений"""
    __tablename__ = 'n_message_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class GroupType(Base):
    """Классификатор - типы групповых сообщений"""
    __tablename__ = 'n_group_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class MailDropType(Base):
    """Классификатор - типы новостных рассылок"""
    __tablename__ = 'n_maildrop_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Message(Base):
    """Сообщения"""
    __tablename__ = 'messages'

    uid: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    id_message_type: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('n_message_types.id'),
        nullable=False
    )
    id_pager: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('pagers.id'),
        nullable=True
    )
    id_group_type: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('n_group_types.id'),
        nullable=True
    )
    id_maildrop_type: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('n_maildrop_types.id'),
        nullable=True
    )
    message: Mapped[str] = mapped_column(String(MESSAGE_MAX_LENGTH), nullable=False)
    sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    datetime_send_after: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    datetime_create: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now
    )


class MessageSchema(BaseModel):
    """Схема - сообщения"""
    uid: Optional[uuid.UUID]
    id_message_type: MessageTypeEnum = Field(
        title="Тип сообщения",
    )
    id_pager: Optional[int] = Field(
        title="id пейджера (для личных сообщений)",
    )
    id_group_type: Optional[GroupTypeEnum] = Field(
        title="Тип группового сообщения (для групповых сообщений)",
    )
    id_maildrop_type: Optional[MaildropTypeEnum] = Field(
        title="Тип новостного сообщения (для новостных сообщений)",
    )
    message: str = Field(
        title="Текст сообщения",
        max_length=MESSAGE_MAX_LENGTH,
    )
    sent: Optional[bool] = Field(
        title="отправлено ли передатчиком"
    )
    datetime_send_after: Optional[datetime.datetime] = Field(
        title="после какого времени отправить",
    )
    datetime_create: Optional[datetime.datetime] = Field(
        title="Дата и время отправки",
    )

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
