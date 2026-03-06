from src.models.menu_type import MenuType
from src.menus.base_menu import BaseMenu
from src.menus.food_menu import FoodMenu
from src.menus.language_menu import LanguageMenu
from src.menus.period_menu import PeriodMenu
from src.menus.settings_menu import SettingsMenu
from src.menus.start_menu import StartMenu
from src.menus.statistic_menu import StatisticMenu
from src.menus.water_menu import WaterMenu


class MenuBuilder:
    @staticmethod
    def build_menu(menu_type: MenuType, telegram_id: int) -> BaseMenu:
        menu = None
        match menu_type:
            case MenuType.START: menu = StartMenu(telegram_id)
            case MenuType.WATER: menu = WaterMenu(telegram_id)
            case MenuType.FOOD: menu = FoodMenu(telegram_id)
            case MenuType.STATISTIC: menu = StatisticMenu(telegram_id)
            case MenuType.PERIOD: menu = PeriodMenu(telegram_id)
            case MenuType.SETTINGS: menu = SettingsMenu(telegram_id)
            case MenuType.LANGUAGE: menu = LanguageMenu(telegram_id)
            case _: menu = StartMenu(telegram_id)

        return menu
