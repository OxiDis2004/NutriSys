from aiogram.fsm.storage.base import BaseStorage, StorageKey

from src.models.language import Language

language_key = "language_key"

LANGUAGES = [
    Language.UKRAINE.value,
    Language.ENGLISH.value,
    Language.GERMAN.value
]

def set_language(storage: BaseStorage, language: str):
    normalized = language.lower()
    for lang in LANGUAGES:
        if lang not in normalized and lang != normalized:
            language = Language.ENGLISH.value

    storage.set_data()
