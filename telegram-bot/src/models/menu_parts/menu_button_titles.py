from enum import Enum


class MenuButtonTitle(Enum):
    #   --- FOR ALL ---
    BACK = "back"
    #   --- Main menu ---
    WATER = "water"
    FOOD = "eat"
    STATISTIC = "stat"
    SETTINGS = "settings"
    LINK_WEBSITE = "link_website"
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
    #   --- Food menu ---
    ADD_FOOD = "add_food"
    #   --- Settings menu ---
    USER_INFO = "user_info"
    LANGUAGE = "language"
    #   --- User info ---
    WEIGHT = "weight"
    HEIGHT = "height"
    BIRTHDAY = "birthday"
    SEX = "sex"
    ACTIVITY = "activity"
    GOAL = "goal"
    #   --- Calendar ---
    OPEN_CALENDAR = "open_calendar"
    #   --- Sex ---
    MALE = "male_choice"
    FEMALE = "female_choice"
    #   --- Activity ---
    ACTIVITY_VERY_LOW = "activity_very_low"
    ACTIVITY_LOW = "activity_low"
    ACTIVITY_MIDDLE = "activity_middle"
    ACTIVITY_HIGH = "activity_high"
    ACTIVITY_VERY_HIGH = "activity_very_high"
    #   --- Goal ---
    LOSE_WEIGHT = "lose_weight"
    KEEP_WEIGHT = "keep_weight"
    GAIN_WEIGHT = "gain_weight"
    #   --- Language menu ---
    UKRAINE = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 English"
    GERMAN = "🇩🇪 Deutsch"