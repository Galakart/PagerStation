"""БД - вспомогательное"""
import datetime

from sqlalchemy.orm import Session

from backend.models.model_utils import StrictsIPaddress


def get_stricts_ipaddress(session: Session, ip_address: str) -> StrictsIPaddress:
    """Возвращает объект ip-адреса ограничений, если такой есть в БД"""
    ip_address_item = session.get(StrictsIPaddress, ip_address)
    return ip_address_item


def create_or_update_stricts_ipaddress(session: Session, ip_address: str) -> bool:
    """Создать или обновить ip-адрес ограничений"""
    ip_address_item = session.get(StrictsIPaddress, ip_address)
    if ip_address_item:
        ip_address_item.last_send = datetime.datetime.now()
    else:
        ip_address_item = StrictsIPaddress(
            ip_address=ip_address,
            last_send=datetime.datetime.now()
        )
    session.add(ip_address_item)
    session.commit()
    return True
