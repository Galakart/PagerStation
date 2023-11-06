"""JWT авторизация"""
import datetime

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

import backend.constants as const
from backend.config_reader import config as appconf

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


def get_username_from_token(token: str) -> str | None:
    """Вытащить логин пользователя из содержимого токена"""
    try:
        payload = jwt.decode(token, appconf.SECRET_KEY, algorithms=[const.TOKEN_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    """Создать токен доступа"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now() + expires_delta
    else:
        expire = datetime.datetime.now() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, appconf.SECRET_KEY, algorithm=const.TOKEN_ALGORITHM)
    return encoded_jwt
