from aiogram import Bot, Dispatcher
import asyncio
import logging
import os

from src import my_setenv
from src.handlers.authmiddleware import AuthMiddleware
from src.routers import setup_routers
from src.services import get_hostname, initialize_client

logging.basicConfig(level=logging.INFO)
my_setenv.get_key()

async def main():
    get_hostname()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    initialize_client()
    setup_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())