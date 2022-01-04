from enum import Enum

import redis

rds = redis.Redis(host='localhost', port=6379,
                  decode_responses=True, charset='utf-8')


def get_state(id_user):
    """Возвращает текущую стадию
    Args:
        id_user (int): id пользователя;
    Returns:
        str: текущая стадия
    """
    state = rds.get(id_user)
    if not state:
        state = States.S_START.value
    return state


def set_state(id_user, state):
    """Сохраняет стадию на которую переходит пользователь
    Args:
        id_user (int): id пользователя;
        state (str): стадия (значение по ключу из класса States);
    """
    rds.set(id_user, state)


class States(Enum):
    """
        Стадии меню юзеров.
        Стадии регистрации начинаются на "0"
        Стадия главного меню всегда "1"
        Стадии после главного меню обозначаются как:
            1 цифра - всегда "1"
            2 цифра - роль юзера
            3 цифра - тематический подраздел
            4 цифра - шаг в этом подразделе
            цифры далее - пункты добавленные позднее
    """
    S_START = '0'

    S_MAINMENU = '1'
