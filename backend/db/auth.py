"""JWT авторизация"""
import datetime
import logging

from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

import backend.constants as const
from backend.config_reader import config as appconf

LOGGER = logging.getLogger()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/")


def verify_password(plain_password, hashed_password):
    """Сравнение обычного и хешированного паролей"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str | None) -> str | None:
    """Хэширование пароля"""
    if password:
        return pwd_context.hash(password)
    return None


def create_access_token(username: str, expires_delta: datetime.timedelta):
    """Создать токен доступа"""
    expire = datetime.datetime.utcnow() + expires_delta

    data = {}
    data["sub"] = username
    data["exp"] = expire
    encoded_jwt = jwt.encode(data, appconf.SECRET_KEY, algorithm=const.TOKEN_ALGORITHM)
    return encoded_jwt


def get_username_from_token(token: str) -> tuple[str | None, bool]:
    """Вытащить логин пользователя из токена и проверить срок действия"""
    is_expired = False
    username = None
    try:
        payload = jwt.decode(token, appconf.SECRET_KEY, algorithms=[const.TOKEN_ALGORITHM])
        username = payload.get("sub")
    except ExpiredSignatureError:
        is_expired = True
    except JWTError as ex:
        LOGGER.error(ex, exc_info=True)

    return (username, is_expired)
