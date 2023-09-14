"""Операции с пейджинговыми сообщениями"""
import datetime

from sqlalchemy import desc

from db.connection import Session
from models.model_messages import (MailDropChannels, MessageMailDrop,
                                   MessagePrivate, RssFeed, StrictsIPaddress)

# TODO у MessagePrivate и MessageMailDrop объединить похожие методы


def create_message_private(id_pager: int, message: str, datetime_send_after: datetime.datetime = None) -> bool:
    session = Session()
    new_item = MessagePrivate(
        id_pager=id_pager,
        message=message,
        datetime_send_after=datetime_send_after,
    )
    session.add(new_item)
    session.commit()
    session.close()
    return True


def create_message_maildrop(id_maildrop_type: int, message: str) -> bool:
    session = Session()
    new_item = MessageMailDrop(
        id_maildrop_type=id_maildrop_type,
        message=message
    )
    session.add(new_item)
    session.commit()
    session.close()
    return True


def mark_message_private_sent(id_message_private: int) -> bool:
    """Отметить - приватное сообщение отправлено"""
    session = Session()
    message_item = session.query(MessagePrivate).get(id_message_private)
    if message_item:
        message_item.sent = 1
        session.add(message_item)
        session.commit()
    session.close()
    return True


def mark_message_maildrop_sent(id_message_maildrop: int) -> bool:
    """Отметить - maildrop сообщение отправлено"""
    session = Session()
    message_item = session.query(MessageMailDrop).get(id_message_maildrop)
    if message_item:
        message_item.sent = 1
        session.add(message_item)
        session.commit()
    session.close()
    return True


def get_unsent_messages_private():
    session = Session()
    values_tuple = session.query(MessagePrivate).filter(MessagePrivate.sent == 0).limit(10).all()
    session.close()
    return values_tuple


def get_unsent_messages_maildrop():
    session = Session()
    values_tuple = session.query(MessageMailDrop).filter(MessageMailDrop.sent == 0).limit(10).all()
    session.close()
    return values_tuple


def get_maildrop_channels_by_type(id_maildrop_type: int) -> MailDropChannels:
    session = Session()
    values_tuple = session.query(MailDropChannels).filter(MailDropChannels.id_maildrop_type == id_maildrop_type).all()
    session.close()
    return values_tuple


def get_last_sent_maildrop_by_type(id_maildrop_type: int) -> MessageMailDrop:
    """Последнее отправленное MailDrop-сообщение"""
    session = Session()
    value = session.query(MessageMailDrop).filter(MessageMailDrop.id_maildrop_type ==
                                                  id_maildrop_type).order_by(desc(MessageMailDrop.id)).first()
    session.close()
    return value


def get_rss_feed_by_maildrop_type(id_maildrop_type: int) -> RssFeed:
    """Возвращает RSS-ленту, связанную с этим id_maildrop_type """
    session = Session()
    value = session.query(RssFeed).filter(RssFeed.id_maildrop_type == id_maildrop_type).first()
    session.close()
    return value


def get_stricts_ipaddress(ip_address: str) -> StrictsIPaddress:
    """Возвращает объект ip-адреса ограничений, если такой есть в БД"""
    session = Session()
    value = session.query(StrictsIPaddress).get(ip_address)
    session.close()
    return value


def create_or_update_stricts_ipaddress(ip_address: str) -> bool:
    session = Session()
    ipaddress_item = session.query(StrictsIPaddress).get(ip_address)
    if ipaddress_item:
        ipaddress_item.last_send = datetime.datetime.now()
    else:
        ipaddress_item = StrictsIPaddress(
            ip_address=ip_address,
            last_send=datetime.datetime.now()
        )
    session.add(ipaddress_item)
    session.commit()
    session.close()
    return True