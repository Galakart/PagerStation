"""Модели пейджеров"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base
from models.mdl_users import user_pagers

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

# TODO соотношения между моделями настроить, чтобы например из Pager перескочить на Transmitter


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


class Pager(Base):
    __tablename__ = 'pagers'
    __table_args__ = {"comment": "Пейджеры"}

    id = Column(Integer, primary_key=True, autoincrement=False, comment='Абонентский номер')
    capcode = Column(Integer, nullable=False)
    id_fbit = Column(Integer, ForeignKey('n_fbits.id'), nullable=False)
    id_codepage = Column(Integer, ForeignKey('n_codepages.id'), nullable=False)
    id_transmitter = Column(Integer, ForeignKey('transmitters.id'), nullable=False)
    users = relationship('User', secondary=user_pagers, back_populates='pagers')
