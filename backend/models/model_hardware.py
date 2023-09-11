"""Модели пейджеров"""
import enum
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .model_user import user_pagers

# pylint: disable=missing-class-docstring,too-few-public-methods


class BaudrateEnum(enum.Enum):
    BAUD_512 = 1
    BAUD_1200 = 2
    BAUD_2400 = 3


class FbitEnum(enum.Enum):
    BIT_0 = 0
    BIT_1 = 1
    BIT_2 = 2
    BIT_3 = 3


class CodepageEnum(enum.Enum):
    LAT = 1
    CYR = 2
    LINGUIST = 3


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


class TransmitterSchema(BaseModel):
    id: Optional[int]
    name: str = Field(
        title="Название передатчика",
        examples=["Motorola"],
        max_length=50,
    )
    freq: int = Field(
        title="Частота, Гц",
        examples=[159025000],
        gt=0,
        lt=999999999,
    )
    id_baudrate: BaudrateEnum = Field(
        title="Скорость передачи",
    )

    class Config:
        from_attributes = True


class Pager(Base):
    __tablename__ = 'pagers'
    __table_args__ = {"comment": "Пейджеры"}

    id = Column(Integer, primary_key=True, autoincrement=False, comment='Абонентский номер')
    capcode = Column(Integer, nullable=False)
    id_fbit = Column(Integer, ForeignKey('n_fbits.id'), nullable=False)
    id_codepage = Column(Integer, ForeignKey('n_codepages.id'), nullable=False)
    id_transmitter = Column(Integer, ForeignKey('transmitters.id'), nullable=False)
    users = relationship('User', secondary=user_pagers, back_populates='pagers')


class PagerSchema(BaseModel):
    id: int = Field(
        title="Абонентский номер",
    )
    capcode: int = Field(
        title="Приватный капкод",
        ge=10,  # из-за особенностей POCSAG-протокола, не рекомендуется использовать капкоды меньше 10
        le=9999999,
    )
    id_fbit: FbitEnum = Field(
        title="Приватный источник",
    )
    id_codepage: CodepageEnum = Field(
        title="Кодировка пейджера",
    )
    id_transmitter: int = Field(
        title="id передатчика",
    )

    class Config:
        from_attributes = True
