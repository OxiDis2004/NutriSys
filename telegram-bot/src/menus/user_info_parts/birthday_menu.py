from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle


class BirthdayMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.BIRTHDAY
        buttons = [
            [
                MenuButton(MenuButtonTitle.OPEN_CALENDAR, MenuButtonTitle.OPEN_CALENDAR)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]

        super().__init__(telegram_id, title, buttons)