from aiogram import Router

from bot.callbacks.date import calendar_router
from bot.callbacks.services import services_router
from bot.handlers.commands import command_router
from bot.handlers.photo import photo_router
from bot.handlers.report import report_router

main_router = Router()
main_router.include_routers(command_router)
main_router.include_routers(calendar_router)
main_router.include_routers(report_router)
main_router.include_routers(services_router)
main_router.include_routers(photo_router)
