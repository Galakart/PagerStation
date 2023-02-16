import logging

from db.connection import Session
from models.model_hardware import (Pager, PagerSchema, Transmitter,
                                   TransmitterSchema)

LOGGER = logging.getLogger('applog')


def get_all_transmitters(skip: int, limit: int) -> tuple[Transmitter] | None:
    session = Session()
    values_tuple = session.query(Transmitter).offset(skip).limit(limit).all()
    session.close()
    return values_tuple


def get_transmitter(id_transmitter: int) -> Transmitter | None:
    session = Session()
    value = session.query(Transmitter).get(id_transmitter)
    session.close()
    return value


def create_transmitter(transmitter_schema_item: TransmitterSchema) -> Transmitter:
    session = Session()
    try:
        transmitter_item = Transmitter(
            name=transmitter_schema_item.name,
            freq=transmitter_schema_item.freq,
            id_baudrate=transmitter_schema_item.id_baudrate.value
        )
        session.add(transmitter_item)
        session.commit()
        session.refresh(transmitter_item)
        return transmitter_item
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()


def update_transmitter(transmitter_schema_item: TransmitterSchema, id_transmitter: int) -> Transmitter:
    session = Session()
    try:
        transmitter_item = session.query(Transmitter).get(id_transmitter)
        if transmitter_item:
            transmitter_item.name = transmitter_schema_item.name
            transmitter_item.freq = transmitter_schema_item.freq
            transmitter_item.id_baudrate = transmitter_schema_item.id_baudrate.value
            session.add(transmitter_item)
            session.commit()
            session.refresh(transmitter_item)
        else:
            transmitter_item = None
        return transmitter_item
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()


def delete_transmitter(id_transmitter: int) -> bool:
    session = Session()
    result = False
    try:
        transmitter_item = session.query(Transmitter).get(id_transmitter)
        if transmitter_item:
            session.delete(transmitter_item)
            session.commit()
            result = True
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()
    return result


def get_all_pagers():
    session = Session()
    values_tuple = session.query(Pager).all()
    session.close()
    return values_tuple


def get_pager(id_pager: int) -> Pager:
    session = Session()
    value = session.query(Pager).get(id_pager)
    session.close()
    return value
