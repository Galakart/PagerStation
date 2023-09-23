"""Модели пользователей"""
import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Uuid
from sqlalchemy.orm import relationship

from .base import Base

# pylint: disable=missing-class-docstring,too-few-public-methods


user_pagers = Table(
    "user_pagers",
    Base.metadata,
    Column("uid_user", Uuid, ForeignKey("users.uid")),
    Column("id_pager", Integer, ForeignKey("pagers.id")),
)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"comment": "Пользователи пейджеров"}

    uid = Column(Uuid, primary_key=True)
    fio = Column(String(200), nullable=False)
    datar = Column(Date)
    pagers = relationship('Pager', secondary=user_pagers, back_populates='users')


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

    class Config:
        orm_mode = True
