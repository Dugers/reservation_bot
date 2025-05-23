from datetime import datetime
from typing import Optional
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from dependency_injector.wiring import inject, Provide
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Button, Cancel, Row

from reservation_bot.di import Container
from reservation_bot.services import ReservationService
from reservation_bot.states import ReservationInfoSG, MainSG, ReservationEditSG

def get_reservation_id(dialog_manager: DialogManager) -> Optional[int]:
    return dialog_manager.start_data.get("id")

@inject
async def getter(dialog_manager: DialogManager, service: ReservationService = Provide[Container.reservation_service], **kwargs):    
    reservation_id = get_reservation_id(dialog_manager)
    if (not reservation_id or not isinstance(reservation_id, int)):
        raise RuntimeError("Reservation id doesn't provide")
    
    reservation = await service.get_by_id(reservation_id)
    if (reservation is None):
        raise RuntimeError("Reservation with this id doesn't exist")
    
    return {
        "reservation": reservation,
        "start_date_str": reservation.start_datetime.date(),
        "start_time_str": reservation.start_datetime.time().strftime("%H:%M"),
        "end_time_str": reservation.end_datetime.time().strftime("%H:%M"),
        "not_expired": reservation.start_datetime > datetime.now()
    }

async def on_click_go_to_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    return await dialog_manager.start(MainSG.main)

async def on_click_update(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    pass

@inject
async def on_click_cancel(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, service: ReservationService = Provide[Container.reservation_service]):
    try:
        reservation_id = get_reservation_id(dialog_manager)
        await service.delete(reservation_id)
        await callback.message.answer("Бронирование успешно отменено")
        await dialog_manager.done()
    except:
        await callback.message.answer("Произошла ошибка при отмене бронирования\nПопробуйте снова позже")

dialog = Dialog(
    Window(
        Multi(
            Format("Дата и время: {start_date_str} {start_time_str} - {end_time_str}"),
            Format("Количество гостей {reservation.count_guests}"),
            Const("==============================================="),
            Format("Столик: {reservation.table.name}"),
            Format("Описание: {reservation.table.description}", when=lambda data, *arr: data["reservation"].table.description),
            Format("Краткое описание: {reservation.table.short_description}", when=lambda data, *arr: not data["reservation"].table.description)
        ),
        Row(
            Button(Const("Изменить"), id="update", on_click=on_click_update),
            Button(Const("Отменить"), id="cancel", on_click=on_click_cancel),
            when="not_expired"
        ),
        Button(Const("Главное меню"), id="go_to_main_menu", on_click=on_click_go_to_main_menu),
        Button(Const("Назад"), id="go_back", on_click=Cancel()),
        state=ReservationInfoSG.main,
        getter=getter
    )
)