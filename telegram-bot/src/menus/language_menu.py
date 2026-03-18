from aiogram.fsm.context import FSMContext

from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.language import Language
from src.services.users import get_current_language


class LanguageMenu(BaseMenu):

    LANGUAGES = [
        (MenuButtonTitle.UKRAINE, Language.UKRAINE),
        (MenuButtonTitle.ENGLISH, Language.ENGLISH),
        (MenuButtonTitle.GERMAN, Language.GERMAN),
    ]

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.LANGUAGE

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
            [MenuButton(await cls._format(state, title, lang), lang)]
            for title, lang in cls.LANGUAGES
        ]

    @staticmethod
    async def _format(state: FSMContext, button: MenuButtonTitle, language: Language):
        current = '(*)' if language.value == await get_current_language(state) else ''
        return f"{button.value} {current}"
