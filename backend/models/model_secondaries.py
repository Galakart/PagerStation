"""Модели таблиц many-to-many, вынесены в отдельный файл чтобы избежать кольцевых импортов"""
from sqlalchemy import Column, ForeignKey, Integer, Table, Uuid

from .base import Base

# pylint: disable=missing-class-docstring,too-few-public-methods


user_pagers = Table(
    "user_pagers",
    Base.metadata,
    Column("uid_user", Uuid, ForeignKey("users.uid"), primary_key=True),
    Column("id_pager", Integer, ForeignKey("pagers.id"), primary_key=True)
)
