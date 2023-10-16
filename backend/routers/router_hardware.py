"""Роутер - оборудование"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_hardware
from backend.db.connection import get_session
from backend.models.model_hardware import PagerSchema, TransmitterSchema

router = APIRouter(
    prefix="/hardware",
    tags=["hardware"],
)


@router.get("/transmitters/", response_model=list[TransmitterSchema])
def get_transmitters(session: Session = Depends(get_session)):
    """Вывод всех передатчиков"""
    transmitters = db_hardware.get_transmitters(session)
    return transmitters


@router.get("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def get_transmitter(id_transmitter: int, session: Session = Depends(get_session)):
    """Вывод конкретного передатчика"""
    transmitter_item = db_hardware.get_transmitter(session, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")
    return transmitter_item


@router.post("/transmitters/", response_model=TransmitterSchema,
             status_code=status.HTTP_201_CREATED)
def create_transmitter(
    transmitter_schema_item: TransmitterSchema,
    session: Session = Depends(get_session)
):
    """Добавление передатчика"""
    transmitter_item = db_hardware.create_transmitter(session, transmitter_schema_item)
    if not transmitter_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка добавления передатчика"
        )
    return transmitter_item


@router.put("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def update_transmitter(
    id_transmitter: int,
    transmitter_schema_item:
    TransmitterSchema, session:
    Session = Depends(get_session)
):
    """Редактирование передатчика"""
    transmitter_item = db_hardware.get_transmitter(session, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")

    transmitter_item = db_hardware.update_transmitter(
        session,
        id_transmitter,
        transmitter_schema_item
    )
    if not transmitter_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка редактирования передатчика"
        )
    return transmitter_item


@router.delete("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def delete_transmitter(id_transmitter: int, session: Session = Depends(get_session)):
    """Удаление передатчика"""
    transmitter_item = db_hardware.get_transmitter(session, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")

    result = db_hardware.delete_transmitter(session, id_transmitter)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления передатчика"
        )
    return transmitter_item


@router.get("/pagers/", response_model=list[PagerSchema])
def get_pagers(
    offset: int = 0,
    limit: int = const.LIMIT_GET,
    session: Session = Depends(get_session)
):
    """Вывод всех пейджеров"""
    pagers = db_hardware.get_pagers(session, offset, limit)
    return pagers


@router.get("/pagers/{id_pager}", response_model=PagerSchema)
def get_pager(id_pager: int, session: Session = Depends(get_session)):
    """Вывод конкретного пейджера"""
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пейджер не найден"
        )
    return pager_item


@router.post("/pagers/", response_model=PagerSchema, status_code=status.HTTP_201_CREATED)
def create_pager(pager_schema_item: PagerSchema, session: Session = Depends(get_session)):
    """Добавление пейджера"""
    pager_item = db_hardware.create_pager(session, pager_schema_item)
    if not pager_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка добавления пейджера"
        )
    return pager_item


@router.put("/pagers/{id_pager}", response_model=PagerSchema)
def update_pager(
    id_pager: int,
    pager_schema_item: PagerSchema,
    session: Session = Depends(get_session)
):
    """Редактирование пейджера"""
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    pager_item = db_hardware.update_pager(session, id_pager, pager_schema_item)
    if not pager_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка редактирования пейджера"
        )
    return pager_item


@router.delete("/pagers/{id_pager}", response_model=PagerSchema)
def delete_pager(id_pager: int, session: Session = Depends(get_session)):
    """Удаление пейджера"""
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    result = db_hardware.delete_pager(session, id_pager)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления пейджера"
        )
    return pager_item
