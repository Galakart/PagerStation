"""Все enum"""
from enum import IntEnum, unique


@unique
class StatesEnum(IntEnum):
    """Стадии"""
    ASK_ID_PAGER = 10
    ASK_MESSAGE = 20
