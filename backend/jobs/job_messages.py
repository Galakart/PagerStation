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
        messages_tuple = db_messages.get_unsent_messages(session)
        for message_item in messages_tuple:

            if message_item.id_message_type == MessageTypeEnum.PRIVATE.value:
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
                else:
                    LOGGER.error(f'Ошибка отправки личного сообщения id:{message_item.uid}')

            elif message_item.id_message_type == MessageTypeEnum.GROUP.value:
                group_channels_tuple = db_channels.get_group_channels_by_type(session, message_item.id_group_type)
                if not group_channels_tuple:
                    LOGGER.warning(f'Есть групповые сообщения для отправки, но нету доступных групповых каналов')
                    continue

                result = False
                for group_channel in group_channels_tuple:
                    transmitter_item = db_hardware.get_transmitter(session, group_channel.id_transmitter)
                    result = pocsag_sender.message_to_air(
                        capcode=group_channel.capcode,
                        fbit=group_channel.id_fbit,
                        freq=transmitter_item.freq,
                        id_baudrate=transmitter_item.id_baudrate,
                        id_codepage=group_channel.id_codepage,
                        message=message_item.message
                    )
                if result:
                    db_messages.mark_message_sent(session, message_item.uid)
                else:
                    LOGGER.error(f'Ошибка отправки группового сообщения id:{message_item.uid}')

            elif message_item.id_message_type == MessageTypeEnum.MAILDROP.value:
                maildrop_channels_tuple = db_channels.get_maildrop_channels_by_type(session, message_item.id_maildrop_type)
                if not maildrop_channels_tuple:
                    LOGGER.warning(f'Есть maildrop сообщения для отправки, но нету доступных maildrop каналов')
                    continue

                result = False
                for maildrop_channel in maildrop_channels_tuple:
                    transmitter_item = db_hardware.get_transmitter(session, maildrop_channel.id_transmitter)
                    result = pocsag_sender.message_to_air(
                        capcode=maildrop_channel.capcode,
                        fbit=maildrop_channel.id_fbit,
                        freq=transmitter_item.freq,
                        id_baudrate=transmitter_item.id_baudrate,
                        id_codepage=maildrop_channel.id_codepage,
                        message=message_item.message
                    )
                if result:
                    db_messages.mark_message_sent(session, message_item.uid)
                else:
                    LOGGER.error(f'Ошибка отправки новостного сообщения id:{message_item.uid}')


def check_celebrations():
    """Создаём праздничное настроение и формируем поздравительные сообщения"""
    today_date = datetime.date.today()
    with SessionLocal() as session:
        users_tuple = db_user.get_users_with_birthday(session)
        for user_item in users_tuple:
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
                id_pager=user_item.pagers[0].id,  # отправим поздравление только на один пейджер пользователя
                id_group_type=None,
                id_maildrop_type=None,
                message='Поздравляем с днём рождения!!!',  # TODO разные фразы
                sent=None,
                datetime_send_after=datetime_send_after,
                datetime_create=None,
            )

            db_messages.create_message(session, message_schema_item)
