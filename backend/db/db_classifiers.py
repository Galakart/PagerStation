"""Классификаторы (т.е. словари констант в БД)"""
from sqlalchemy import desc

from db.connection import Session


def get_classifier_items(model, is_reverse=False):
    """Весь классификатор по названию модели"""
    session = Session()
    if hasattr(model, 'active'):
        values_tuple = session.query(model).filter(model.active == 1).order_by(desc(model.id) if is_reverse else model.id).all()
    else:
        values_tuple = session.query(model).order_by(desc(model.id) if is_reverse else model.id).all()
    session.close()
    return values_tuple


def find_classifier_object(model, id_item=None, name=None):
    """Поиск объекта в классификаторе по его id или имени"""
    session = Session()
    item = None
    if hasattr(model, 'active'):
        if id_item:
            item = session.query(model).filter(model.id == id_item, model.active == 1).first()
        elif name:
            item = session.query(model).filter(model.name == name, model.active == 1).first()
    else:
        if id_item:
            item = session.query(model).get(id_item)
        elif name:
            item = session.query(model).filter(model.name == name).first()
    session.close()
    return item
