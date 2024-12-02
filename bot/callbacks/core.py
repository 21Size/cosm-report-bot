from aiogram.filters.callback_data import CallbackData


class MainMenuCallback(CallbackData, prefix="all"):
    type: str = 'mainmenu'
