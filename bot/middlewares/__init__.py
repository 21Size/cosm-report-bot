from aiogram import Dispatcher

from bot.middlewares.auth import register_auth_middleware
from bot.middlewares.ydisk import register_ydisk_middleware
from bot.middlewares.services import register_services_middleware


async def register_all_middlewares(dp: Dispatcher) -> None:
    # await register_throttling_middleware(dp)
    await register_auth_middleware(dp)
    await register_services_middleware(dp)
    await register_ydisk_middleware(dp)
