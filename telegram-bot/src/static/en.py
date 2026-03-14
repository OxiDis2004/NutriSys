from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit

EN_VOCABULARY = {
    MenuButtonTitle.BACK: "🔙 Back",
    MenuButtonTitle.WATER: "💧 Water",
    MenuButtonTitle.FOOD: "🥗 Food",
    MenuButtonTitle.STATISTIC: "📊 Statistics",
    MenuButtonTitle.SETTINGS: "⚙️ Settings",
    MenuButtonTitle.LINK_WEBSITE: "🔗 Website",
    MenuButtonTitle.HELP: "❓ Help",

    MenuButtonTitle.CALORIE: "Calories",
    MenuButtonTitle.DRUNK_WATER: "Drunk water",

    MenuButtonTitle.LAST_WEEK: "Last week",
    MenuButtonTitle.LAST_MONTH: "Last month",
    MenuButtonTitle.LAST_YEAR: "Last year",

    MenuButtonTitle.ADD_250_ML: "250 ml",
    MenuButtonTitle.ADD_500_ML: "500 ml",
    MenuButtonTitle.ADD_1_L: "1 l",
    MenuButtonTitle.ADD_1_5_L: "1.5 l",

    MenuButtonTitle.USER_INFO: "👤 Personal information",
    MenuButtonTitle.LANGUAGE: "🌐 Language",

    MenuButtonTitle.WEIGHT: "⚖️ Change weight",
    MenuButtonTitle.HEIGHT: "📏 Change height",
    MenuButtonTitle.BIRTHDAY: "🎂 Change birthday",
    MenuButtonTitle.SEX: "⚧️ Change sex",
    MenuButtonTitle.ACTIVITY: "🏃‍♂️ Change activity level",
    MenuButtonTitle.GOAL: "🎯 Change goal",

    MenuButtonTitle.MALE: "Male",
    MenuButtonTitle.FEMALE: "Female",

    MenuButtonTitle.ACTIVITY_VERY_LOW: "Very low (0-1)",
    MenuButtonTitle.ACTIVITY_LOW: "Low (2-3)",
    MenuButtonTitle.ACTIVITY_MIDDLE: "Middle (4-5)",
    MenuButtonTitle.ACTIVITY_HIGH: "High (6-7)",
    MenuButtonTitle.ACTIVITY_VERY_HIGH: "Very High (7+)",

    MenuButtonTitle.LOSE_WEIGHT: "Lose",
    MenuButtonTitle.KEEP_WEIGHT: "Keep",
    MenuButtonTitle.GAIN_WEIGHT: "Gain",

    MenuTitle.NOT_FOUND: "I didn’t understand 🤔 Please choose from the menu below.",
    MenuTitle.START: "Welcome! Here is the main menu:",
    MenuTitle.STATISTIC: "Your status: ✅ Everything works\nChoose a category to view statistics:",
    MenuTitle.PERIOD: "Choose a period to display:",
    MenuTitle.WATER: "Enter how much water you drank:",
    MenuTitle.DRUNK: "You have been drinking: {water} {unit}",
    MenuTitle.FOOD: "Send a photo of food:",
    MenuTitle.SETTINGS: "⚙️ Settings menu:",
    MenuTitle.USER_INFO: "What information would you like to change:",
    MenuTitle.LANGUAGE: "🌐 Select a language:",
    MenuTitle.EXISTS_COMMAND: "Available commands:",

    MenuTitle.WEIGHT: "Enter your weight (kg):",
    MenuTitle.HEIGHT: "Enter your height (cm):",
    MenuTitle.BIRTHDAY: "🎂 Select your birthday:",
    MenuTitle.SEX: "Select your sex:",
    MenuTitle.ACTIVITY: "🏃‍♂️ Select activity level:",
    MenuTitle.GOAL: "🎯 Select your goal:",

    Unit.L: "l",
    Unit.ML: "ml",

    StatisticType.WATER: "Water statistic",
    StatisticType.CALORIE: "Calorie statistic",

    StatisticType.WEEK: "Weekday",
    StatisticType.MONTH: "Day in month",
    StatisticType.YEAR: "Month",
}

def vocabulary():
    return EN_VOCABULARY