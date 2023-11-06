"""Роутер - вспомогательное"""
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import backend.constants as const
from backend.db import db_user
from backend.db.auth import create_access_token
from backend.db.connection import get_session
from backend.models.model_user import TokenSchema

router = APIRouter()


@router.post("/token/", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    """Логин и получение токена доступа"""
    user = db_user.authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.api_login},
        expires_delta=datetime.timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/capcode_to_frame/{capcode}")
def capcode_to_frame(capcode: int = Path(ge=1, le=9999999)):
    """Расчёт фрейма для капкода"""
    return {"frame_number": capcode % 8}
