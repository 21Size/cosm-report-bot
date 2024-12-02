from typing import Callable, Awaitable, Dict, Any

from aioboto3 import Session
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update

from bot.config import settings


class S3MiddlewareMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        session = Session()
        data["s3_session"] = session
        return await handler(event, data)

async def register_s3_middleware(dp: Dispatcher) -> None:
    dp.update.middleware(S3MiddlewareMiddleware())
