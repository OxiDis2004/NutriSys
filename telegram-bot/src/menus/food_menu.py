from aiogram.fsm.context import FSMContext

from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class FoodMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.FOOD

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
            [
                MenuButton(MenuButtonTitle.ADD_FOOD, MenuButtonTitle.ADD_FOOD),
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]