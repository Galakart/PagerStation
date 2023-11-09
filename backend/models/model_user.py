"""Модели пользователей"""
import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Date, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .model_secondaries import user_pagers

# pylint: disable=too-few-public-methods


class User(Base):
    """Пользователи"""
    __tablename__ = 'users'

    uid: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    fio: Mapped[str] = mapped_column(String(200), nullable=False)
    datar: Mapped[datetime.date | None] = mapped_column(Date)
    pagers: Mapped[list] = relationship('Pager', secondary=user_pagers, back_populates='users')
    api_login: Mapped[str | None] = mapped_column(String(200), nullable=True, unique=True)
    api_password: Mapped[str | None] = mapped_column(String(200), nullable=True)


class UserSchema(BaseModel):
    """Схема - пользователи"""
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
    api_login: Optional[str] = Field(
        title="Логин для REST API",
        examples=["ivan"],
        max_length=200,
        min_length=3,
    )
    api_password: Optional[str] = Field(
        title="Пароль для REST API",
        examples=["newpassword555"],
        max_length=64,
        min_length=8,
    )

    class Config:  # pylint: disable=missing-class-docstring
        orm_mode = True


class TokenSchema(BaseModel):
    """Схема - токен доступа"""
    access_token: str
    token_type: str
