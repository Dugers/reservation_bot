from aiogram import Router
from aiogram_dialog import Dialog

dialogs: Dialog = [

]

dialogs_router = Router()
if (dialogs):
    dialogs_router.include_routers(*dialogs)