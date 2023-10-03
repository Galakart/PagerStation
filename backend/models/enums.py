"""Все enum, применямые в моделях"""
from enum import IntEnum, unique


@unique
class BaudrateEnum(IntEnum):
    """Скорость передачи сообщения"""
    BAUD_512 = 1
    BAUD_1200 = 2
    BAUD_2400 = 3


@unique
class FbitEnum(IntEnum):
    """Номер источника"""
    BIT_0 = 0
    BIT_1 = 1
    BIT_2 = 2
    BIT_3 = 3


@unique
class CodepageEnum(IntEnum):
    """Кодировка текста"""
    LAT = 1
    CYR = 2
    LINGUIST = 3


@unique
class MessageTypeEnum(IntEnum):
    """Тип сообщения"""
    PRIVATE = 1
    GROUP = 2
    MAILDROP = 3


@unique
class GroupTypeEnum(IntEnum):
    """Тип группового сообщения"""
    COMMON = 1
    ALERT = 2  # групповое сообщение с громким оповещением, независимо от настроек беззвучности пейджера


@unique
class MaildropTypeEnum(IntEnum):
    """Тип новостного сообщения"""
    # Motorola Advisor может принимать 4 капкода по 4 источника.
    # Значит у нас могут быть максимум 16 ячеек (8, если мы используем ещё личный и групповой капкод)
    # под разные темы новостных сообщений.
    # Темы 1-4 фиксированы (уведомления, погода, курс валют, новости),
    # остальные можно кастомизировать
    NOTIFICATION = 1
    WEATHER = 2
    CURRENCY = 3
    NEWS = 4
    CUSTOM_5 = 5
    CUSTOM_6 = 6
    CUSTOM_7 = 7
    CUSTOM_8 = 8
    CUSTOM_9 = 9
    CUSTOM_10 = 10
    CUSTOM_11 = 11
    CUSTOM_12 = 12
    CUSTOM_13 = 13
    CUSTOM_14 = 14
    CUSTOM_15 = 15
    CUSTOM_16 = 16
