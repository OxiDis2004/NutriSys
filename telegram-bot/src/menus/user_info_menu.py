from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class UserInfoMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.USER_INFO
        buttons = [
            [
                MenuButton(MenuButtonTitle.WEIGHT, MenuButtonTitle.WEIGHT),
                MenuButton(MenuButtonTitle.HEIGHT, MenuButtonTitle.HEIGHT),
                MenuButton(MenuButtonTitle.BIRTHDAY, MenuButtonTitle.BIRTHDAY)
            ],
            [
                MenuButton(MenuButtonTitle.SEX, MenuButtonTitle.SEX),
                MenuButton(MenuButtonTitle.ACTIVITY, MenuButtonTitle.ACTIVITY),
                MenuButton(MenuButtonTitle.GOAL, MenuButtonTitle.GOAL)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]
        super().__init__(telegram_id, title, buttons)
