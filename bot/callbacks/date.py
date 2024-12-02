from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram_calendar import SimpleCalendarCallback, SimpleCalendar

from bot.schemas.user import UserSchema
from bot.states.report import ReportForm

calendar_router = Router()


@calendar_router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(
    callback_query: CallbackQuery, callback_data: SimpleCalendarCallback, state: FSMContext, user: UserSchema
):
    calendar = SimpleCalendar(locale="ru_RU.UTF-8", show_alerts=True)
    dt_now = datetime.now()
    calendar.set_dates_range(
        datetime(dt_now.year - 1, 1, 1),
        datetime(dt_now.year + 1, 12, 31)
    )
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.edit_text(
            f'Дата записи: {date.strftime("%d/%m/%Y")}\n\n'
            f'Введите время записи (пример: 18:00):',
            reply_markup=None
        )
        await state.update_data(date=date)
        await state.set_state(ReportForm.time)