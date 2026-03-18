from aiogram.fsm.context import FSMContext

from src.models.language import Language
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType, PeriodType
from src.models.unit import Unit
from src.services.users import get_current_language
from src.static import ua, en, de


async def translate(
        state: FSMContext,
        text: MenuButton | MenuTitle | StatisticType | PeriodType | Unit
):
    language = await get_current_language(state)
    vocabulary = {}

    match language:
        case Language.UKRAINE.value: vocabulary = ua.vocabulary()
        case Language.ENGLISH.value: vocabulary = en.vocabulary()
        case Language.GERMAN.value: vocabulary = de.vocabulary()

    return vocabulary[text] if text in vocabulary else text