"""Класс с конфигурациями из переменных окружения"""
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс для доступа к переменным окружения"""
    owm_token: SecretStr
    owm_latitude: str
    owm_longitude: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()  # type: ignore
