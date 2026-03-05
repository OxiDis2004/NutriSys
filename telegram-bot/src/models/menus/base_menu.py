from abc import ABC

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.models.menu_buttons import MenuButton
from src.services.language import translate
from src.services.users import get_current_user_language


class BaseMenu(ABC):
    def __init__(self, telegram_id: int, title: str, buttons: list[list[MenuButton]]):
        self._telegram_id = telegram_id
        self._title: str = title
        self._buttons = buttons
        self._keyboard: list[list[InlineKeyboardButton]] = []
        self._last_language = ''

    def _build(self):
        self._keyboard = [
            [
                InlineKeyboardButton(
                    text=translate(self._telegram_id, button.title),
                    callback_data=button.callback
                )
                for button in button_row
            ] for button_row in self._buttons
        ]

    @property
    def title(self):
        return translate(self._telegram_id, self._title)

    @property
    def keyboard(self):
        if len(self._keyboard) == 0 or get_current_user_language(self._telegram_id) != self._last_language:
            self._build()
            self._last_language = get_current_user_language(self._telegram_id)

        return InlineKeyboardMarkup(inline_keyboard=self._keyboard)
