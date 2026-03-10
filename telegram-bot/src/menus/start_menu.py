from src.models.menu_parts.menu_title import MenuTitle
from src.menus.base_menu import BaseMenu
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_buttons import MenuButton
from src.services.users import get_website_url


class StartMenu(BaseMenu):
    def __init__(self, telegram_id: int):
        title = MenuTitle.START_TITLE
        buttons = [
            [
                MenuButton(MenuButtonTitle.WATER, MenuButtonTitle.WATER),
                MenuButton(MenuButtonTitle.FOOD, MenuButtonTitle.FOOD)
            ],
            [
                MenuButton(MenuButtonTitle.STATISTIC, MenuButtonTitle.STATISTIC),
                MenuButton(MenuButtonTitle.SETTINGS, MenuButtonTitle.SETTINGS),
            ],
            [MenuButton(MenuButtonTitle.LINK_WEBSITE, url=get_website_url(telegram_id))],
            [MenuButton(MenuButtonTitle.HELP, MenuButtonTitle.HELP)]
        ]
        super().__init__(telegram_id, title, buttons)
