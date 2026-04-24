from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle


class ActivityMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.ACTIVITY

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
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