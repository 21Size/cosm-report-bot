from loguru import logger
from redis.asyncio import Redis

from data_parser.config import Settings


class RedisDB:
    def __init__(self, settings: Settings):
        logger.info("Connecting to redis...")
        self.settings = settings

        self.users = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password,
            db=settings.redis.users_db,
        )
        logger.info(f"Redis users({settings.redis.users_db}) connected")

        self.services = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password,
            db=settings.redis.services_db,
        )
        logger.info(f"Redis services({settings.redis.services_db}) connected")

        self.tg_storage = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            password=settings.redis.password,
            db=settings.redis.tg_storage_db,
        )
        logger.info(f"Redis tg_storage({settings.redis.tg_storage_db}) connected")

    async def close_connections(self):
        await self.users.close()
        await self.services.close()
        await self.tg_storage.close()
        logger.info("Redis connections closed")
