import asyncio

from data_parser.config import settings
from data_parser.gsheets.gsheets import gs
from data_parser.rds import RedisDB
from data_parser.services.parser import ParseDataService


async def main():
    rds = RedisDB(settings)
    await ParseDataService(settings, gs, rds).process()
    await rds.close_connections()

if __name__ == '__main__':
    asyncio.run(main())