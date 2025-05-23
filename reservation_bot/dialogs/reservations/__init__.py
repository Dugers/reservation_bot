from aiogram_dialog import Dialog

from .list import dialog as list_dialog
from .create import dialog as create_dialog
from .info import dialog as info_dialog

dialogs: Dialog = [
    list_dialog,
    create_dialog,
    info_dialog
]