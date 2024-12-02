from aiogram.filters.callback_data import CallbackData


class ServicesPageCallback(CallbackData, prefix="service"):
    lvl: int
    page: int


class SelectServiceCallback(CallbackData, prefix="service"):
    lvl: int
    service_index: int