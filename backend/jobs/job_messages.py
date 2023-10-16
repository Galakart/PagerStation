"""Периодические действия - сообщения"""
import datetime
import logging
import random

from backend.db import db_channels, db_hardware, db_messages, db_user
from backend.db.connection import SessionLocal
from backend.models.model_messages import MessageSchema, MessageTypeEnum
from backend.pocsag_ops import pocsag_sender

LOGGER = logging.getLogger()


def send_messages():
    """Проверка и отправка неотправленных сообщений"""
    with SessionLocal() as session:
        messages = db_messages.get_unsent_messages(session)
        for message_item in messages:

            match message_item.id_message_type:
                case MessageTypeEnum.PRIVATE.value:
                    pager_item = db_hardware.get_pager(session, message_item.id_pager)
                    if not pager_item:
                        continue

                    transmitter_item = db_hardware.get_transmitter(
                        session,
                        pager_item.id_transmitter
                    )
                    if not transmitter_item:
                        continue

                    result = pocsag_sender.message_to_air(
                        capcode=pager_item.capcode,
                        fbit=pager_item.id_fbit,
                        freq=transmitter_item.freq,
                        id_baudrate=transmitter_item.id_baudrate,
                        id_codepage=pager_item.id_codepage,
                        message=message_item.message
                    )
                    if not result:
                        LOGGER.error('Ошибка отправки личного сообщения id: %s', message_item.uid)
                        continue

                    db_messages.mark_message_sent(session, message_item.uid)

                case MessageTypeEnum.GROUP.value:
                    group_channels = db_channels.get_group_channels_by_type(
                        session,
                        message_item.id_group_type
                    )
                    if not group_channels:
                        continue

                    result = False
                    for group_channel in group_channels:
                        transmitter_item = db_hardware.get_transmitter(
                            session,
                            group_channel.id_transmitter
                        )
                        if not transmitter_item:
                            continue
                        result = pocsag_sender.message_to_air(
                            capcode=group_channel.capcode,
                            fbit=group_channel.id_fbit,
                            freq=transmitter_item.freq,
                            id_baudrate=transmitter_item.id_baudrate,
                            id_codepage=group_channel.id_codepage,
                            message=message_item.message
                        )
                    if not result:
                        LOGGER.error(
                            'Ошибка отправки группового сообщения id: %s',
                            message_item.uid
                        )
                        continue

                    db_messages.mark_message_sent(session, message_item.uid)

                case MessageTypeEnum.MAILDROP.value:
                    maildrop_channels = db_channels.get_maildrop_channels_by_type(
                        session,
                        message_item.id_maildrop_type
                    )
                    if not maildrop_channels:
                        continue

                    result = False
                    for maildrop_channel in maildrop_channels:
                        transmitter_item = db_hardware.get_transmitter(
                            session,
                            maildrop_channel.id_transmitter
                        )
                        if not transmitter_item:
                            continue
                        result = pocsag_sender.message_to_air(
                            capcode=maildrop_channel.capcode,
                            fbit=maildrop_channel.id_fbit,
                            freq=transmitter_item.freq,
                            id_baudrate=transmitter_item.id_baudrate,
                            id_codepage=maildrop_channel.id_codepage,
                            message=message_item.message
                        )
                    if not result:
                        LOGGER.error(
                            'Ошибка отправки новостного сообщения id: %s',
                            message_item.uid
                        )
                        continue

                    db_messages.mark_message_sent(session, message_item.uid)


def check_celebrations():
    """Создаём праздничное настроение и формируем поздравительные сообщения"""
    today_date = datetime.date.today()
    with SessionLocal() as session:
        users = db_user.get_users_with_birthday(session)
        for user_item in users:
            datetime_send_after = datetime.datetime(
                year=today_date.year,
                month=today_date.month,
                day=today_date.day,
                hour=random.randint(9, 14),
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
            )

            message_schema_item = MessageSchema(
                uid=None,
                id_message_type=MessageTypeEnum.PRIVATE,
                id_pager=user_item.pagers[0].id,  # только на один пейджер пользователя
                id_group_type=None,
                id_maildrop_type=None,
                message='Поздравляем с днём рождения!!!',  # TODO разные фразы
                sent=None,
                datetime_send_after=datetime_send_after,
                datetime_create=None,
            )

            db_messages.create_message(session, message_schema_item)
