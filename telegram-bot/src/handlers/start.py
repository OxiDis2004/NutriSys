import logging
import uuid

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ErrorEvent

from src.handlers import history_append
from src.models.menu_parts.menu_type import MenuType
from src.utils.menu_builder import MenuFactory

logger = logging.getLogger(__name__)
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    menu = await MenuFactory.build_menu(MenuType.START, state)
    await message.answer(
        text=menu.title,
        reply_markup=menu.keyboard
    )
    await history_append(state, MenuType.START)


@router.message()
async def handle_message(message: Message):
    logger.info(
        "Telegram message received | telegram_id=%s | chat_id=%s",
        message.from_user.id if message.from_user else None,
        message.chat.id
    )


@router.error()
async def global_error_handler(event: ErrorEvent):
    error_id = str(uuid.uuid4())

    logger.exception(
        "Telegram bot error | error_id=%s | update=%s",
        error_id,
        event.update
    )

    return True
