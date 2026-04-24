from aiogram.fsm.context import FSMContext

from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_title import MenuTitle
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.services.users import get_website_url


class StartMenu(BaseMenu):

    @classmethod
    def get_title(cls) -> MenuTitle:
        return MenuTitle.START

    @classmethod
    async def get_buttons(cls, state: FSMContext) -> list[list[MenuButton]]:
        url = await get_website_url(state)
        return [
            [
                MenuButton(MenuButtonTitle.WATER, MenuButtonTitle.WATER),
                MenuButton(MenuButtonTitle.FOOD, MenuButtonTitle.FOOD)
            ],
            [
                MenuButton(MenuButtonTitle.STATISTIC, MenuButtonTitle.STATISTIC),
                MenuButton(MenuButtonTitle.SETTINGS, MenuButtonTitle.SETTINGS),
            ],
            [MenuButton(MenuButtonTitle.LINK_WEBSITE, url=url)],
            [MenuButton(MenuButtonTitle.HELP, MenuButtonTitle.HELP)]
        ]
