from aiogram.fsm.context import FSMContext

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


class MenuFactory:
    _menus: dict[MenuType, type[BaseMenu]] = {
        MenuType.START: StartMenu,
        MenuType.WATER: WaterMenu,
        MenuType.FOOD: FoodMenu,
        MenuType.STATISTIC: StatisticMenu,
        MenuType.PERIOD: PeriodMenu,
        MenuType.SETTINGS: SettingsMenu,
        MenuType.USER_INFO: UserInfoMenu,
        MenuType.WEIGHT: WeightMenu,
        MenuType.HEIGHT: HeightMenu,
        MenuType.BIRTHDAY: BirthdayMenu,
        MenuType.SEX: SexMenu,
        MenuType.ACTIVITY: ActivityMenu,
        MenuType.GOAL: GoalMenu,
        MenuType.LANGUAGE: LanguageMenu,
    }

    @staticmethod
    async def build_menu(menu_type: MenuType, state: FSMContext) -> BaseMenu:
        menu_cls = MenuFactory._menus.get(menu_type, StartMenu)
        return await menu_cls.create(state)
