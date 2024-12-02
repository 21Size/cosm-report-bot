import time
from datetime import datetime
from typing import Any

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.handlers import ErrorHandler
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar
from httpx import AsyncClient
from loguru import logger

from bot.callbacks.core import MainMenuCallback
from bot.schemas.user import UserSchema
from bot.states.report import ReportForm

command_router = Router()


@command_router.message(CommandStart())
@command_router.message(Command("start"))
@command_router.callback_query(MainMenuCallback.filter(F.type == "mainmenu"))
async def command_start_handler(message: Message | CallbackQuery, user: UserSchema) -> None:
    await message.answer(f"Здравствуйте, {user.fio}!")



@command_router.message(Command("report"))
async def command_report_handler(message: Message | CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    calendar = SimpleCalendar(locale="ru_RU.UTF-8", show_alerts=True)
    dt_now = datetime.now()
    calendar.set_dates_range(
        datetime(dt_now.year - 1, 1, 1),
        datetime(dt_now.year + 1, 12, 31)
    )
    await message.answer(
        "Выберите дату записи:",
        reply_markup=await calendar.start_calendar(year=dt_now.year, month=dt_now.month)
    )
    await state.set_state(ReportForm.date)


@command_router.errors()
class MyHandler(ErrorHandler):
    async def handle(self) -> Any:
        logger.exception(f"Cause unexpected exception {self.exception_name}: {self.exception_message}")
        data = {
            "chat_id": 222249912,
            "service": "cosm-report-bot",
            "time": int(time.time()),
            "message": f"\n"
                       f"Exception: {self.exception_message}\n"
        }
        data["message"] += f"\nComment: {self.exception_message}"
        async with AsyncClient() as ac:
            try:
                await ac.post("http://alert-bot:8080/alert", json=data)
            except Exception as e:
                logger.error(e)  # TODO exc