"""Класс с конфигурациями из переменных окружения"""
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """Класс для доступа к переменным окружения"""
    owm_token: SecretStr
    owm_latitude: str
    owm_longitude: str

    class Config:
        """Переменные окружения загружаются из файла .env в корне проекта"""
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()  # type: ignore
