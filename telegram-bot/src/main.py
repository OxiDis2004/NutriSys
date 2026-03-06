from aiogram import Bot, Dispatcher
import asyncio
import logging
import os
import my_setenv
from src.routers import setup_routers

logging.basicConfig(level=logging.INFO)
my_setenv.get_key()

async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    setup_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())