from src.menus.user_info_menu import UserInfoMenu
from src.menus.user_info_parts.activity_menu import ActivityMenu
from src.menus.user_info_parts.birthday_menu import BirthdayMenu
from src.menus.user_info_parts.goal_menu import GoalMenu
from src.menus.user_info_parts.height_menu import HeightMenu
from src.menus.user_info_parts.sex_menu import SexMenu
from src.menus.user_info_parts.weight_menu import WeightMenu
from src.models.menu_parts.menu_type import MenuType
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
            case MenuType.USER_INFO: menu = UserInfoMenu(telegram_id)
            case MenuType.WEIGHT: menu = WeightMenu(telegram_id)
            case MenuType.HEIGHT: menu = HeightMenu(telegram_id)
            case MenuType.BIRTHDAY: menu = BirthdayMenu(telegram_id)
            case MenuType.SEX: menu = SexMenu(telegram_id)
            case MenuType.ACTIVITY: menu = ActivityMenu(telegram_id)
            case MenuType.GOAL: menu = GoalMenu(telegram_id)
            case MenuType.LANGUAGE: menu = LanguageMenu(telegram_id)
            case _: menu = StartMenu(telegram_id)

        return menu
