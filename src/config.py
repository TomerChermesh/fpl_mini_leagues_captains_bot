import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings


class Config(BaseSettings):
    telegram_bot_token: str

    class Config:
        load_dotenv()
        telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')


@lru_cache()
def get_config():
    return Config()
