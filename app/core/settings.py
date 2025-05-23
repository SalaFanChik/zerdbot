# app/core/settings.py

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyHttpUrl
from functools import lru_cache


class Settings(BaseSettings):
    # Telegram
    bot_token: str

    # Database
    database_url: PostgresDsn

    # External service
    access_token: str
    base_domain: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
