import json
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update

from bot.rds import RedisDB
from bot.schemas.user import UserSchema


class AuthMiddlewareMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        rds: RedisDB = data["bot"].rds
        user = await rds.users.get(data["event_context"].user.id)
        if user:
            data["user"] = UserSchema(tg_id=data["event_context"].user.id, **json.loads(user))
            return await handler(event, data)
        else:
            await event.message.answer(f"Вашего id нет среди сотрудников, обратитесь к менеджеру!")



async def register_auth_middleware(dp: Dispatcher) -> None:
    dp.update.middleware(AuthMiddlewareMiddleware())
