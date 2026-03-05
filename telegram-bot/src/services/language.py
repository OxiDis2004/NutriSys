from src.models.menu_buttons import MenuButton

def translate(telegram_id: int, text: MenuButton | str):
    return text.title.value if text is MenuButton else text

