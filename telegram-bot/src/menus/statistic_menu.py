from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_title import MenuTitle
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class StatisticMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.STATISTIC

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
            [
                MenuButton(MenuButtonTitle.CALORIE, MenuButtonTitle.CALORIE),
                MenuButton(MenuButtonTitle.DRUNK_WATER, MenuButtonTitle.DRUNK_WATER)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]