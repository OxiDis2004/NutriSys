from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_title import MenuTitle
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton


class UserInfoMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.USER_INFO

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        return [
            [
                MenuButton(MenuButtonTitle.WEIGHT, MenuButtonTitle.WEIGHT),
                MenuButton(MenuButtonTitle.HEIGHT, MenuButtonTitle.HEIGHT),
                MenuButton(MenuButtonTitle.BIRTHDAY, MenuButtonTitle.BIRTHDAY)
            ],
            [
                MenuButton(MenuButtonTitle.SEX, MenuButtonTitle.SEX),
                MenuButton(MenuButtonTitle.ACTIVITY, MenuButtonTitle.ACTIVITY),
                MenuButton(MenuButtonTitle.GOAL, MenuButtonTitle.GOAL)
            ],
            [
                MenuButton(MenuButtonTitle.BACK, MenuButtonTitle.BACK)
            ]
        ]