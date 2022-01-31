from loader import bot, storage , loop
import logging
from db.base import database

async def on_startup(dp):
    await database.connect()


async def on_shutdown(dp):
    await bot.close()
    await database.disconnect()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    print('Start')


    logger = logging.getLogger("manager_bot")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("manager_log.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    executor.start_polling(dp,loop=loop,on_shutdown=on_shutdown,on_startup=on_startup)
    logger.info("Program started")