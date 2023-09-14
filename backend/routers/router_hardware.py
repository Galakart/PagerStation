from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_hardware
from backend.db.connection import get_session
from backend.models.model_hardware import PagerSchema, TransmitterSchema

# TODO UUID Primary keys https://fastapi.tiangolo.com/tutorial/extra-data-types/

LIMIT_GET = 50  # TODO вынести во всех роутерах в константы

router = APIRouter(
    prefix="/hardware",
    tags=["hardware"],
)


@router.get("/transmitters/", response_model=list[TransmitterSchema])
def get_transmitters(session: Session = Depends(get_session), offset: int = 0, limit: int = const.LIMIT_GET):
    """Вывод всех передатчиков"""
    transmitters_tuple = db_hardware.get_transmitters(session, offset, limit)
    return transmitters_tuple


@router.get("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def get_transmitter(session: Session = Depends(get_session), id_transmitter: int = 0):
    """Вывод конкретного передатчика"""
    transmitter_item = db_hardware.get_transmitter(session, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")
    return transmitter_item


@router.post("/transmitters/", response_model=TransmitterSchema, status_code=status.HTTP_201_CREATED)
def create_transmitter(session: Session = Depends(get_session), transmitter_schema_item: TransmitterSchema = None):
    """Добавление передатчика"""
    transmitter_item = db_hardware.create_transmitter(session, transmitter_schema_item)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка добавления передатчика")
    return transmitter_item


@router.put("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def update_transmitter(session: Session = Depends(get_session), id_transmitter: int = 0, transmitter_schema_item: TransmitterSchema = None):
    """Редактирование передатчика"""
    transmitter_item = db_hardware.get_transmitter(session, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")

    transmitter_item = db_hardware.update_transmitter(session, id_transmitter, transmitter_schema_item)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка редактирования передатчика")
    return transmitter_item


@router.delete("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def delete_transmitter(session: Session = Depends(get_session), id_transmitter: int = 0):
    """Удаление передатчика"""
    transmitter_item = db_hardware.get_transmitter(session, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")

    result = db_hardware.delete_transmitter(session, id_transmitter)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления передатчика")
    return transmitter_item


@router.get("/pagers/", response_model=list[PagerSchema])
def get_pagers(session: Session = Depends(get_session), offset: int = 0, limit: int = const.LIMIT_GET):
    """Вывод всех пейджеров"""
    pagers_tuple = db_hardware.get_pagers(session, offset, limit)
    return pagers_tuple


@router.get("/pagers/{id_pager}", response_model=PagerSchema)
def get_pager(session: Session = Depends(get_session), id_pager: int = 0):
    """Вывод конкретного пейджера"""
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")
    return pager_item


@router.post("/pagers/", response_model=PagerSchema, status_code=status.HTTP_201_CREATED)
def create_pager(session: Session = Depends(get_session), pager_schema_item: PagerSchema = None):
    """Добавление пейджера"""
    pager_item = db_hardware.create_pager(session, pager_schema_item)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка добавления пейджера")
    return pager_item


@router.put("/pagers/{id_pager}", response_model=PagerSchema)
def update_pager(session: Session = Depends(get_session), id_pager: int = 0, pager_schema_item: PagerSchema = None):
    """Редактирование пейджера"""
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    pager_item = db_hardware.update_pager(session, id_pager, pager_schema_item)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка редактирования пейджера")
    return pager_item


@router.delete("/pagers/{id_pager}", response_model=PagerSchema)
def delete_pager(session: Session = Depends(get_session), id_pager: int = 0):
    """Удаление пейджера"""
    pager_item = db_hardware.get_pager(session, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    result = db_hardware.delete_pager(session, id_pager)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления пейджера")
    return pager_item
