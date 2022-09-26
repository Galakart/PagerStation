from models.model_pagers import Pager

from db.connection import Session


def get_pager(id_pager: int) -> Pager:
    session = Session()
    value = session.query(Pager).get(id_pager)
    session.close()
    return value
