import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from src.handlers.authmiddleware import AuthMiddleware
from src.routers import setup_routers
from src.services import get_hostname, initialize_client
from src.utils.logger import setup_logger

logger = logging.getLogger(__name__)


def get_token():
    return os.getenv("TELEGRAM_BOT_TOKEN", "")


def create_dispatcher():
    dp = Dispatcher()
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    return dp


async def main():
    bot = Bot(token=get_token())
    setup_logger()

    logger.info("Starting telegram bot")
    logger.info("Server host: %s", get_hostname())

    dp = create_dispatcher()

    initialize_client()
    setup_routers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())