from fastapi import APIRouter, HTTPException, status

import db
from models.model_hardware import PagerSchema, TransmitterSchema

# UUID Primary keys https://fastapi.tiangolo.com/tutorial/extra-data-types/

LIMIT_GET = 50

router = APIRouter(
    prefix="/hardware",
    tags=["hardware"],
)


@router.get("/transmitters", response_model=list[TransmitterSchema])
def transmitters_items(skip: int = 0, limit: int = LIMIT_GET):
    """Вывод всех передатчиков"""
    all_transmitters_tuple = db.db_hardware.get_all_transmitters(skip, limit)
    return all_transmitters_tuple


@router.get("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def transmitter(id_transmitter: int):
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
