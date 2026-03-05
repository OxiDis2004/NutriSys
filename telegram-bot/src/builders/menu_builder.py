from src.models.menu_type import MenuType
from src.models.menus.base_menu import BaseMenu
from src.models.menus.food_menu import FoodMenu
from src.models.menus.language_menu import LanguageMenu
from src.models.menus.period_menu import PeriodMenu
from src.models.menus.settings_menu import SettingsMenu
from src.models.menus.start_menu import StartMenu
from src.models.menus.statistic_menu import StatisticMenu
from src.models.menus.water_menu import WaterMenu


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

        return menu
