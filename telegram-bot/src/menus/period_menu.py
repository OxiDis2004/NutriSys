from aiogram.fsm.context import FSMContext

from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class PeriodMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.PERIOD

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
            [
                MenuButton(MenuButtonTitle.LAST_WEEK, MenuButtonTitle.LAST_WEEK),
                MenuButton(MenuButtonTitle.LAST_MONTH, MenuButtonTitle.LAST_MONTH),
                MenuButton(MenuButtonTitle.LAST_YEAR, MenuButtonTitle.LAST_YEAR)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]