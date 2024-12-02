import json
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update
from bot.rds import RedisDB


class ServicesMiddlewareMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        rds: RedisDB = data["bot"].rds
        services = await rds.services.get("services")
        if services:
            data["services"] = json.loads(services)
            return await handler(event, data)
        else:
            await event.message.answer(f"Услуги не найдены, обратитесь к администратору!")

async def register_services_middleware(dp: Dispatcher) -> None:
    dp.update.middleware(ServicesMiddlewareMiddleware())
