from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Row, Select
from aiogram_dialog.widgets.text import Const, Format
from dependency_injector.wiring import inject, Provide

from reservation_bot.services import ReservationService
from reservation_bot.states import MainSG, ReservationsListSG, ReservationInfoSG
from reservation_bot.di import Container

PAGE_SIZE = 5

@inject
async def getter(dialog_manager: DialogManager, service: ReservationService = Provide[Container.reservation_service], **kwargs):
    getter_data = {}

    user_id = dialog_manager.event.from_user.id
    reservations = await service.get_by_user(user_id)

    getter_data["reservations"] = [{
        "id": reservation.id,
        "table": {
            "name": reservation.table.name
        },
        "start_date_str": str(reservation.start_datetime.date()),
        "start_time_str": reservation.start_datetime.time().strftime("%H:%M"),
        "end_time_str": reservation.end_datetime.time().strftime("%H:%M")
    } for reservation in reservations]
    getter_data["has_reservations"] = bool(len(reservations))
    
    return getter_data

async def on_click_go_to_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    return await dialog_manager.start(MainSG.main)

async def on_click_scrolling_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, reservation_id: str):
    return await dialog_manager.start(ReservationInfoSG.main, data={id: int(reservation_id)})

dialog = Dialog(Window(
    Const(
        text="Ваши бронирования:",
        when="has_reservations"
    ),
    Const(
        text="У вас нету бронирований",
        when=lambda data, *args: not data.get("has_reservations", False)
    ),
    ScrollingGroup(
        Select(
            Format("{item[table][name]} | {item[start_date_str]} {item[start_time_str]} - {item[end_time_str]}"),
                id="scrolling_button",
                item_id_getter=lambda item: item["id"],
                items="reservations",
                on_click=on_click_scrolling_button,
        ),
        id="scrolling_group",
        width=1,
        height=PAGE_SIZE,
        when="has_reservations"
    ),
    Row(
        Button(
            text=Const("Главное меню"),
            id="go_to_main_menu",
            on_click=on_click_go_to_main_menu
        )
    ),
    state=ReservationsListSG.main,
    getter=getter
))