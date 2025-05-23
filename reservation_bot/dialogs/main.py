from aiogram_dialog import Dialog, DialogManager, Window
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Row, Button

from reservation_bot.states import MainSG, ReservationsListSG, ReservationCreateSG

async def getter(dialog_manager: DialogManager, *args, **kwargs):
    return {"user": dialog_manager.event.from_user}

def on_click_book(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    return dialog_manager.start(ReservationCreateSG.guests_count)

def on_click_book_list(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    return dialog_manager.start(ReservationsListSG.main)

dialog = Dialog(
    Window(
        Format("Добро пожаловать, {user.full_name}!"),
        Row(
            Button(Const("🕑 Забронировать столик"), id="book",
                   on_click=on_click_book_list),
            Button(Const("📖 Мои бронирования"), id="book_list",
                on_click=on_click_book_list)
        ),
        state=MainSG.main,
        getter=getter
    )
)