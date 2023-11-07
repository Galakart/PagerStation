"""Зависимости для роутеров"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.db import auth, db_user
from backend.db.connection import get_session
from backend.models.model_user import User

# TODO повторяющийся код с raise HTTPException


def check_user_credentials_dependency(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
) -> User:
    """Проверка логина-пароля пользователя"""
    user = db_user.get_user_by_login(session=session, api_login=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.api_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректные логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def check_user_token_dependency(
        token: str = Depends(auth.oauth2_scheme),
        session: Session = Depends(get_session)
) -> User:
    """Проверка что токен валидный и пользователь существует"""
    username, is_expired = auth.get_username_from_token(token)
    if is_expired:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Истёк срок действия токена",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен невалидный",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db_user.get_user_by_login(session=session, api_login=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не существует или заблокирован",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
