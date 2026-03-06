from aiogram import Dispatcher

from src.handlers.start import router as start_router
from src.handlers.admin import router as admin_router
from src.handlers.settings import router as settings_router
from src.handlers.water import router as water_router
from src.handlers.food import router as food_router
from src.handlers.previous import router as previous_router
from src.handlers.help import router as help_router


def setup_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(settings_router)
    dp.include_router(water_router)
    dp.include_router(food_router)
    dp.include_router(previous_router)
    dp.include_router(help_router)
