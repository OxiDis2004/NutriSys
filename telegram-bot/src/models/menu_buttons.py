from src.models.menu_button_titles import MenuButtonTitle


class MenuButton:
    def __init__(self, title: MenuButtonTitle | str, callback):
        self._title = title
        self._callback = callback

    @property
    def title(self):
        return self._title

    @property
    def callback(self):
        return self._callback