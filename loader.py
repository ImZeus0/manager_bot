import asyncio
from aiogram import Bot, Dispatcher
from core.config import get_settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(get_settings().telegram_token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()

