from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class WaterMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.WATER
        buttons = [
            [
                MenuButton(MenuButtonTitle.ADD_250_ML, MenuButtonTitle.ADD_250_ML),
                MenuButton(MenuButtonTitle.ADD_500_ML, MenuButtonTitle.ADD_500_ML),
            ],
            [
                MenuButton(MenuButtonTitle.ADD_1_L, MenuButtonTitle.ADD_1_L),
                MenuButton(MenuButtonTitle.ADD_1_5_L, MenuButtonTitle.ADD_1_5_L),
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]
        super().__init__(telegram_id, title, buttons)
