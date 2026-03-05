from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.handlers import open_menu_edit
from src.models.language import Language
from src.models.menu_type import MenuType
from src.models.menu_button_titles import MenuButtonTitle
from src.services.users import set_current_user_language

router = Router()


@router.callback_query(F.data == MenuButtonTitle.SETTINGS.value)
async def settings_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit(callback, state, MenuType.SETTINGS)

@router.callback_query(F.data == MenuButtonTitle.LANGUAGE.value)
async def language_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit(callback, state, MenuType.LANGUAGE)

@router.callback_query(F.data.in_([Language.UKRAINE.value, Language.ENGLISH.value, Language.GERMAN.value]))
async def change_language(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    set_current_user_language(callback.from_user.id, callback.data)
    await open_menu_edit(callback, state, MenuType.SETTINGS)
