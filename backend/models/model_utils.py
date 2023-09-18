"""Модели utils"""
import datetime

from sqlalchemy import Column, DateTime, String

from .base import Base

# pylint: disable=missing-class-docstring,too-few-public-methods


class StrictsIPaddress(Base):
    __tablename__ = 'stricts_ipaddresses'
    __table_args__ = {"comment": "IP адреса для ограничений на количество сообщений за период"}

    ip_address = Column(String(16), primary_key=True)
    last_send = Column(DateTime, nullable=False, default=datetime.datetime.now, comment='Дата-время последней отправки')
