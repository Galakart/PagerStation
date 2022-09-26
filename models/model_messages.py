"""Модели сообщений"""
import datetime

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)

from models.base import Base

# pylint: disable=missing-class-docstring,too-few-public-methods


MAILDROP_TYPES = {
    'notification': 1,
    'news': 2,
    'weather': 3,
    'currency': 4,
}


class MessagePrivate(Base):
    __tablename__ = 'messages_private'
    __table_args__ = {"comment": "Сообщения - личные"}

    id = Column(Integer, primary_key=True)
    id_pager = Column(Integer, ForeignKey('pagers.id'), nullable=False)
    message = Column(String(950), nullable=False)
    sent = Column(Boolean, nullable=False, default=False)
    date_create = Column(DateTime, nullable=False, default=datetime.datetime.now)


class MailDropType(Base):
    __tablename__ = 'n_maildrop_types'
    __table_args__ = {"comment": "Типы новостных рассылок"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), unique=True, nullable=False)


class MailDropChannels(Base):
    __tablename__ = 'maildrop_channels'
    __table_args__ = {"comment": "Новостные каналы трансмиттера, и их капкоды"}

    id_transmitter = Column(Integer, ForeignKey('transmitters.id'), primary_key=True)
    capcode = Column(Integer, primary_key=True)
    id_fbit = Column(Integer, ForeignKey('n_fbits.id'), primary_key=True)
    id_maildrop_type = Column(Integer, ForeignKey('n_maildrop_types.id'), nullable=False)
    id_codepage = Column(Integer, ForeignKey('n_codepages.id'), nullable=False)


class MessageMailDrop(Base):
    __tablename__ = 'messages_maildrop'
    __table_args__ = {"comment": "Сообщения - новостные"}

    id = Column(BigInteger, primary_key=True)
    id_maildrop_type = Column(Integer, ForeignKey('n_maildrop_types.id'), nullable=False)
    message = Column(String(950), nullable=False)
    sent = Column(Boolean, nullable=False, default=False)
    date_create = Column(DateTime, nullable=False, default=datetime.datetime.now)
