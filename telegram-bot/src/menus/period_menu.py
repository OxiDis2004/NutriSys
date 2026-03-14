from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class PeriodMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.PERIOD
        buttons = [
            [
                MenuButton(MenuButtonTitle.LAST_WEEK, MenuButtonTitle.LAST_WEEK),
                MenuButton(MenuButtonTitle.LAST_MONTH, MenuButtonTitle.LAST_MONTH),
                MenuButton(MenuButtonTitle.LAST_YEAR, MenuButtonTitle.LAST_YEAR)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]
        super().__init__(telegram_id, title, buttons)
