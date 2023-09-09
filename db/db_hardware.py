import logging

from db.connection import Session
from models.model_hardware import (Pager, PagerSchema, Transmitter,
                                   TransmitterSchema)

LOGGER = logging.getLogger('applog')


def get_all_transmitters(skip: int, limit: int) -> tuple[Transmitter]:
    session = Session()
    values_tuple = session.query(Transmitter).offset(skip).limit(limit).all()
    session.close()
    return values_tuple


def get_transmitter(id_transmitter: int) -> Transmitter:
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


def get_all_pagers(skip: int, limit: int) -> tuple[Pager]:
    session = Session()
    values_tuple = session.query(Pager).offset(skip).limit(limit).all()
    session.close()
    return values_tuple


def get_pager(id_pager: int) -> Pager:
    session = Session()
    value = session.query(Pager).get(id_pager)
    session.close()
    return value


def create_pager(pager_schema_item: PagerSchema) -> Pager:
    session = Session()
    try:
        pager_item = Pager(
            id=pager_schema_item.id,
            capcode=pager_schema_item.capcode,
            id_fbit=pager_schema_item.id_fbit.value,
            id_codepage=pager_schema_item.id_codepage.value,
            id_transmitter=pager_schema_item.id_transmitter,
        )
        session.add(pager_item)
        session.commit()
        session.refresh(pager_item)
        return pager_item
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()


def update_pager(pager_schema_item: PagerSchema, id_pager: int) -> Pager:
    session = Session()
    try:
        pager_item = session.query(Pager).get(id_pager)
        if pager_item:
            pager_item.capcode = pager_schema_item.capcode
            pager_item.id_fbit = pager_schema_item.id_fbit.value
            pager_item.id_codepage = pager_schema_item.id_codepage.value
            pager_item.id_transmitter = pager_schema_item.id_transmitter
            session.add(pager_item)
            session.commit()
            session.refresh(pager_item)
        else:
            pager_item = None
        return pager_item
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()


def delete_pager(id_pager: int) -> bool:
    session = Session()
    result = False
    try:
        pager_item = session.query(Pager).get(id_pager)
        if pager_item:
            session.delete(pager_item)
            session.commit()
            result = True
    except Exception as ex:
        LOGGER.error(ex)
    finally:
        session.close()
    return result
