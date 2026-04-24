from abc import ABC, abstractmethod

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle
from src.utils import translate


class BaseMenu(ABC):
    def __init__(self, state: FSMContext, title: str, keyboard: list[list[InlineKeyboardButton]]):
        self._state: FSMContext = state
        self._title: str = title
        self._keyboard: list[list[InlineKeyboardButton]] = keyboard

    @classmethod
    @abstractmethod
    def get_title(cls) -> MenuTitle:
        pass

    @classmethod
    @abstractmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        pass

    @classmethod
    async def create(cls, state: FSMContext):
        translated_title = await translate(state, cls.get_title())
        keyboard = await cls.build(state, await cls.get_buttons(state))
        return cls(state, translated_title, keyboard)

    @staticmethod
    async def build(state: FSMContext, buttons: list[list[MenuButton]]) \
            -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=(await translate(state, button.title)),
                    callback_data=button.callback,
                    web_app=WebAppInfo(url=button.url) if button.url is not None else None
                )
                for button in button_row
            ] for button_row in buttons
        ]

    @property
    def title(self):
        return self._title

    @property
    def keyboard(self):
        return InlineKeyboardMarkup(inline_keyboard=self._keyboard)
