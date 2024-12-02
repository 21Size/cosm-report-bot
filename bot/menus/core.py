from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.callbacks.core import MainMenuCallback
from bot.callbacks.schemas.services import ServicesPageCallback


def make_main_menu_keyboard() -> InlineKeyboardMarkup:
    buy_btn = InlineKeyboardButton(text="Buy", callback_data="menu_buy")
    sell_btn = InlineKeyboardButton(text="Sell", callback_data="menu_sell")
    settings_btn = InlineKeyboardButton(text="Settings", callback_data="menu_settings")
    refresh_btn = InlineKeyboardButton(text="Refresh", callback_data="menu_refresh")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [buy_btn, sell_btn],
            [settings_btn],
            [refresh_btn]
        ]
    )


def make_help_menu() -> InlineKeyboardMarkup:
    main_menu_btn = InlineKeyboardButton(text="Main Menu", callback_data=MainMenuCallback().pack())
    return InlineKeyboardMarkup(inline_keyboard=[[main_menu_btn]])


def make_go_back_btn() -> InlineKeyboardMarkup:
    go_back_btn = InlineKeyboardButton(text="Go Back", callback_data="main_menu")
    return InlineKeyboardMarkup(inline_keyboard=[[go_back_btn]])

def make_services_menu(services: list[str], page: int, lvl: int) -> InlineKeyboardMarkup:
    assert lvl in [1, 2, 3]
    assert page > 0

    buttons = []
    length = len(services)

    if length > 10:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=" " if page == 1 else "<-",
                    callback_data="_" if page == 1 else f"service_page_{lvl}_{page-1}",
                ),
                InlineKeyboardButton(
                    text=" " if length <= page*10 else "->",
                    callback_data="_" if length <= page*10 else f"service_page_{lvl}_{page+1}"
                ),
            ]
        )

    buttons += [
        [InlineKeyboardButton(text=x, callback_data=f"select_service_lvl_{lvl}_{i}")]
        for i, x in enumerate(services[(page-1)*10:page*10])
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



go_back_button = make_go_back_btn()
main_menu_keyboard = make_main_menu_keyboard()
help_menu_keyboard = make_help_menu()
