"""Всё по отправке сообщений в эфир"""
import logging
import os

from backend.models.model_hardware import Transmitter
from backend.pocsag_ops.charset_encoder import CharsetEncoder

LOGGER = logging.getLogger()
charset_encoder = CharsetEncoder()


def message_to_air(
        transmitter: Transmitter,
        capcode: int,
        fbit: int,
        id_codepage: int,
        message: str
) -> bool:
    """Отправляет сообщение в эфир"""
    capcode_formatted = f'{capcode:07d}'
    message_encoded = charset_encoder.encode_message(message, id_codepage)
    fbit = fbit - 1  # у rpitx отсчёт источников идёт от 0

    if transmitter.external and transmitter.external_command:
        command = transmitter.external_command \
            .replace("{capcode}", str(capcode)) \
            .replace("{fbit}", str(fbit)) \
            .replace("{freq}", str(transmitter.freq)) \
            .replace("{id_baudrate}", str(transmitter.id_baudrate)) \
            .replace("{id_codepage}", str(id_codepage)) \
            .replace("{message}", message)
    else:
        if not os.path.exists('./pocsag'):
            LOGGER.error('Не найден бинарник pocsag, сообщение просто помечено как отправленное')
            return True
        command = (
            f'echo "{capcode_formatted}:{message_encoded}" | sudo ./pocsag -f "{transmitter.freq}" '
            f'-b {fbit} -r {transmitter.id_baudrate} -t 1'
        )

    os.system(command)
    return True
