"""Модели общие"""
import datetime

from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime,
                        ForeignKey, Integer, String, Table)
from sqlalchemy.orm import relationship

from models.base import Base

# TODO BigInteger и SmallInteger
# TODO соотношения между моделями настроить, чтобы например из Pager перескочить на Transmitter

# pylint: disable=missing-class-docstring,too-few-public-methods

BAUDRATES = {
    '512': 1,
    '1024': 2,
    '2048': 3,
}

FBITS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
}

CODEPAGES = {
    'lat': 1,
    'cyr': 2,
    'linguist': 3,
}

ROLES = {
    'admin': 10,
}

MAILDROP_TYPES = {
    'notification': 1,
    'news': 2,
    'weather': 3,
    'currency': 4,
}


class Baudrate(Base):
    __tablename__ = 'n_baudrates'
    __table_args__ = {"comment": "Скорости передачи данных"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(4), unique=True, nullable=False)


class Fbit(Base):
    __tablename__ = 'n_fbits'
    __table_args__ = {"comment": "Источники (функциональные биты)"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(1), unique=True, nullable=False)


class Codepage(Base):
    __tablename__ = 'n_codepages'
    __table_args__ = {"comment": "Кодировки текста"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(8), unique=True, nullable=False)


class Transmitter(Base):
    __tablename__ = 'transmitters'
    __table_args__ = {"comment": "Передатчики"}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    freq = Column(Integer, unique=True, nullable=False)
    id_baudrate = Column(Integer, ForeignKey('n_baudrates.id'), nullable=False)


user_pagers = Table(
    "user_pagers",
    Base.metadata,
    Column("id_user", Integer, ForeignKey("users.id")),
    Column("id_pager", Integer, ForeignKey("pagers.id")),
)


class Pager(Base):
    __tablename__ = 'pagers'
    __table_args__ = {"comment": "Пейджеры"}

    id = Column(Integer, primary_key=True, autoincrement=False, comment='Абонентский номер')
    capcode = Column(Integer, nullable=False)
    id_fbit = Column(Integer, ForeignKey('n_fbits.id'), nullable=False)
    id_codepage = Column(Integer, ForeignKey('n_codepages.id'), nullable=False)
    id_transmitter = Column(Integer, ForeignKey('transmitters.id'), nullable=False)
    users = relationship('User', secondary=user_pagers, back_populates='pagers')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"comment": "Пользователи пейджеров"}

    id = Column(Integer, primary_key=True)
    fio = Column(String(200), nullable=False)
    datar = Column(Date)
    pagers = relationship('Pager', secondary=user_pagers, back_populates='users')


class Role(Base):
    __tablename__ = 'n_role'
    __table_args__ = {"comment": "Список доступных дополнительных ролей пользователй"}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(25), unique=True, nullable=False)


class ServiceRole(Base):
    __tablename__ = 'service_roles'
    __table_args__ = {"comment": "Дополнительные роли пользователей"}

    id_user = Column(Integer, ForeignKey('users.id'), primary_key=True)
    id_role = Column(Integer, ForeignKey('n_role.id'), primary_key=True)


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
