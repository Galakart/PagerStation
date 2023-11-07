"""Роутер - вспомогательное"""
import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, status

import backend.constants as const
from backend.db.auth import create_access_token
from backend.models.model_user import TokenSchema, User
from backend.routers.dependencies import check_user_credentials_dependency

router = APIRouter()


@router.post("/token/", response_model=TokenSchema)
async def login_for_access_token(user: User = Depends(check_user_credentials_dependency)):
    """Логин и получение токена доступа"""
    if not user.api_login:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    access_token = create_access_token(
        username=user.api_login,
        expires_delta=datetime.timedelta(minutes=const.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/capcode_to_frame/{capcode}")
def capcode_to_frame(capcode: int = Path(ge=1, le=9999999)):
    """Расчёт фрейма для капкода"""
    return {"frame_number": capcode % 8}
