"""Модели сообщений"""
import datetime
import uuid
from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text, Uuid)

from backend.constants import MESSAGE_MAX_LENGTH

from .base import Base
from .model_hardware import CodepageEnum, FbitEnum

# pylint: disable=missing-class-docstring,too-few-public-methods


@unique
class MessageTypeEnum(Enum):
    PRIVATE = 1
    GROUP = 2
    MAILDROP = 3


@unique
class GroupTypeEnum(Enum):
    COMMON = 1
    ALERT = 2  # групповое сообщение с громким оповещением, независимо от настроек беззвучности пейджера


@unique
class MaildropTypeEnum(Enum):
    NOTIFICATION = 1
    WEATHER = 2
    CURRENCY = 3
    NEWS = 4


class MessageType(Base):
    __tablename__ = 'n_message_types'
    __table_args__ = {"comment": "Типы сообщений"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), unique=True, nullable=False)


class GroupType(Base):
    __tablename__ = 'n_group_types'
    __table_args__ = {"comment": "Типы групповых сообщений"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), unique=True, nullable=False)


class MailDropType(Base):
    __tablename__ = 'n_maildrop_types'
    __table_args__ = {"comment": "Типы новостных рассылок"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), unique=True, nullable=False)


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {"comment": "Сообщения"}

    uid = Column(Uuid, primary_key=True)
    id_message_type = Column(Integer, ForeignKey('n_message_types.id'), nullable=False)
    id_pager = Column(Integer, ForeignKey('pagers.id'), comment="указывается если сообщение личное (id_message_type=1)")
    id_group_type = Column(Integer, ForeignKey('n_group_types.id'), comment="указывается если сообщение групповое (id_message_type=2)")
    id_maildrop_type = Column(Integer, ForeignKey('n_maildrop_types.id'), comment="указывается если сообщение новостное (id_message_type=3)")
    message = Column(String(MESSAGE_MAX_LENGTH), nullable=False)
    sent = Column(Boolean, nullable=False, default=False)
    datetime_send_after = Column(DateTime, comment='Отправить после указанной даты-времени')
    datetime_create = Column(DateTime, nullable=False, default=datetime.datetime.now)


class MessageSchema(BaseModel):
    uid: Optional[uuid.UUID]
    id_message_type: MessageTypeEnum = Field(
        title="Тип сообщения",
    )
    # TODO добавить проверку, если id_message_type=1, то обязательно указывать id_pager, итд для остальных типов
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

    class Config:
        orm_mode = True


class GroupChannel(Base):
    __tablename__ = 'channels_group'
    __table_args__ = {"comment": "Групповые каналы трансмиттера"}

    id_transmitter = Column(Integer, ForeignKey('transmitters.id'), primary_key=True)
    capcode = Column(Integer, primary_key=True)
    id_fbit = Column(Integer, ForeignKey('n_fbits.id'), primary_key=True)
    id_group_type = Column(Integer, ForeignKey('n_group_types.id'), nullable=False)
    id_codepage = Column(Integer, ForeignKey('n_codepages.id'), nullable=False)


class GroupChannelSchema(BaseModel):
    id_transmitter: int = Field(
        title="id передатчика",
    )
    capcode: int = Field(
        title="Капкод",
        ge=10,
        le=9999999,
    )
    id_fbit: FbitEnum = Field(
        title="Источник",
    )
    id_group_type: GroupTypeEnum = Field(
        title="Тип группового сообщения",
    )
    id_codepage: CodepageEnum = Field(
        title="Кодировка текста",
    )

    class Config:
        orm_mode = True


class MailDropChannel(Base):
    __tablename__ = 'channels_maildrop'
    __table_args__ = {"comment": "Новостные каналы трансмиттера"}

    id_transmitter = Column(Integer, ForeignKey('transmitters.id'), primary_key=True)
    capcode = Column(Integer, primary_key=True)
    id_fbit = Column(Integer, ForeignKey('n_fbits.id'), primary_key=True)
    id_maildrop_type = Column(Integer, ForeignKey('n_maildrop_types.id'), nullable=False)
    id_codepage = Column(Integer, ForeignKey('n_codepages.id'), nullable=False)


class MailDropChannelSchema(BaseModel):
    id_transmitter: int = Field(
        title="id передатчика",
    )
    capcode: int = Field(
        title="Капкод",
        ge=10,
        le=9999999,
    )
    id_fbit: FbitEnum = Field(
        title="Источник",
    )
    id_maildrop_type: MaildropTypeEnum = Field(
        title="Тип новостного канала",
    )
    id_codepage: CodepageEnum = Field(
        title="Кодировка текста",
    )

    class Config:
        orm_mode = True


class MaildropRssFeed(Base):
    __tablename__ = 'rss_feeds'
    __table_args__ = {"comment": "RSS-ленты"}

    id = Column(BigInteger, primary_key=True)
    id_maildrop_type = Column(Integer, ForeignKey('n_maildrop_types.id'), nullable=False, unique=True)
    feed_link = Column(Text, nullable=False)
    datetime_create = Column(DateTime, nullable=False, default=datetime.datetime.now)
