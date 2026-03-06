from src.models.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_button_titles import MenuButtonTitle
from src.models.menu_buttons import MenuButton


class StartMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.START_TITLE
        buttons = [
            [
                MenuButton(MenuButtonTitle.WATER, MenuButtonTitle.WATER),
                MenuButton(MenuButtonTitle.FOOD, MenuButtonTitle.FOOD)
            ],
            [
                MenuButton(MenuButtonTitle.STATISTIC, MenuButtonTitle.STATISTIC),
                MenuButton(MenuButtonTitle.SETTINGS, MenuButtonTitle.SETTINGS),
            ],
            [MenuButton(MenuButtonTitle.HELP, MenuButtonTitle.HELP)]
        ]
        super().__init__(telegram_id, title, buttons)
