from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.handlers import open_menu_edit_callback
from src.handlers.previous import go_back
from src.models.menu_parts.menu_title import MenuTitle
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.unit import Unit
from src.services.food import food_add_request
from src.utils import translate

router = Router()


@router.callback_query(F.data == MenuButtonTitle.FOOD.value)
async def food_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await open_menu_edit_callback(callback, state, MenuType.FOOD)

@router.callback_query(F.photo)
async def sent_photo(message: Message, state: FSMContext):
    food_response = await food_add_request(state, message.photo[-1])
    translated_text = await translate(state, MenuTitle.FOOD_RESPONSE)
    translated_kcal = await translate(state, Unit.KCAL)
    translated_g = await translate(state, Unit.GRAM)
    text = translated_text.format(**food_response.get("statistic", None), u_kcal=translated_kcal,u_g=translated_g)
    await go_back(message, state, text=text, new_message=True)