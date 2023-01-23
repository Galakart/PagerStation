"""Всё по отправке сообщений в эфир"""
import datetime
import os

import db
from models.model_messages import MessageMailDrop, MessagePrivate
from models.model_pagers import Baudrate, Codepage, Transmitter
from pocsag_sender.charset_encoder import CharsetEncoder

charset_encoder = CharsetEncoder()


def send_messages() -> bool:
    """Проверка и отправка неотправленных сообщений"""
    today_datetime = datetime.datetime.now()
    unsent_messages_private_tuple = db.db_messages.get_unsent_messages_private()
    if unsent_messages_private_tuple:
        unsent_message_private_item: MessagePrivate
        for unsent_message_private_item in unsent_messages_private_tuple:
            if not unsent_message_private_item.datetime_send_after or (today_datetime >= unsent_message_private_item.datetime_send_after):
                pager_item = db.db_pagers.get_pager(unsent_message_private_item.id_pager)
                transmitter_item = db.db_classifiers.find_classifier_object(Transmitter, pager_item.id_transmitter)
                baudrate_item = db.db_classifiers.find_classifier_object(Baudrate, transmitter_item.id_baudrate)
                codepage_item = db.db_classifiers.find_classifier_object(Codepage, pager_item.id_codepage)
                message_to_air(pager_item.capcode, pager_item.id_fbit, transmitter_item.freq,
                               baudrate_item.name, codepage_item.id, unsent_message_private_item.message)
                db.db_messages.mark_message_private_sent(unsent_message_private_item.id)

    unsent_messages_maildrop_tuple = db.db_messages.get_unsent_messages_maildrop()
    if unsent_messages_maildrop_tuple:
        unsent_message_maildrop_item: MessageMailDrop
        for unsent_message_maildrop_item in unsent_messages_maildrop_tuple:
            maildrop_channels_tuple = db.db_messages.get_maildrop_channels_by_type(
                unsent_message_maildrop_item.id_maildrop_type)
            for maildrop_channel_item in maildrop_channels_tuple:
                transmitter_item = db.db_classifiers.find_classifier_object(
                    Transmitter, maildrop_channel_item.id_transmitter)
                baudrate_item = db.db_classifiers.find_classifier_object(Baudrate, transmitter_item.id_baudrate)
                codepage_item = db.db_classifiers.find_classifier_object(Codepage, maildrop_channel_item.id_codepage)
                message_to_air(maildrop_channel_item.capcode, maildrop_channel_item.id_fbit,
                               transmitter_item.freq, baudrate_item.name, codepage_item.id, unsent_message_maildrop_item.message)
                db.db_messages.mark_message_maildrop_sent(unsent_message_maildrop_item.id)

    return True


def message_to_air(capcode: int, fbit: int, freq: int, baudrate: int, id_codepage: int, message: str) -> bool:
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
    capcode = f'{capcode:07d}'
    message_text = charset_encoder.encode_message(message, id_codepage)
    if not os.path.exists('./pocsag'):
        return False
    os.system(f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -r {baudrate} -t 1')
    return True
