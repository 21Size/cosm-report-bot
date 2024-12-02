import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import main_router
from bot.logs.setup_loguru import setup_logger
from bot.middlewares import register_all_middlewares
from bot.config import settings
from bot.rds import RedisDB


async def main() -> None:
    bot = Bot(settings.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot.rds = RedisDB(settings)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)

    await register_all_middlewares(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logger(ignored=["aioboto3", "boto3", "botocore", "s3transfer", "urllib3"])
    asyncio.run(main())
