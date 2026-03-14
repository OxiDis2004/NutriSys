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
    MenuButtonTitle.LINK_WEBSITE: "🔗 Веб-інтерфейс",
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

    MenuButtonTitle.USER_INFO: "👤 Особисті дані",
    MenuButtonTitle.LANGUAGE: "🌐 Мова",

    MenuButtonTitle.WEIGHT: "⚖️ Змінити вагу",
    MenuButtonTitle.HEIGHT: "📏 Змінити зріст",
    MenuButtonTitle.BIRTHDAY: "🎂 Змінити дату народження",
    MenuButtonTitle.SEX: "⚧️ Змінити стать",
    MenuButtonTitle.ACTIVITY: "🏃‍♂️ Змінити рівень активності",
    MenuButtonTitle.GOAL: "🎯 Змінити ціль",

    MenuButtonTitle.MALE: "Чоловіча",
    MenuButtonTitle.FEMALE: "Жіноча",

    MenuButtonTitle.ACTIVITY_VERY_LOW: "Дуже мала (0-1)",
    MenuButtonTitle.ACTIVITY_LOW: "Мала (2-3)",
    MenuButtonTitle.ACTIVITY_MIDDLE: "Середня (4-5)",
    MenuButtonTitle.ACTIVITY_HIGH: "Високий (6-7)",
    MenuButtonTitle.ACTIVITY_VERY_HIGH: "Дуже високий (7+)",

    MenuButtonTitle.LOSE_WEIGHT: "Схуднути",
    MenuButtonTitle.KEEP_WEIGHT: "Тримати",
    MenuButtonTitle.GAIN_WEIGHT: "Набрати",

    MenuTitle.NOT_FOUND: "Не зрозумів 🤔 Оберіть із меню нижче.",
    MenuTitle.START: "Ласкаво просимо! Ось головне меню:",
    MenuTitle.STATISTIC: "Ваш статус: ✅ Все працює\nОберіть категорію для перегляду статистики:",
    MenuTitle.PERIOD: "Оберіть період для показу:",
    MenuTitle.WATER: "Введіть, скільки води ви випили:",
    MenuTitle.FOOD: "Надішліть фото з їжею для розпізнавання:",
    MenuTitle.DRUNK: "Ви випили води: {water} {unit}",
    MenuTitle.SETTINGS: "⚙️ Меню налаштувань:",
    MenuTitle.USER_INFO: "Які дані ви хочете змінити:",
    MenuTitle.LANGUAGE: "🌐 Оберіть мову:",
    MenuTitle.EXISTS_COMMAND: "Існуючі команди:",

    MenuTitle.WEIGHT: "Введіть вашу вагу (кг):",
    MenuTitle.HEIGHT: "Введіть ваш зріст (см):",
    MenuTitle.BIRTHDAY: "Виберіть вашу дату народження:",
    MenuTitle.SEX: "Виберіть вашу стать:",
    MenuTitle.ACTIVITY: "Виберіть ваш рівень активності:",
    MenuTitle.GOAL: "Виберіть вашу ціль:",
    
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