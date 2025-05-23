from aiogram import Router
from aiogram_dialog import Dialog, DialogManager

from .main import dialog as main_dialog
from .reservations_list import dialog as reservations_list_dialog
from reservation_bot.states import MainSG

dialogs: Dialog = [
    main_dialog,
    reservations_list_dialog
]

dialogs_router = Router()
if (dialogs):
    dialogs_router.include_routers(*dialogs)

async def start_main_dialog(dialog_manager: DialogManager):
    await dialog_manager.start(MainSG.main)