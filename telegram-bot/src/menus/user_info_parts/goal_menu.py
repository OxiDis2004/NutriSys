from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle


class GoalMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.GOAL
        buttons = [
            [
                MenuButton(MenuButtonTitle.LOSE_WEIGHT, MenuButtonTitle.LOSE_WEIGHT),
                MenuButton(MenuButtonTitle.KEEP_WEIGHT, MenuButtonTitle.KEEP_WEIGHT),
                MenuButton(MenuButtonTitle.GAIN_WEIGHT, MenuButtonTitle.GAIN_WEIGHT)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]

        super().__init__(telegram_id, title, buttons)