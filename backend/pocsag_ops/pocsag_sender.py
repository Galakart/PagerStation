"""Всё по отправке сообщений в эфир"""
import logging
import os

from backend.models.model_hardware import BaudrateEnum
from backend.pocsag_ops.charset_encoder import CharsetEncoder

LOGGER = logging.getLogger()
charset_encoder = CharsetEncoder()


def message_to_air(capcode: int, fbit: int, freq: int, id_baudrate: int, id_codepage: int, message: str) -> bool:
    """Отправляет сообщение в эфир

    Args:
        capcode (int): капкод
        fbit (int): id источника
        freq (int): частота в Гц
        baudrate (int): id скорости
        id_codepage (int): id кодировки текста
        message (str): сообщение

    Returns:
        bool: успех
    """
    if not os.path.exists('./pocsag'):
        LOGGER.error('Не найден бинарник pocsag, сообщение просто помечено как отправленное')
        return True

    if id_baudrate == BaudrateEnum.BAUD_512.value:
        baudrate = 512
    elif id_baudrate == BaudrateEnum.BAUD_1200.value:
        baudrate = 1200
    elif id_baudrate == BaudrateEnum.BAUD_2400.value:
        baudrate = 2400
    else:
        return False

    capcode = f'{capcode:07d}'
    message_text = charset_encoder.encode_message(message, id_codepage)

    os.system(f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -r {baudrate} -t 1')
    return True
