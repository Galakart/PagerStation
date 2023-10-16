"""Модели utils"""
import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

# pylint: disable=too-few-public-methods


class StrictsIPaddress(Base):
    """IP адреса для ограничений на количество сообщений за период"""
    __tablename__ = 'stricts_ipaddresses'

    ip_address: Mapped[str] = mapped_column(String(16), primary_key=True)
    last_send: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        comment='Дата-время последней отправки'
    )
