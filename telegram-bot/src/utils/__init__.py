from typing import Union

from aiogram.fsm.context import FSMContext

from src.models.language import Language
from src.models.menu_parts.menu_buttons import MenuButton
from src.models.menu_parts.menu_title import MenuTitle
from src.models.statistic_type import StatisticType, PeriodType
from src.models.unit import Unit
from src.services.users import get_current_language
from src.static import ua, en, de

TypeToTranslate = Union[MenuButton, MenuTitle, StatisticType, PeriodType, Unit]

Vocabulary = {
    Language.UKRAINE.value: ua.vocabulary(),
    Language.ENGLISH.value: en.vocabulary(),
    Language.GERMAN.value: de.vocabulary()
}

async def translate(
        state: FSMContext,
        text: TypeToTranslate
):
    language = await get_current_language(state)
    vocabulary = Vocabulary.get(language, {})
    return vocabulary[text] if text in vocabulary else text