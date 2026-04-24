from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_title import MenuTitle
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class WaterMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.WATER

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
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