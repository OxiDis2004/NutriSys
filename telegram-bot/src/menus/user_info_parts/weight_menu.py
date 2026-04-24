from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle


class WeightMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.WEIGHT

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return []