"""Класс с конфигурациями из переменных окружения"""
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    owm_token: SecretStr
    owm_latitude: str
    owm_longitude: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()  # type: ignore
