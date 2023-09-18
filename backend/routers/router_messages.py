from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_hardware
from backend.db.connection import get_session
from backend.models.model_hardware import PagerSchema, TransmitterSchema

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)
