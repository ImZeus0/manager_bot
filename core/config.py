TOKEN = '1655901681:AAGL13xkvRHqYVr6sjQQrQLu8bWvRnSgpp8'


CHAT_ID = -690591344

import os
from functools import lru_cache
from pydantic import BaseSettings, RedisDsn
from os.path import join


class Settings(BaseSettings):
    telegram_token: str
    database_url:str
    admin:int

    class Config:
        env_file = join(os.getcwd(), 'core/config.env')
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
