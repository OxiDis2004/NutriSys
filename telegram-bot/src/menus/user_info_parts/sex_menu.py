from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle


class SexMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.SEX

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
            [
                MenuButton(MenuButtonTitle.MALE, MenuButtonTitle.MALE),
                MenuButton(MenuButtonTitle.FEMALE, MenuButtonTitle.FEMALE)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]