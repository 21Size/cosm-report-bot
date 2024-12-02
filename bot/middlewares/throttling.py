import time
import traceback
from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject, Update
from loguru import logger


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        try:
            if event.callback_query:
                return await handler(event, data)
            else:
                user = f'user{event.message.from_user.id}'

            t_now = int(datetime.now().timestamp() * 1000)

            lock = await self.storage.redis.get(name=f"{user}/lock")
            if lock:
                return

            user_time_marks = await self.storage.redis.scan(match=f"{user}/*")
            time_marks = [int(tm.decode().split("/")[1]) for tm in user_time_marks[1]] if user_time_marks[1] else []

            if time_marks:
                if len([tm for tm in time_marks if tm > (t_now - 60000)]) >= 5:
                    await self.storage.redis.set(name=f"{user}/{t_now}", value=1, ex=60)
                    await self.storage.redis.set(name=f"{user}/lock", value=1, ex=60)
                    await event.message.answer(f"Too many messages. Please wait a minute.")
                    return

                if len([tm for tm in time_marks if tm > (t_now - 3000)]) >= 1:
                    await self.storage.redis.set(name=f"{user}/{t_now}", value=1, ex=60)
                    await self.storage.redis.set(name=f"{user}/lock", value=1, ex=3)
                    await event.message.answer(f"Too many messages. Please wait a second.")
                    return

            await self.storage.redis.set(name=f"{user}/{t_now}", value=1, ex=60)
        except Exception as e:
            logger.warning(traceback.format_exc())

        return await handler(event, data)


async def register_throttling_middleware(dp: Dispatcher) -> None:
    dp.update.middleware(ThrottlingMiddleware(storage=dp.storage))
