"""Обработчики шагов навыка"""
import datetime
import logging
import os
import time
from random import choice

import enums
import phrases
import requests

logger = logging.getLogger()

REST_TIMEOUT = 4

AUTH_HEADER = {"Authorization": f"Bearer {os.environ['API_TOKEN']}"}
API_URL = os.environ['API_URL']
USERS_ME_URL = f'{API_URL}/users/me/'
PAGER_URL = f'{API_URL}/hardware/pagers/'
CREATE_MESSAGE_URL = f'{API_URL}/messages/'


def handle_start(event: dict) -> dict:
    """Проверка связи до сервера и запрос номера абонента"""
    time.tzset()
    try:
        rest_response = requests.get(
            USERS_ME_URL,
            headers=AUTH_HEADER,
            timeout=REST_TIMEOUT,
        )
        if rest_response.status_code != 200:
            raise requests.exceptions.Timeout
    except requests.exceptions.Timeout:
        return _create_result_dict(
            event=event,
            text=phrases.ERR_SKILL,
            end_session=True,
        )

    # Выберем приветствие в зависимости от времени суток, или рандомно какое-нибудь из стандартных
    cur_datetime = datetime.datetime.now()
    greetings_lst = []
    if (0 <= cur_datetime.hour <= 6) or (22 <= cur_datetime.hour <= 23):
        greetings_lst = phrases.GREETINGS_NIGHT.copy()
    elif 7 <= cur_datetime.hour <= 10:
        greetings_lst = phrases.GREETINGS_MORNING.copy()
    elif 11 <= cur_datetime.hour <= 16:
        greetings_lst = phrases.GREETINGS_DAY.copy()
    elif 17 <= cur_datetime.hour <= 21:
        greetings_lst = phrases.GREETINGS_EVENING.copy()
    greetings_lst.extend(phrases.GREETINGS_COMMON)

    # после приветствия спрашиваем номер абонента
    text = f'{choice(greetings_lst)}, {choice(phrases.ASK_NUMBER)}'

    session_state = event['state']['session']
    session_state['step_number'] = enums.StatesEnum.ASK_ID_PAGER

    return _create_result_dict(
        event=event,
        text=text,
        session_state=session_state,
    )


def handle_something_wrong(event: dict) -> dict:
    """Когда в навыке что-то пошло не так"""
    return _create_result_dict(
        event=event,
        text=phrases.ERR_SKILL,
        end_session=True,
    )


def handle_id_pager(event: dict) -> dict:
    """Проверка номера абонента и запрос текста сообщения"""
    session_state = event['state']['session']
    id_pager = _get_id_pager_from_request(event['request']['nlu'])
    if not id_pager:
        return _create_result_dict(
            event=event,
            text=phrases.ERR_WRONG_NUMBER,
            session_state=session_state,
        )

    try:
        rest_response = requests.get(
            f'{PAGER_URL}{id_pager}',
            headers=AUTH_HEADER,
            timeout=REST_TIMEOUT,
        )
        if rest_response.status_code == 404:
            return _create_result_dict(
                event=event,
                text=phrases.ERR_UNKNOWN,
                session_state=session_state,
            )
        if rest_response.status_code != 200:
            raise requests.exceptions.Timeout
    except requests.exceptions.Timeout:
        return _create_result_dict(
            event=event,
            text=phrases.ERR_SKILL,
            end_session=True,
        )

    # добавим в фразу "Номер такой-то найден" собственно сам номер, и спросим текст сообщения
    text = f'{choice(phrases.NUMBER_FOUND) % id_pager}. {choice(phrases.ASK_MESSAGE)}'

    session_state['id_pager'] = id_pager
    session_state['step_number'] = enums.StatesEnum.ASK_MESSAGE

    return _create_result_dict(
        event=event,
        text=text,
        session_state=session_state,
    )


def handle_message(event: dict) -> dict:
    """Отправка текста на пейджер, и фраза подтверждения"""
    session_state = event['state']['session']

    id_pager = event['state']['session']['id_pager']
    message = event['request']['original_utterance']

    payload = {
        'id_message_type': 1,
        'id_pager': id_pager,
        'message': message
    }
    try:
        rest_response = requests.post(
            CREATE_MESSAGE_URL,
            json=payload,
            headers=AUTH_HEADER,
            timeout=REST_TIMEOUT,
        )
        if rest_response.status_code != 201:
            raise requests.exceptions.Timeout
    except requests.exceptions.Timeout:
        return _create_result_dict(
            event=event,
            text=phrases.ERR_SKILL,
            end_session=True,
        )

    text = f'{choice(phrases.CONFIRM_SEND)}. {choice(phrases.GOODBYE)}'

    return _create_result_dict(
        event=event,
        text=text,
        end_session=True,
        session_state=session_state,
    )


def _get_id_pager_from_request(nlu: dict) -> int | None:
    """
    Представляет все произнесённые числа в фразе как один абонентский номер.
    :param nlu: словарь event['request']['nlu'].
    :return: абонентский номер.
    """
    id_pager = None

    number_part = ''
    for entity in nlu['entities']:
        if entity['type'] == 'YANDEX.NUMBER':
            number_part += str(entity['value'])
    if number_part.isdigit():
        id_pager = int(number_part)
    return id_pager


def _create_result_dict(
        event: dict,
        text: str,
        end_session: bool = False,
        session_state: dict | None = None
) -> dict:
    """Создание dict для ответа навыку"""
    if not session_state:
        session_state = event['state']['session']

    result_dict = {
        "version": event["version"],
        "session": event["session"],
        "response": {
            "text": text,
            "end_session": end_session
        },
        "session_state": session_state,
        # "session_state": {
        #     "step_number": 10,
        #     "id_pager": 1234,
        # },
    }
    return result_dict
