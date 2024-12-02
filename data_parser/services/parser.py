import asyncio
import json
import traceback
import pprint

from loguru import logger
from pygsheets import Worksheet

from data_parser.config import Settings
from data_parser.utils.alerts import send_alert_to_tg_bot
from data_parser.gsheets.gsheets import GSheets
from data_parser.rds import RedisDB


class ParseDataService:
    def __init__(self, settings: Settings, gsheets: GSheets, rds: RedisDB):
        self.settings = settings
        self.client = gsheets.client
        self.rds = rds

    def build_nested_dict(self, data: list[dict]):
        nested_dict = {}
        lvl1 = lvl2 = lvl3 = ''
        for record in data:
            lvl1 = record['уровень 1']
            lvl2 = record['уровень 2']
            lvl3 = record['уровень 3']

            # Обработка уровня 1
            if lvl1:
                if lvl1 not in nested_dict:
                    nested_dict[lvl1] = {}

            # Обработка уровня 2
            if lvl2:
                if lvl2 not in nested_dict[lvl1]:
                    nested_dict[lvl1][lvl2] = {}

            # Обработка уровня 3
            if lvl3:
                if lvl3 not in nested_dict[lvl1][lvl2]:
                    nested_dict[lvl1][lvl2][lvl3] = {}

        return nested_dict

    async def process(self):
        while True:
            try:
                logger.info('Start parsing')
                sh = self.client.open_by_key(self.settings.gsheets.cosm_table_id)

                logger.info("Processing users")
                wks: Worksheet = sh.worksheet_by_title("Лист1")
                records = wks.get_all_records()

                users_data = {}
                for record in records:
                    if record["tg_id"]:
                        users_data[record["tg_id"]] = json.dumps(
                            {
                                "city": record['Город клиники'],
                                "address": record['Адрес клиники'],
                                "fio": record['ФИО специалиста'],
                                "nickname": record['Ник в Telegram'],
                            }
                        )

                await self.rds.users.mset(users_data)
                logger.success('Users data is saved')

                logger.info("Processing services")
                wks: Worksheet = sh.worksheet_by_title("теги процедур")
                records = wks.get_all_records()

                logger.info(pprint.pformat(records))

                services_data = self.build_nested_dict(records)
                logger.info(pprint.pformat(services_data))

                await self.rds.services.set("services", json.dumps(services_data))

                # pprint.pprint(users_data)
            except Exception as e:
                logger.error(traceback.format_exc())
                # await send_alert_to_tg_bot("ParseDataService", e, "parse users error")
            await asyncio.sleep(3600)


