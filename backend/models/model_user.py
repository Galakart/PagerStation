"""Модели пользователей"""
import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Date, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .model_secondaries import user_pagers

# pylint: disable=missing-class-docstring,too-few-public-methods


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"comment": "Пользователи пейджеров"}

    uid: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    fio: Mapped[str] = mapped_column(String(200), nullable=False)
    datar: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    pagers: Mapped[list] = relationship('Pager', secondary=user_pagers, back_populates='users')


class UserSchema(BaseModel):
    uid: Optional[uuid.UUID]
    fio: str = Field(
        title="ФИО пользователя",
        examples=["Иванов Иван Иванович"],
        max_length=200,
        min_length=3,
    )
    datar: Optional[datetime.date] = Field(
        title="Дата рождения пользователя",
        examples=[datetime.date(1991, 7, 12)],
    )
    pagers: Optional[list] = Field(
        title="Пейджеры пользователя"
    )

    class Config:
        orm_mode = True
