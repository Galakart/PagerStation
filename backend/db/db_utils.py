


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
