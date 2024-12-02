import io

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger
from yadisk import AsyncClient
from yadisk.exceptions import PathExistsError

from bot.config import settings
from bot.schemas.user import UserSchema
from bot.states.report import ReportForm

photo_router = Router()

@photo_router.message(ReportForm.photo)
async def report_photo_handler(
    message: Message, state: FSMContext, user: UserSchema, ydisk: AsyncClient
):
    logger.info(message.photo)

    state_data = await state.get_data()
    service_lvl_1 = state_data["service_lvl_1_name"]
    service_lvl_2 = state_data.get("service_lvl_2_name") + "/" if state_data.get("service_lvl_2_name") else ""
    service_lvl_3 = state_data.get("service_lvl_3_name") + "/" if state_data.get("service_lvl_3_name") else ""

    disk_path = (
        f"{user.city}/{user.address}/{user.fio}/"
        f"{service_lvl_1}/{service_lvl_2}{service_lvl_3}"
        f"{state_data['date'].strftime('%Y-%m-%d')}/{state_data['time'].strftime('%H:%M')}"
    )

    if message.photo:
        # async with s3_session.client(
        #     service_name='s3',
        #     endpoint_url='https://storage.yandexcloud.net',
        #     aws_access_key_id=settings.s3.access_key_id,
        #     aws_secret_access_key=settings.s3.secret_access_key,
        #     region_name=settings.s3.region_name
        # ) as s3:
        #     file_id = message.photo[-1].file_id
        #     file = await message.bot.get_file(file_id)
        #     file_path = file.file_path
        #     logger.info(file_path)
        #     result: io.BytesIO | None = await message.bot.download_file(file_path)
        #
        #     await s3.upload_fileobj(
        #         result,
        #         settings.s3.bucket_name,
        #         f"{disk_path}/{file_path.split('/')[-1]}",
        #     )
        file_id = message.photo[-1].file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        result: io.BytesIO | None = await message.bot.download_file(file_path)

        async with ydisk:
            logger.info(f"Try to create path: {disk_path}")
            for i in range(len(disk_path.split("/"))):
                try:
                    logger.info(f"{i+1} | Try to create: {"/".join(disk_path.split("/")[0:i+1])}")
                    await ydisk.mkdir("/".join(disk_path.split("/")[0:i+1]))
                except PathExistsError:
                    pass
            await ydisk.upload(result, f"{disk_path}/{file_path.split('/')[-1]}")

    if message.text:
        await state.clear()
        await message.answer(f"Отчет сохранен по пути: {disk_path}")
