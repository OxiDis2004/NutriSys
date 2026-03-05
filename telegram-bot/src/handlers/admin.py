from aiogram import Router
from aiogram.types import Message

ADMINS = [123456789]

router = Router()


@router.message(lambda message: message.from_user.id in ADMINS)
async def admin_panel(message: Message):
    await message.answer("Admin panel opened")