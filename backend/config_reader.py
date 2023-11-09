"""Класс с конфигурациями из переменных окружения"""
from pydantic import BaseSettings, SecretStr

# pylint: disable=too-few-public-methods


class Settings(BaseSettings):
    """Класс для доступа к переменным окружения"""
    OWM_TOKEN: SecretStr
    OWM_LATITUDE: str
    OWM_LONGITUDE: str
    SECRET_KEY: str

    class Config:
        """Переменные окружения загружаются из файла .env в корне проекта"""
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()  # type: ignore
