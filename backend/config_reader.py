"""Класс с конфигурациями из переменных окружения"""
from pydantic import BaseSettings, Extra, SecretStr


class Settings(BaseSettings, extra=Extra.ignore):
    owm_token: SecretStr
    owm_latitude: str
    owm_longitude: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()  # type: ignore
