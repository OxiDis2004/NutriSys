from src.models.menu_parts.menu_button_titles import MenuButtonTitle


class MenuButton:
    def __init__(self, title: MenuButtonTitle | str, callback = None, url = None):
        self._title = title
        self._callback = callback
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def callback(self):
        return self._callback

    @property
    def url(self):
        return self._url