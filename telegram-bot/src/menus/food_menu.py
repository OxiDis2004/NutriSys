from aiogram.fsm.context import FSMContext

from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_buttons import MenuButton


class FoodMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.FOOD

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return []