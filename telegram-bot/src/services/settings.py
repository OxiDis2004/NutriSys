from datetime import date
from src.models.language import Language
from src.models.menu_parts.menu_button_titles import MenuButtonTitle
from src.models.user import User
from src.services import request_put
from src.services.users import get_current_user, update_user

language_key = "language_key"

def get_current_user_language(telegram_id: int):
    user: User = get_current_user(telegram_id)
    return user.language if user.language is not None else Language.ENGLISH.value

async def set_current_user_language(telegram_id: int, language: str):
    user: User = get_current_user(telegram_id)
    if user.language != language:
        user.language = language
        body = user.base_info()
        resp = await request_put(f"/user/change_language", body)

        if resp.status_code == 202:
            update_user(telegram_id, user)

async def update_user_info(
        telegram_id: int,
        weight: str = None,
        height: str = None,
        birthday: date = None,
        sex: MenuButtonTitle = None,
        activity: MenuButtonTitle = None,
        goal: MenuButtonTitle = None
):
    user: User = get_current_user(telegram_id)
    if user is None:
        return

    print(sex, activity, goal)

    user.birthday = birthday
    user.weight = weight
    user.height = height
    user.sex = sex
    user.activity = activity
    user.goal = goal

    body = {
        "id": user.user_id,
        "name": None,
        "lastname": None,
        "birthday": user.birthday,
        "weight": user.weight,
        "height": user.height,
        "sex": user.sex,
        "activity": user.activity,
        "goal": user.goal,
    }
    resp = await request_put(f"/user/update_info", body)

    if resp.status_code == 202:
        update_user(telegram_id, user)
