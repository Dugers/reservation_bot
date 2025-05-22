from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager

from reservation_bot.dialogs import start_main_dialog

welcome_router = Router()

@welcome_router.message(Command(commands="start"))
async def welcome_handler(message: Message, dialog_manager: DialogManager):
    return await start_main_dialog(dialog_manager)