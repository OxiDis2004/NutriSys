from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class SettingsMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.SETTINGS_TITLE
        buttons = [
            [
                MenuButton(MenuButtonTitle.LANGUAGE, MenuButtonTitle.LANGUAGE)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]
        super().__init__(telegram_id, title, buttons)
