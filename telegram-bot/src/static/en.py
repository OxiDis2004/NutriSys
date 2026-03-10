from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_title import MenuTitle
from src.models.unit import Unit

EN_VOCABULARY = {
    MenuButtonTitle.BACK: "🔙 Back",
    MenuButtonTitle.WATER: "💧 Water",
    MenuButtonTitle.FOOD: "🥗 Food",
    MenuButtonTitle.STATISTIC: "📊 Statistics",
    MenuButtonTitle.SETTINGS: "⚙️ Settings",
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

    MenuButtonTitle.LANGUAGE: "🌐 Language",

    MenuTitle.NOT_FOUND: "I didn’t understand 🤔 Please choose from the menu below.",
    MenuTitle.START_TITLE: "Welcome! Here is the main menu:",
    MenuTitle.STATISTIC_TITLE: "Your status: ✅ Everything works\nChoose a category to view statistics:",
    MenuTitle.PERIOD_TITLE: "Choose a period to display:",
    MenuTitle.WATER_TITLE: "Enter how much water you drank:",
    MenuTitle.DRUNK_TITLE: "You have been drinking: {water} {unit}",
    MenuTitle.FOOD_TITLE: "Send a photo of food:",
    MenuTitle.SETTINGS_TITLE: "⚙️ Settings menu:",
    MenuTitle.LANGUAGE_TITLE: "🌐 Select a language:",
    MenuTitle.EXISTS_COMMAND: "Available commands:",

    Unit.L: "l",
    Unit.ML: "ml"
}

def vocabulary():
    return EN_VOCABULARY