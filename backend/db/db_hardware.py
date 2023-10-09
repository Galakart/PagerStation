"""БД - оборудование"""
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.model_hardware import (Pager, PagerSchema, Transmitter,
                                           TransmitterSchema)

LOGGER = logging.getLogger('applog')


def get_transmitters(session: Session, offset=None, limit=None):
    """Все передатчики"""
    result = session.execute(
        select(Transmitter)
        .offset(offset)
        .limit(limit)
    )
    transmitters = result.scalars().all()
    return transmitters


def get_transmitter(session: Session, id_transmitter: int) -> Transmitter:
    """Передатчик по id"""
    transmitter = session.get(Transmitter, id_transmitter)
    return transmitter


def create_transmitter(session: Session, transmitter_schema_item: TransmitterSchema) -> Transmitter:
    """Создать передатчик"""
    transmitter = Transmitter(
        name=transmitter_schema_item.name,
        freq=transmitter_schema_item.freq,
        id_baudrate=transmitter_schema_item.id_baudrate.value
    )
    session.add(transmitter)
    session.commit()
    session.refresh(transmitter)
    return transmitter


def update_transmitter(
        session: Session,
        id_transmitter: int,
        transmitter_schema_item: TransmitterSchema
) -> Transmitter:
    """Изменить передатчик"""
    transmitter = session.get(Transmitter, id_transmitter)
    if transmitter:
        transmitter.name = transmitter_schema_item.name
        transmitter.freq = transmitter_schema_item.freq
        transmitter.id_baudrate = transmitter_schema_item.id_baudrate.value

        session.add(transmitter)
        session.commit()
        session.refresh(transmitter)
    return transmitter


def delete_transmitter(session: Session, id_transmitter: int) -> bool:
    """Удалить передатчик"""
    result = False
    transmitter = session.get(Transmitter, id_transmitter)
    if transmitter:
        session.delete(transmitter)
        session.commit()
        result = True
    return result


def get_pagers(session: Session, offset=None, limit=None):
    """Все пейджеры"""
    result = session.execute(
        select(Pager)
        .offset(offset)
        .limit(limit)
    )
    pagers = result.scalars().all()
    return pagers


def get_pager(session: Session, id_pager: int) -> Pager:
    """Пейджер по его абонентскому номеру"""
    pager = session.get(Pager, id_pager)
    return pager


def create_pager(session: Session, pager_schema_item: PagerSchema) -> Pager:
    """Создать пейджер"""
    pager = Pager(
        id=pager_schema_item.id,
        capcode=pager_schema_item.capcode,
        id_fbit=pager_schema_item.id_fbit.value,
        id_codepage=pager_schema_item.id_codepage.value,
        id_transmitter=pager_schema_item.id_transmitter,
    )
    session.add(pager)
    session.commit()
    session.refresh(pager)
    return pager


def update_pager(session: Session, id_pager: int, pager_schema_item: PagerSchema) -> Pager:
    """Изменить пейджер"""
    pager = session.get(Pager, id_pager)
    if pager:
        pager.capcode = pager_schema_item.capcode
        pager.id_fbit = pager_schema_item.id_fbit.value
        pager.id_codepage = pager_schema_item.id_codepage.value
        pager.id_transmitter = pager_schema_item.id_transmitter

        session.add(pager)
        session.commit()
        session.refresh(pager)
    return pager


def delete_pager(session: Session, id_pager: int) -> bool:
    """Удалить пейджер"""
    result = False
    pager = session.get(Pager, id_pager)
    if pager:
        session.delete(pager)
        session.commit()
        result = True
    return result
