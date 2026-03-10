from src.models.language import Language
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit

from src.services.users import get_current_user_language
from src.static import ua, en, de

CURRENT_LANGUAGE = None

def translate(telegram_id: int, text: MenuButton | MenuTitle | StatisticType | Unit):
    global CURRENT_LANGUAGE

    language = get_current_user_language(telegram_id)
    if CURRENT_LANGUAGE != language:
        CURRENT_LANGUAGE = language

    vocabulary = {}

    match CURRENT_LANGUAGE:
        case Language.UKRAINE.value: vocabulary = ua.vocabulary()
        case Language.ENGLISH.value: vocabulary = en.vocabulary()
        case Language.GERMAN.value: vocabulary = de.vocabulary()

    return vocabulary[text] if text in vocabulary else text

