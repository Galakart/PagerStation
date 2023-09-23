"""Операции с пейджинговыми сообщениями"""
import uuid

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from backend.models.model_messages import Message, MessageSchema


def get_messages(session: Session, offset=None, limit=None):
    result = session.execute(
        select(Message)
        .offset(offset)
        .limit(limit)
    )
    messages = result.scalars().all()
    return messages


def get_message(session: Session, uid_message: uuid.UUID) -> Message:
    message = session.get(Message, uid_message)
    return message


def create_message(session: Session, message_schema_item: MessageSchema) -> Message:
    message = Message(
        uid=uuid.uuid4(),
        id_message_type=message_schema_item.id_message_type.value,
        id_pager=message_schema_item.id_pager,
        id_group_type=message_schema_item.id_group_type.value if message_schema_item.id_group_type else None,
        id_maildrop_type=message_schema_item.id_maildrop_type.value if message_schema_item.id_maildrop_type else None,
        message=message_schema_item.message,
        datetime_send_after=message_schema_item.datetime_send_after,
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def delete_message(session: Session, uid_message: uuid.UUID) -> bool:
    result = False
    message = session.get(Message, uid_message)
    # TODO выдавать ошибку если сообщение уже отправлено
    if message and not message.sent:
        session.delete(message)
        session.commit()
        result = True
    return result


def get_unsent_messages(session: Session, id_message_type: int):
    result = session.execute(
        select(Message)
        .where(
            and_(
                Message.id_message_type == id_message_type,
                Message.sent == False,
            )
        )
        .limit(5)
    )
    messages = result.scalars().all()
    return messages


def mark_message_sent(session: Session, uid_message: uuid.UUID) -> bool:
    result = False
    message = session.get(Message, uid_message)
    if message:
        message.sent = True
        session.add(message)
        session.commit()
        result = True
    return result


# def get_maildrop_channels_by_type(id_maildrop_type: int) -> MailDropChannels:
#     session = Session()
#     values_tuple = session.query(MailDropChannels).filter(MailDropChannels.id_maildrop_type == id_maildrop_type).all()
#     session.close()
#     return values_tuple


# def get_last_sent_maildrop_by_type(id_maildrop_type: int) -> MessageMailDrop:
#     """Последнее отправленное MailDrop-сообщение"""
#     session = Session()
#     value = session.query(MessageMailDrop).filter(MessageMailDrop.id_maildrop_type ==
#                                                   id_maildrop_type).order_by(desc(MessageMailDrop.id)).first()
#     session.close()
#     return value


# def get_rss_feed_by_maildrop_type(id_maildrop_type: int) -> RssFeed:
#     """Возвращает RSS-ленту, связанную с этим id_maildrop_type """
#     session = Session()
#     value = session.query(RssFeed).filter(RssFeed.id_maildrop_type == id_maildrop_type).first()
#     session.close()
#     return value
