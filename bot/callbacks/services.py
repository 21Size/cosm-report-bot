from datetime import datetime
from venv import logger

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendarCallback, SimpleCalendar

from bot.callbacks.schemas.services import ServicesPageCallback, SelectServiceCallback
from bot.menus.core import make_services_menu
from bot.schemas.user import UserSchema
from bot.states.report import ReportForm

services_router = Router()


@services_router.callback_query(F.data.startswith("service_page_"))
async def service_page_callback(
    callback_query: CallbackQuery, state: FSMContext, services: dict, user: UserSchema
):
    lvl = int(callback_query.data.split("_")[-2])
    page = int(callback_query.data.split("_")[-1])

    state_data = await state.get_data()

    if lvl == 1:
        services_names = list(services.keys())
    elif lvl == 2:
        services_names = list(services[state_data["service_lvl_1_name"]].keys())
    else:
        services_names = list(services[state_data["service_lvl_1_name"]][state_data["service_lvl_2_name"]].keys())

    await callback_query.message.edit_reply_markup(reply_markup=make_services_menu(services_names, page, lvl))


@services_router.callback_query(F.data.startswith("select_service_lvl_"))
async def service_select_lvl_callback(
    callback_query: CallbackQuery, state: FSMContext, services: dict, user: UserSchema
):
    lvl = int(callback_query.data.split("_")[-2])
    service_index = int(callback_query.data.split("_")[-1])

    logger.info(f"Try to select service {lvl=} {service_index=}")

    state_data = await state.get_data()

    if lvl < 3:
        if lvl == 1:
            service_lvl_1_name = list(services.keys())[service_index]
            await state.update_data(
                {
                    f"service_lvl_1_index": service_index,
                    f"service_lvl_1_name": service_lvl_1_name,
                }
            )
            services_names = list(services[service_lvl_1_name].keys())
            if not services_names:
                await callback_query.message.edit_text(
                    f"Дата и время записи: {state_data["date"].strftime("%d/%m/%Y")} {state_data["time"].strftime("%H:%M")}\n\n"
                    f"Выбранная услуга:\n\n"
                    f"-{service_lvl_1_name}\n\n"
                    f"Отправьте фото для отчета (чтобы сохранить отчет отправьте любой текст)",
                    reply_markup=None
                )
                await state.set_state(ReportForm.photo)
                return
        else:  #lvl == 2
            service_lvl_1_name = state_data["service_lvl_1_name"]
            service_lvl_2_name = list(services[service_lvl_1_name].keys())[service_index]
            await state.update_data(
                {
                    f"service_lvl_2_index": service_index,
                    f"service_lvl_2_name": service_lvl_2_name,
                }
            )
            services_names = list(services[service_lvl_1_name][service_lvl_2_name].keys())
            if not services_names:
                await callback_query.message.edit_text(
                    f"Дата и время записи: {state_data["date"].strftime("%d/%m/%Y")} {state_data["time"].strftime("%H:%M")}\n\n"
                    f"Выбранная услуга:\n\n"
                    f"-{service_lvl_1_name}\n"
                    f"--{service_lvl_2_name}\n\n"
                    f"Отправьте фото для отчета (чтобы сохранить отчет отправьте любой текст)",
                    reply_markup=None
                )
                await state.set_state(ReportForm.photo)
                return
        await callback_query.answer()
        await callback_query.message.edit_text(
            f"Дата и время записи: {state_data["date"].strftime("%d/%m/%Y")} {state_data["time"].strftime("%H:%M")}\n\n"
            f"Выберите услугу ({lvl+1} уровень):",
            reply_markup=make_services_menu(services_names, 1, lvl+1)
        )
    else:
        service_lvl_1_name = state_data["service_lvl_1_name"]
        service_lvl_2_name = state_data["service_lvl_2_name"]
        service_lvl_3_name = list(services[service_lvl_1_name][service_lvl_2_name].keys())[service_index]
        await state.update_data(
            {
                f"service_lvl_3_index": service_index,
                f"service_lvl_3_name": service_lvl_3_name
            }
        )
        await callback_query.message.edit_text(
            f"Дата и время записи: {state_data["date"].strftime("%d/%m/%Y")} {state_data["time"].strftime("%H:%M")}\n\n"
            f"Выбранная услуга:\n\n"
            f"-{service_lvl_1_name}\n"
            f"--{service_lvl_2_name}\n"
            f"---{service_lvl_3_name}\n\n"
            f"Отправьте фото для отчета (чтобы сохранить отчет отправьте любой текст)",
            reply_markup=None
        )
        await state.set_state(ReportForm.photo)