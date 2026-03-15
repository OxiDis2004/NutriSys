from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.language import Language
from src.services.settings import get_current_user_language


class LanguageMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.LANGUAGE
        buttons = [
            [
                MenuButton(self._format(telegram_id, MenuButtonTitle.UKRAINE, Language.UKRAINE),
                    Language.UKRAINE)
            ],
            [
                MenuButton(self._format(telegram_id, MenuButtonTitle.ENGLISH, Language.ENGLISH),
                    Language.ENGLISH)
            ],
            [
                MenuButton(self._format(telegram_id, MenuButtonTitle.GERMAN, Language.GERMAN),
                    Language.GERMAN)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]

        super().__init__(telegram_id, title, buttons)

    @staticmethod
    def _format(telegram_id: int, button: MenuButtonTitle, language: Language):
        current = '(*)' if language.value == get_current_user_language(telegram_id) else ''
        return f"{button.value} {current}"
