import datetime

from backend.db import db_hardware, db_messages
from backend.db.connection import SessionLocal
from backend.models.model_messages import MessageTypeEnum
from backend.pocsag_ops import pocsag_sender


def send_messages() -> bool:
    """Проверка и отправка неотправленных сообщений"""
    today_datetime = datetime.datetime.now()
    with SessionLocal() as session:
        messages_tuple = db_messages.get_unsent_messages(session, MessageTypeEnum.PRIVATE.value)
        for message_item in messages_tuple:
            if message_item.datetime_send_after and (today_datetime < message_item.datetime_send_after):
                continue

            pager_item = db_hardware.get_pager(session, message_item.id_pager)
            transmitter_item = db_hardware.get_transmitter(session, pager_item.id_transmitter)

            result = pocsag_sender.message_to_air(
                capcode=pager_item.capcode,
                fbit=pager_item.id_fbit,
                freq=transmitter_item.freq,
                id_baudrate=transmitter_item.id_baudrate,
                id_codepage=pager_item.id_codepage,
                message=message_item.message
            )
            if result:
                db_messages.mark_message_sent(session, message_item.uid)

    # unsent_messages_private_tuple = db.db_messages.get_unsent_messages_private()
    # if unsent_messages_private_tuple:
    #     unsent_message_private_item: MessagePrivate
    #     for unsent_message_private_item in unsent_messages_private_tuple:
    #         if not unsent_message_private_item.datetime_send_after or (today_datetime >= unsent_message_private_item.datetime_send_after):
    #             pager_item = db.db_hardware.get_pager(unsent_message_private_item.id_pager)
    #             transmitter_item = db.db_classifiers.find_classifier_object(Transmitter, pager_item.id_transmitter)
    #             baudrate_item = db.db_classifiers.find_classifier_object(Baudrate, transmitter_item.id_baudrate)
    #             codepage_item = db.db_classifiers.find_classifier_object(Codepage, pager_item.id_codepage)
    #             message_to_air(pager_item.capcode, pager_item.id_fbit, transmitter_item.freq,
    #                            baudrate_item.name, codepage_item.id, unsent_message_private_item.message)
    #             db.db_messages.mark_message_private_sent(unsent_message_private_item.id)

    # unsent_messages_maildrop_tuple = db.db_messages.get_unsent_messages_maildrop()
    # if unsent_messages_maildrop_tuple:
    #     unsent_message_maildrop_item: MessageMailDrop
    #     for unsent_message_maildrop_item in unsent_messages_maildrop_tuple:
    #         maildrop_channels_tuple = db.db_messages.get_maildrop_channels_by_type(
    #             unsent_message_maildrop_item.id_maildrop_type)
    #         for maildrop_channel_item in maildrop_channels_tuple:
    #             transmitter_item = db.db_classifiers.find_classifier_object(
    #                 Transmitter, maildrop_channel_item.id_transmitter)
    #             baudrate_item = db.db_classifiers.find_classifier_object(Baudrate, transmitter_item.id_baudrate)
    #             codepage_item = db.db_classifiers.find_classifier_object(Codepage, maildrop_channel_item.id_codepage)
    #             message_to_air(maildrop_channel_item.capcode, maildrop_channel_item.id_fbit,
    #                            transmitter_item.freq, baudrate_item.name, codepage_item.id, unsent_message_maildrop_item.message)
    #             db.db_messages.mark_message_maildrop_sent(unsent_message_maildrop_item.id)

    return True
