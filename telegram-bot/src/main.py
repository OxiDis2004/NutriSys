from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import logging
import os

logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Hello! I am your Aiogram bot 🤖")

@dp.message()
async def echo(message: Message):
    await message.reply(f"You said: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())