from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src.handlers import open_menu_edit_callback
from src.handlers.previous import previous_callback, previous_callback_message
from src.models.language import Language
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.services.users import set_current_user_language, update_user_info

router = Router()

class UserData(StatesGroup):
    weight = State()
    height = State()

MENU_MAP = {
    MenuButtonTitle.SETTINGS.value: MenuType.SETTINGS,
    MenuButtonTitle.USER_INFO.value: MenuType.USER_INFO,
    MenuButtonTitle.WEIGHT.value: MenuType.WEIGHT,
    MenuButtonTitle.HEIGHT.value: MenuType.HEIGHT,
    MenuButtonTitle.BIRTHDAY.value: MenuType.BIRTHDAY,
    MenuButtonTitle.SEX.value: MenuType.SEX,
    MenuButtonTitle.ACTIVITY.value: MenuType.ACTIVITY,
    MenuButtonTitle.GOAL.value: MenuType.GOAL,
    MenuButtonTitle.LANGUAGE.value: MenuType.LANGUAGE,
}

SEX_LIST = [
    MenuButtonTitle.MALE.value,
    MenuButtonTitle.FEMALE.value,
]

ACTIVITY_LIST = [
    MenuButtonTitle.ACTIVITY_VERY_LOW.value,
    MenuButtonTitle.ACTIVITY_LOW.value,
    MenuButtonTitle.ACTIVITY_MIDDLE.value,
    MenuButtonTitle.ACTIVITY_HIGH.value,
    MenuButtonTitle.ACTIVITY_VERY_HIGH.value,
]

GOAL_LIST = [
    MenuButtonTitle.LOSE_WEIGHT.value,
    MenuButtonTitle.KEEP_WEIGHT.value,
    MenuButtonTitle.GAIN_WEIGHT.value,
]

async def menu_handler(callback: CallbackQuery, state: FSMContext, menu_type: MenuType):
    await open_menu_edit_callback(callback, state, menu_type)
    await callback.answer()

@router.callback_query(F.data.in_(MENU_MAP.keys()))
async def menu_router(callback: CallbackQuery, state: FSMContext):
    if callback.data == MenuButtonTitle.WEIGHT.value:
        await state.set_state(UserData.weight)
    elif callback.data == MenuButtonTitle.HEIGHT.value:
        await state.set_state(UserData.height)

    await menu_handler(callback, state, MENU_MAP[callback.data])

@router.message(UserData.weight)
async def get_weight(message: Message, state: FSMContext):
    await update_user_info(message.from_user.id, weight=message.text)
    await state.set_state(None)
    await previous_callback_message(message, state)

@router.message(UserData.height)
async def get_height(message: Message, state: FSMContext):
    await update_user_info(message.from_user.id, height=message.text)
    await state.set_state(None)
    await previous_callback_message(message, state)

@router.callback_query(F.data.in_(SEX_LIST))
async def update_sex_handler(callback: CallbackQuery, state: FSMContext):
    await update_user_info(callback.from_user.id, sex=MenuButtonTitle(callback.data))
    await previous_callback(callback, state)

@router.callback_query(F.data.in_(ACTIVITY_LIST))
async def update_activity_handler(callback: CallbackQuery, state: FSMContext):
    await update_user_info(callback.from_user.id, activity=MenuButtonTitle(callback.data))
    await previous_callback(callback, state)

@router.callback_query(F.data.in_(GOAL_LIST))
async def update_goal_handler(callback: CallbackQuery, state: FSMContext):
    await update_user_info(callback.from_user.id, goal=MenuButtonTitle(callback.data))
    await previous_callback(callback, state)

@router.callback_query(F.data.in_([Language.UKRAINE.value, Language.ENGLISH.value, Language.GERMAN.value]))
async def change_language(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await set_current_user_language(callback.from_user.id, callback.data)
    await previous_callback(callback, state)
