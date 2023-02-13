from fastapi import APIRouter, HTTPException, status

import db
from models.model_hardware import PagerSchema, TransmitterSchema

# TODO paginator https://fastapi.tiangolo.com/tutorial/query-params/
# TODO Data and error validation, try-catch, html response codes
# TODO UUID Primary keys

router = APIRouter(
    prefix="/hardware",
    tags=["hardware"],
)


@router.get("/transmitters", response_model=list[TransmitterSchema])
def transmitters_items():
    all_transmitters_tuple = db.db_hardware.get_all_transmitters()
    return all_transmitters_tuple


@router.get("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def transmitter(id_transmitter: int):
    transmitter_item = db.db_hardware.get_transmitter(id_transmitter)
    if not transmitter_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transmitter item not found")
    return transmitter_item


@router.post("/transmitters", response_model=TransmitterSchema, status_code=status.HTTP_201_CREATED)
def transmitter_add(transmitter_schema_item: TransmitterSchema):
    transmitter_item = db.db_hardware.create_transmitter(transmitter_schema_item)
    # if not transmitter_item:
    #     raise HTTPException(status_code=400, detail="No data")
    return transmitter_item


@router.put("/transmitters/{id_transmitter}", response_model=TransmitterSchema)
def transmitter_update(transmitter_schema_item: TransmitterSchema, id_transmitter: int):
    transmitter_item = db.db_hardware.update_transmitter(transmitter_schema_item, id_transmitter)
    # if not transmitter_item:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return transmitter_item


@router.delete("/transmitters/{id_transmitter}")
def transmitter_delete(id_transmitter: int):
    result = db.db_hardware.delete_transmitter(id_transmitter)
    # if not transmitter_item:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return {"status": "success"}
