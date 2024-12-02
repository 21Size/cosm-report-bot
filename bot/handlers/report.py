import traceback
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from bot.menus.core import make_services_menu
from bot.schemas.user import UserSchema
from bot.states.report import ReportForm

report_router = Router()


@report_router.message(F.text, ReportForm.time)
async def report_time_handler(message: Message, state: FSMContext, services: dict, user: UserSchema):
    try:
        await state.update_data(time=datetime.strptime(message.text, "%H:%M"))
        state_data = await state.get_data()
        await message.answer(
            f"Дата и время записи: {state_data["date"].strftime("%d/%m/%Y")} {state_data["time"].strftime("%H:%M")}\n\n"
            "Выберите услугу (1 уровень):",
            reply_markup=make_services_menu(list(services.keys()), 1, 1)
        )
        await state.set_state(ReportForm.service_lvl_1_index)
    except ValueError as e:
        logger.error(e)
        state_data = await state.get_data()
        await message.answer(
            f"Дата записи: {state_data["date"].strftime("%d/%m/%Y")}\n\n"
            f"‼️Ошибка в формате времени (пример: 18:00), введите еще раз:"
        )
    except Exception as e:
        raise e
