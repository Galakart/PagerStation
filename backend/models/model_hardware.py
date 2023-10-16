"""Модели пейджеров"""
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import BaudrateEnum, CodepageEnum, FbitEnum
from .model_secondaries import user_pagers

# pylint: disable=too-few-public-methods


class Baudrate(Base):
    """Классификатор - скорости передачи данных"""
    __tablename__ = 'n_baudrates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(4), unique=True, nullable=False)


class Fbit(Base):
    """Классификатор - источники (функциональные биты)"""
    __tablename__ = 'n_fbits'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(1), unique=True, nullable=False)


class Codepage(Base):
    """Классификатор - кодировки текста"""
    __tablename__ = 'n_codepages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(8), unique=True, nullable=False)


class Transmitter(Base):
    """Передатчики"""
    __tablename__ = 'transmitters'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    freq: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    id_baudrate: Mapped[int] = mapped_column(Integer, ForeignKey('n_baudrates.id'), nullable=False)


class TransmitterSchema(BaseModel):
    """Схема - передатчики"""
    id: Optional[int]
    name: str = Field(
        title="Название передатчика",
        examples=["Motorola"],
        max_length=50,
    )
    freq: int = Field(
        title="Частота, Гц",
        examples=[159025000],
        gt=60000000,
        lt=999999999,
    )
    id_baudrate: BaudrateEnum = Field(
        title="Скорость передачи",
    )

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class Pager(Base):
    """Пейджеры"""
    __tablename__ = 'pagers'

    id: Mapped[int] = mapped_column(  # абонентский номер
        Integer,
        primary_key=True,
        autoincrement=False
    )
    capcode: Mapped[int] = mapped_column(Integer, nullable=False)
    id_fbit: Mapped[int] = mapped_column(Integer, ForeignKey('n_fbits.id'), nullable=False)
    id_codepage: Mapped[int] = mapped_column(Integer, ForeignKey('n_codepages.id'), nullable=False)
    id_transmitter: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('transmitters.id'),
        nullable=False
    )
    users: Mapped[list] = relationship('User', secondary=user_pagers, back_populates='pagers')


class PagerSchema(BaseModel):
    """Схема - пейджеры"""
    id: int = Field(
        title="Абонентский номер",
    )
    capcode: int = Field(
        title="Приватный капкод",
        ge=10,  # из-за особенностей POCSAG-протокола, не рекомендуются капкоды меньше 10
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
    users: Optional[list] = Field(
        title="Пользователи пейджера"
    )

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True
