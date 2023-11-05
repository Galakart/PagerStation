"""Main Alice skill handler"""
import os
from enum import IntEnum, unique

import requests

API_URL = os.environ['API_URL']
PAGER_URL = f'{API_URL}/hardware/pagers/'
CREATE_MESSAGE_URL = f'{API_URL}/messages/'


@unique
class StatesEnum(IntEnum):
    """Стадии"""
    ASK_ID_PAGER = 10
    ASK_MESSAGE = 20


def handle_event(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    id_pager = None
    end_session = False

    # Начальный текст
    text = 'Назовите номер абонента'
    state = StatesEnum.ASK_ID_PAGER

    # TODO проверка на доступность всех параметров
    if 'state' in event and 'step_number' in event['state']['session']:
        match event['state']['session']['step_number']:

            case StatesEnum.ASK_ID_PAGER:
                id_pager = _get_id_pager_from_request(event['request']['nlu'])
                if id_pager:
                    try:
                        rest_response = requests.get(f'{PAGER_URL}{id_pager}', timeout=3)
                        if rest_response.status_code == 200:
                            text = f'Хорошо, продиктуйте сообщение для абонента {id_pager}'
                            state = StatesEnum.ASK_MESSAGE
                        else:
                            text = 'Нет такого абонента. Пожалуйста, назовите правильный номер'
                    except requests.exceptions.Timeout:
                        text = 'Сервис сейчас недоступен. Попробуйте попозже.'
                        end_session = True
                else:
                    text = 'Не удалось распознать номер, пожалуйста повторите.'

            case StatesEnum.ASK_MESSAGE:
                id_pager = event['state']['session']['id_pager']
                message = event['request']['original_utterance']
                state = None
                end_session = True

                payload = {
                    'id_message_type': 1,
                    'id_pager': id_pager,
                    'message': message
                }
                try:
                    rest_response = requests.post(CREATE_MESSAGE_URL, json=payload, timeout=3)
                    if rest_response.status_code == 201:
                        text = 'Сообщение будет отправлено. До свидания.'
                    else:
                        text = 'Что-то не так с сервисом. Попробуйте попозже.'
                        end_session = True
                except requests.exceptions.Timeout:
                    text = 'Сервис сейчас недоступен. Попробуйте попозже.'
                    end_session = True

    return {
        "version": event["version"],
        "session": event["session"],
        "response": {
            "text": text,
            "end_session": end_session
        },
        "session_state": {
            "step_number": state,
            "id_pager": id_pager
        },
    }


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
