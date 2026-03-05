from enum import Enum


class MenuButtonTitle(Enum):
    #   --- FOR ALL ---
    BACK = "back"
    #   --- Main menu ---
    WATER = "water"
    FOOD = "eat"
    STATISTIC = "stat"
    SETTINGS = "settings"
    HELP = "help"
    #   --- Statistic menu ---
    CALORIE = "calorie"
    DRUNK_WATER = "drunk_water"
    #   --- Period menu ---
    LAST_WEEK = "last_week"
    LAST_MONTH = "last_month"
    LAST_YEAR = "last_year"
    #   --- Water menu ---
    ADD_250_ML = "250ml"
    ADD_500_ML = "500ml"
    ADD_1_L = "1l"
    ADD_1_5_L = "1.5l"
    #   --- Settings menu ---
    LANGUAGE = "language"
    #   --- Language menu ---
    UKRAINE = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 English"
    GERMAN = "🇩🇪 Deutsch"