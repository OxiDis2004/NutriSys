from src.models.language import Language
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType
from src.models.unit import Unit

from src.services.settings import get_current_user_language
from src.static import ua, en, de

def translate(telegram_id: int, text: MenuButton | MenuTitle | StatisticType | Unit):
    language = get_current_user_language(telegram_id)
    vocabulary = {}

    match language:
        case Language.UKRAINE.value: vocabulary = ua.vocabulary()
        case Language.ENGLISH.value: vocabulary = en.vocabulary()
        case Language.GERMAN.value: vocabulary = de.vocabulary()

    return vocabulary[text] if text in vocabulary else text
