from models.common import (ROLES, MailDropChannels, MessageMailDrop,
                           MessagePrivate, Pager, ServiceRole, User)
from sqlalchemy import desc

from db.connection import Session

# TODO в Users добавить поле active
# TODO у MessagePrivate и MessageMailDrop объединить похожие методы


def get_admins():
    """Все админы"""
    session = Session()
    values_tuple = session.query(User).join(ServiceRole, ServiceRole.id_user == User.id).filter(
        ServiceRole.id_role == ROLES['admin']).all()  # TODO ... Users.active==1
    session.close()
    return values_tuple


def create_message_private(id_pager: int, message: str) -> bool:
    session = Session()
    new_item = MessagePrivate(
        id_pager=id_pager,
        message=message
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


def get_last_sent_maildrop_by_type(id_maildrop_type: int) -> MessageMailDrop:
    """Последнее отправленное MailDrop-сообщение"""
    session = Session()
    value = session.query(MessageMailDrop).filter(MessageMailDrop.id_maildrop_type ==
                                                  id_maildrop_type).order_by(desc(MessageMailDrop.id)).first()
    session.close()
    return value


def get_classifier_items(model, is_reverse=False):
    """Весь классификатор по названию модели"""
    session = Session()
    if hasattr(model, 'active'):
        if is_reverse:
            values_tuple = session.query(model).filter(model.active == 1).order_by(desc(model.id)).all()
        else:
            values_tuple = session.query(model).filter(model.active == 1).order_by(model.id).all()
    else:
        if is_reverse:  # TODO повторяющийся код
            values_tuple = session.query(model).order_by(desc(model.id)).all()
        else:
            values_tuple = session.query(model).order_by(model.id).all()
    session.close()
    return values_tuple


def find_classifier_object(model, id=None, name=None):
    """Поиск объекта в классификаторе по его id или имени"""
    session = Session()
    if hasattr(model, 'active'):
        if id:
            item = session.query(model).filter(model.id == id, model.active == 1).first()
        elif name:
            item = session.query(model).filter(model.name == name, model.active == 1).first()
        else:
            item = None
    else:
        if id:
            item = session.query(model).get(id)
        elif name:
            item = session.query(model).filter(model.name == name).first()
        else:
            item = None
    session.close()
    return item


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


def get_maildrop_channels_by_type(id_maildrop_type: int) -> MailDropChannels:
    session = Session()
    values_tuple = session.query(MailDropChannels).filter(MailDropChannels.id_maildrop_type == id_maildrop_type).all()
    session.close()
    return values_tuple


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


def get_user_pagers(id_user: int) -> Pager:  # TODO many-to-many
    session = Session()
    user = session.query(User).get(id_user)
    pagers = None
    if user:
        pagers = user.pagers
    session.close()
    return pagers


def get_pager(id_pager: int) -> Pager:
    session = Session()
    value = session.query(Pager).get(id_pager)
    session.close()
    return value
