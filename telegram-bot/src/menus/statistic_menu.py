from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class StatisticMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.STATISTIC_TITLE
        buttons = [
            [
                MenuButton(MenuButtonTitle.CALORIE, MenuButtonTitle.CALORIE),
                MenuButton(MenuButtonTitle.DRUNK_WATER, MenuButtonTitle.DRUNK_WATER)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]
        super().__init__(telegram_id, title, buttons)
