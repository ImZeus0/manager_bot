import asyncio
import logging

from aiogram import Bot, Dispatcher
from core.config import get_settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.ERROR,filename='bot_error.log')

bot = Bot(get_settings().telegram_token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
loop = asyncio.get_event_loop()

