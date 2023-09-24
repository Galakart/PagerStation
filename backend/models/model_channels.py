"""Модели каналов"""
import datetime

from pydantic import BaseModel, Field
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import GroupTypeEnum, MaildropTypeEnum
from .model_hardware import CodepageEnum, FbitEnum

# pylint: disable=missing-class-docstring,too-few-public-methods


class GroupChannel(Base):
    __tablename__ = 'channels_group'
    __table_args__ = {"comment": "Групповые каналы трансмиттера"}

    id_transmitter: Mapped[int] = mapped_column(Integer, ForeignKey('transmitters.id'), primary_key=True)
    capcode: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_fbit: Mapped[int] = mapped_column(Integer, ForeignKey('n_fbits.id'), primary_key=True)
    id_group_type: Mapped[int] = mapped_column(Integer, ForeignKey('n_group_types.id'), nullable=False)
    id_codepage: Mapped[int] = mapped_column(Integer, ForeignKey('n_codepages.id'), nullable=False)


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

# TODO может объединить в одной таблице БД все типы каналов


class MailDropChannel(Base):
    __tablename__ = 'channels_maildrop'
    __table_args__ = {"comment": "Новостные каналы трансмиттера"}

    id_transmitter: Mapped[int] = mapped_column(Integer, ForeignKey('transmitters.id'), primary_key=True)
    capcode: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_fbit: Mapped[int] = mapped_column(Integer, ForeignKey('n_fbits.id'), primary_key=True)
    id_maildrop_type: Mapped[int] = mapped_column(Integer, ForeignKey('n_maildrop_types.id'), nullable=False)
    id_codepage: Mapped[int] = mapped_column(Integer, ForeignKey('n_codepages.id'), nullable=False)


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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_maildrop_type: Mapped[int] = mapped_column(Integer, ForeignKey('n_maildrop_types.id'), nullable=False, unique=True)
    feed_link: Mapped[str] = mapped_column(Text, nullable=False)
    datetime_create: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
