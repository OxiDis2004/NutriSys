from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle


class ActivityMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.ACTIVITY
        buttons = [
            [
                MenuButton(MenuButtonTitle.ACTIVITY_VERY_LOW, MenuButtonTitle.ACTIVITY_VERY_LOW),
                MenuButton(MenuButtonTitle.ACTIVITY_LOW, MenuButtonTitle.ACTIVITY_LOW)
            ],
            [
                MenuButton(MenuButtonTitle.ACTIVITY_MIDDLE, MenuButtonTitle.ACTIVITY_MIDDLE)
            ],
            [
                MenuButton(MenuButtonTitle.ACTIVITY_HIGH, MenuButtonTitle.ACTIVITY_HIGH),
                MenuButton(MenuButtonTitle.ACTIVITY_VERY_HIGH, MenuButtonTitle.ACTIVITY_VERY_HIGH)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]

        super().__init__(telegram_id, title, buttons)