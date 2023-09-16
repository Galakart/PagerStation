"""Модели пользователей"""
import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .base import Base

# pylint: disable=missing-class-docstring,too-few-public-methods


user_pagers = Table(
    "user_pagers",
    Base.metadata,
    Column("id_user", Integer, ForeignKey("users.id")),
    Column("id_pager", Integer, ForeignKey("pagers.id")),
)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"comment": "Пользователи пейджеров"}

    id = Column(Integer, primary_key=True)
    fio = Column(String(200), nullable=False)
    datar = Column(Date)
    pagers = relationship('Pager', secondary=user_pagers, back_populates='users')


class UserSchema(BaseModel):
    id: Optional[int]
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

    class Config:
        orm_mode = True
