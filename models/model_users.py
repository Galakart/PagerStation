"""Модели юзеров"""
import datetime
import enum

from pydantic import BaseModel, Field
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models.base import Base

# pylint: disable=missing-class-docstring,too-few-public-methods


class RoleEnum(enum.IntEnum):
    ADMIN = 10

# TODO BigInteger и SmallInteger
# relationship https://fastapi.tiangolo.com/tutorial/sql-databases/


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
    id: int | None
    fio: str = Field(
        title="ФИО пользователя",
        example="Иванов Иван Иванович",
        max_length=200,
        min_length=3,
    )
    datar: datetime.date = Field(
        title="Дата рождения пользователя",
        example=datetime.date(1991, 7, 12),
    )

    class Config:
        orm_mode = True


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
