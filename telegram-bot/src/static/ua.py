from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit

UA_VOCABULARY = {
    MenuButtonTitle.BACK: "🔙 Назад",
    MenuButtonTitle.WATER: "💧 Вода",
    MenuButtonTitle.FOOD: "🥗 Їжа",
    MenuButtonTitle.STATISTIC: "📊 Статистика",
    MenuButtonTitle.SETTINGS: "⚙️ Налаштування",
    MenuButtonTitle.HELP: "❓ Допомога",

    MenuButtonTitle.CALORIE: "Калорії",
    MenuButtonTitle.DRUNK_WATER: "Випита вода",

    MenuButtonTitle.LAST_WEEK: "Останній тиждень",
    MenuButtonTitle.LAST_MONTH: "Останній місяць",
    MenuButtonTitle.LAST_YEAR: "Останній рік",

    MenuButtonTitle.ADD_250_ML: "250 мл",
    MenuButtonTitle.ADD_500_ML: "500 мл",
    MenuButtonTitle.ADD_1_L: "1 л",
    MenuButtonTitle.ADD_1_5_L: "1,5 л",

    MenuButtonTitle.LANGUAGE: "🌐 Мова",

    MenuTitle.NOT_FOUND: "Не зрозумів 🤔 Оберіть із меню нижче.",
    MenuTitle.START_TITLE: "Ласкаво просимо! Ось головне меню:",
    MenuTitle.STATISTIC_TITLE: "Ваш статус: ✅ Все працює\nОберіть категорію для перегляду статистики:",
    MenuTitle.PERIOD_TITLE: "Оберіть період для показу:",
    MenuTitle.WATER_TITLE: "Введіть, скільки води ви випили:",
    MenuTitle.FOOD_TITLE: "Надішліть фото з їжею для розпізнавання:",
    MenuTitle.DRUNK_TITLE: "Ви випили води: {water} {unit}",
    MenuTitle.SETTINGS_TITLE: "⚙️ Меню налаштувань:",
    MenuTitle.LANGUAGE_TITLE: "🌐 Оберіть мову:",
    MenuTitle.EXISTS_COMMAND: "Існуючі команди:",
    
    Unit.L: "л",
    Unit.ML: "мл",

    StatisticType.WATER: "Статистика випитої води",
    StatisticType.CALORIE: "Статистика калорії",

    StatisticType.WEEK: "День неділі",
    StatisticType.MONTH: "День місяця",
    StatisticType.YEAR: "Місяць",
}

def vocabulary():
    return UA_VOCABULARY