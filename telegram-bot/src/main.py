from aiogram import Bot, Dispatcher
import asyncio
import logging
import os
from src.routers import setup_routers
from src.services import get_hostname

logging.basicConfig(level=logging.INFO)
# my_setenv.get_key()
get_hostname()

async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    setup_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())