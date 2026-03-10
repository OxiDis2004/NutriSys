from abc import ABC

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle
from src.services.language import translate


class BaseMenu(ABC):
    def __init__(self, telegram_id: int, title: MenuTitle, buttons: list[list[MenuButton]]):
        self._telegram_id = telegram_id
        self._title: MenuTitle = title
        self._buttons = buttons
        self._keyboard: list[list[InlineKeyboardButton]] = []

    def _build(self):
        self._keyboard = [
            [
                InlineKeyboardButton(
                    text=translate(self._telegram_id, button.title),
                    callback_data=button.callback,
                    web_app=WebAppInfo(url=button.url) if button.url is not None else None
                )
                for button in button_row
            ] for button_row in self._buttons
        ]

    @property
    def title(self):
        return translate(self._telegram_id, self._title)

    @property
    def keyboard(self):
        self._build()
        return InlineKeyboardMarkup(inline_keyboard=self._keyboard)
