from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit

DE_VOCABULARY = {
    MenuButtonTitle.BACK: "🔙 Zurück",
    MenuButtonTitle.WATER: "💧 Wasser",
    MenuButtonTitle.FOOD: "🥗 Essen",
    MenuButtonTitle.STATISTIC: "📊 Statistik",
    MenuButtonTitle.SETTINGS: "⚙️ Einstellungen",
    MenuButtonTitle.LINK_WEBSITE: "🔗 Website",
    MenuButtonTitle.HELP: "❓ Hilfe",

    MenuButtonTitle.CALORIE: "Kalorien",
    MenuButtonTitle.DRUNK_WATER: "Getrunkenes Wasser",

    MenuButtonTitle.LAST_WEEK: "Letzte Woche",
    MenuButtonTitle.LAST_MONTH: "Letzter Monat",
    MenuButtonTitle.LAST_YEAR: "Letztes Jahr",

    MenuButtonTitle.ADD_250_ML: "250 ml",
    MenuButtonTitle.ADD_500_ML: "500 ml",
    MenuButtonTitle.ADD_1_L: "1 l",
    MenuButtonTitle.ADD_1_5_L: "1,5 l",

    MenuButtonTitle.USER_INFO: "👤 Persönliche Angaben",
    MenuButtonTitle.LANGUAGE: "🌐 Sprache",

    MenuButtonTitle.WEIGHT: "⚖️ Gewicht ändern",
    MenuButtonTitle.HEIGHT: "📏 Körpergröße ändern",
    MenuButtonTitle.BIRTHDAY: "🎂 Geburtsdatum ändern",
    MenuButtonTitle.SEX: "⚧️ Geschlecht ändern",
    MenuButtonTitle.ACTIVITY: "🏃‍♂️ Aktivitätsniveau ändern",
    MenuButtonTitle.GOAL: "🎯 Ziel ändern",

    MenuButtonTitle.MALE: "Männlich",
    MenuButtonTitle.FEMALE: "Weiblich",

    MenuButtonTitle.ACTIVITY_VERY_LOW: "Sehr niedrig (0-1)",
    MenuButtonTitle.ACTIVITY_LOW: "Niedrig (2-3)",
    MenuButtonTitle.ACTIVITY_MIDDLE: "Mittel (4-5)",
    MenuButtonTitle.ACTIVITY_HIGH: "Hohes (6-7)",
    MenuButtonTitle.ACTIVITY_VERY_HIGH: "Sehr hohes (7+)",

    MenuButtonTitle.LOSE_WEIGHT: "Abnehmen",
    MenuButtonTitle.KEEP_WEIGHT: "Behalten",
    MenuButtonTitle.GAIN_WEIGHT: "Aufnehmen",

    MenuTitle.NOT_FOUND: "Nicht verstanden 🤔 Bitte wählen Sie aus dem Menü unten.",
    MenuTitle.START: "Willkommen! Hier ist das Hauptmenü:",
    MenuTitle.STATISTIC: "Ihr Status: ✅ Alles funktioniert\nWählen Sie eine Kategorie zur Anzeige der Statistik:",
    MenuTitle.PERIOD: "Wählen Sie den Zeitraum aus:",
    MenuTitle.WATER: "Geben Sie ein, wie viel Wasser Sie getrunken haben:",
    MenuTitle.DRUNK: "Sie haben getrunken: {water} {unit}",
    MenuTitle.FOOD: "Schicken Sie einen Foto zu:",
    MenuTitle.SETTINGS: "⚙️ Einstellungsmenü:",
    MenuTitle.USER_INFO: "Welche Angaben möchten Sie ändern:",
    MenuTitle.LANGUAGE: "🌐 Sprache auswählen:",
    MenuTitle.EXISTS_COMMAND: "Verfügbare Befehle:",

    MenuTitle.WEIGHT: "Geben Sie Ihr Gewicht (kg) ein:",
    MenuTitle.HEIGHT: "Geben Sie Ihre Körpergröße (cm) ein:",
    MenuTitle.BIRTHDAY: "Wählen Sie Ihr Geburtsdatum aus:",
    MenuTitle.SEX: "Wählen Sie Ihr Geschlecht aus:",
    MenuTitle.ACTIVITY: "Wählen Sie Ihr Aktivitätsniveau aus:",
    MenuTitle.GOAL: "Wählen Sie Ihr Ziel aus:",

    Unit.L: "l",
    Unit.ML: "ml",

    StatisticType.WATER: "Wasser Statistik",
    StatisticType.CALORIE: "Calorien Statistik",

    StatisticType.WEEK: "Wochentag",
    StatisticType.MONTH: "Tag in Monat",
    StatisticType.YEAR: "Monat",
}

def vocabulary():
    return DE_VOCABULARY