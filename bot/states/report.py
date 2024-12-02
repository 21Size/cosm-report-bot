from aiogram.fsm.state import StatesGroup, State


class ReportForm(StatesGroup):
    date = State()
    time = State()
    service_lvl_1_index = State()
    service_lvl_1_name = State()
    service_lvl_2_index = State()
    service_lvl_2_name = State()
    service_lvl_3_index = State()
    service_lvl_3_name = State()
    photo = State()