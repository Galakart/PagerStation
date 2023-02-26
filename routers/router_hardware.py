from fastapi import APIRouter, HTTPException, status

import db
from models.model_hardware import PagerSchema, TransmitterSchema

# TODO UUID Primary keys https://fastapi.tiangolo.com/tutorial/extra-data-types/

LIMIT_GET = 50  # TODO вынести во всех роутерах в константы

router = APIRouter(
    prefix="/hardware",
    tags=["hardware"],
)


@router.get("/transmitters", response_model=list[TransmitterSchema])
def transmitters_items_get(skip: int = 0, limit: int = LIMIT_GET):
    """Вывод всех передатчиков"""
    all_transmitters_tuple = db.db_hardware.get_all_transmitters(skip, limit)
    return all_transmitters_tuple


@router.get("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def transmitter_get(id_transmitter: int):
    """Вывод конкретного передатчика"""
    transmitter_item = db.db_hardware.get_transmitter(id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")
    return transmitter_item


@router.post("/transmitters", response_model=TransmitterSchema, status_code=status.HTTP_201_CREATED)
def transmitter_add(transmitter_schema_item: TransmitterSchema):
    """Добавление передатчика"""
    transmitter_item = db.db_hardware.create_transmitter(transmitter_schema_item)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка добавления передатчика")
    return transmitter_item


@router.put("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def transmitter_update(transmitter_schema_item: TransmitterSchema, id_transmitter: int):
    """Редактирование передатчика"""
    transmitter_item = db.db_hardware.get_transmitter(id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")

    transmitter_item = db.db_hardware.update_transmitter(transmitter_schema_item, id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка редактирования передатчика")
    return transmitter_item


@router.delete("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def transmitter_delete(id_transmitter: int):
    """Удаление передатчика"""
    transmitter_item = db.db_hardware.get_transmitter(id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Передатчик не найден")

    result = db.db_hardware.delete_transmitter(id_transmitter)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления передатчика")
    return transmitter_item


@router.get("/pagers", response_model=list[PagerSchema])
def pagers_items_get(skip: int = 0, limit: int = LIMIT_GET):
    """Вывод всех пейджеров"""
    all_pagers_tuple = db.db_hardware.get_all_pagers(skip, limit)
    return all_pagers_tuple


@router.get("/pagers/{id_pager}", response_model=PagerSchema)
def pager_get(id_pager: int):
    """Вывод конкретного пейджера"""
    pager_item = db.db_hardware.get_pager(id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")
    return pager_item


@router.post("/pagers", response_model=PagerSchema, status_code=status.HTTP_201_CREATED)
def pager_add(pager_schema_item: PagerSchema):
    """Добавление пейджера"""
    pager_item = db.db_hardware.create_pager(pager_schema_item)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка добавления пейджера")
    return pager_item


@router.put("/pagers/{id_pager}", response_model=PagerSchema)
def pager_update(pager_schema_item: PagerSchema, id_pager: int):
    """Редактирование пейджера"""
    pager_item = db.db_hardware.get_pager(id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    pager_item = db.db_hardware.update_pager(pager_schema_item, id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка редактирования пейджера")
    return pager_item


@router.delete("/pagers/{id_pager}", response_model=PagerSchema)
def pager_delete(id_pager: int):
    """Удаление пейджера"""
    pager_item = db.db_hardware.get_pager(id_pager)
    if not pager_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пейджер не найден")

    result = db.db_hardware.delete_pager(id_pager)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка удаления пейджера")
    return pager_item
