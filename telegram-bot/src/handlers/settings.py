from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src.handlers import open_menu_edit_callback, Event
from src.handlers.previous import go_back
from src.models.activity import Activity
from src.models.goal import Goal
from src.models.menu_parts.menu_type import MenuType
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.sex import Sex
from src.services.settings import set_current_language, new_update_user_info

router = Router()

class UserData(StatesGroup):
    weight = State()
    height = State()
    birthday = State()
    sex = State()
    activity = State()
    goal = State()
    language = State()

MENU_CONFIG = {
    MenuButtonTitle.SETTINGS.value: (MenuType.SETTINGS, None),
    MenuButtonTitle.USER_INFO.value: (MenuType.USER_INFO, None),
    MenuButtonTitle.WEIGHT.value: (MenuType.WEIGHT, UserData.weight),
    MenuButtonTitle.HEIGHT.value: (MenuType.HEIGHT, UserData.height),
    MenuButtonTitle.BIRTHDAY.value: (MenuType.BIRTHDAY, UserData.birthday),
    MenuButtonTitle.SEX.value: (MenuType.SEX, UserData.sex),
    MenuButtonTitle.ACTIVITY.value: (MenuType.ACTIVITY, UserData.activity),
    MenuButtonTitle.GOAL.value: (MenuType.GOAL, UserData.goal),
    MenuButtonTitle.LANGUAGE.value: (MenuType.LANGUAGE, UserData.language),
}

async def menu_handler(callback: CallbackQuery, state: FSMContext, menu_type: MenuType):
    await open_menu_edit_callback(callback, state, menu_type)
    await callback.answer()

@router.callback_query(F.data.in_(MENU_CONFIG.keys()))
async def menu_router(callback: CallbackQuery, state: FSMContext):
    menu_type, user_state = MENU_CONFIG[callback.data]
    if user_state:
        await state.set_state(user_state)
    await menu_handler(callback, state, menu_type)

async def update_handler(event: Event, state: FSMContext, **kwargs):
    success = await new_update_user_info(state, **kwargs)
    if not success:
        return

    await state.set_state()
    await go_back(event, state)

@router.message(UserData.weight)
async def get_weight(message: Message, state: FSMContext):
    await update_handler(message, state, weight=message.text)

@router.message(UserData.height)
async def get_height(message: Message, state: FSMContext):
    await update_handler(message, state, height=message.text)

@router.callback_query(UserData.birthday)
async def update_birthday_handler(callback: CallbackQuery, state: FSMContext):
    await update_handler(callback, state, birthday=callback.data)

@router.callback_query(UserData.sex)
async def update_sex_handler(callback: CallbackQuery, state: FSMContext):
    await update_handler(callback, state, sex=Sex(callback.data))

@router.callback_query(UserData.activity)
async def update_activity_handler(callback: CallbackQuery, state: FSMContext):
    await update_handler(callback, state, activity=Activity(callback.data))

@router.callback_query(UserData.goal)
async def update_goal_handler(callback: CallbackQuery, state: FSMContext):
    await update_handler(callback, state, goal=Goal(callback.data))

@router.callback_query(UserData.language)
async def change_language(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await set_current_language(state, callback.data)
    await state.set_state()
    await go_back(callback, state)
