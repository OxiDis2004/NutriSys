from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.menu_parts.menu_title import MenuTitle
from src.models.unit import Unit

DE_VOCABULARY = {
    MenuButtonTitle.BACK: "🔙 Zurück",
    MenuButtonTitle.WATER: "💧 Wasser",
    MenuButtonTitle.FOOD: "🥗 Essen",
    MenuButtonTitle.STATISTIC: "📊 Statistik",
    MenuButtonTitle.SETTINGS: "⚙️ Einstellungen",
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

    MenuButtonTitle.LANGUAGE: "🌐 Sprache",

    MenuTitle.NOT_FOUND: "Nicht verstanden 🤔 Bitte wählen Sie aus dem Menü unten.",
    MenuTitle.START_TITLE: "Willkommen! Hier ist das Hauptmenü:",
    MenuTitle.STATISTIC_TITLE: "Ihr Status: ✅ Alles funktioniert\nWählen Sie eine Kategorie zur Anzeige der Statistik:",
    MenuTitle.PERIOD_TITLE: "Wählen Sie den Zeitraum aus:",
    MenuTitle.WATER_TITLE: "Geben Sie ein, wie viel Wasser Sie getrunken haben:",
    MenuTitle.DRUNK_TITLE: "Sie haben getrunken: {water} {unit}",
    MenuTitle.FOOD_TITLE: "Schicken Sie einen Foto zu:",
    MenuTitle.SETTINGS_TITLE: "⚙️ Einstellungsmenü:",
    MenuTitle.LANGUAGE_TITLE: "🌐 Sprache auswählen:",
    MenuTitle.EXISTS_COMMAND: "Verfügbare Befehle:",

    Unit.L: "l",
    Unit.ML: "ml"
}

def vocabulary():
    return DE_VOCABULARY