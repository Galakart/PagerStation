from enum import Enum, unique


@unique
class BaudrateEnum(Enum):
    BAUD_512 = 1
    BAUD_1200 = 2
    BAUD_2400 = 3


@unique
class FbitEnum(Enum):
    BIT_0 = 0
    BIT_1 = 1
    BIT_2 = 2
    BIT_3 = 3


@unique
class CodepageEnum(Enum):
    LAT = 1
    CYR = 2
    LINGUIST = 3


@unique
class MessageTypeEnum(Enum):
    PRIVATE = 1
    GROUP = 2
    MAILDROP = 3


@unique
class GroupTypeEnum(Enum):
    COMMON = 1
    ALERT = 2  # групповое сообщение с громким оповещением, независимо от настроек беззвучности пейджера


@unique
class MaildropTypeEnum(Enum):
    NOTIFICATION = 1
    WEATHER = 2
    CURRENCY = 3
    NEWS = 4
