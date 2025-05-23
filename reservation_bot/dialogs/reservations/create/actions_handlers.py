from datetime import date, datetime
from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from dependency_injector.wiring import inject, Provide
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar

from .getters import get_start_date, get_start_time, get_end_time, get_guests_count, get_table_id
from reservation_bot.di import Container
from reservation_bot.states import MainSG, ReservationsListSG
from reservation_bot.services import ReservationService, Reservation

async def on_click_go_to_main_menu(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    return await dialog_manager.start(MainSG.main)

async def on_start_date_selected(callback: CallbackQuery, widget: ManagedCalendar, dialog_manager: DialogManager, selected_date: date):
    dialog_manager.dialog_data["start_date"] = selected_date

async def on_table_id_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, table_id: str):
    dialog_manager.dialog_data["table_id"] = int(table_id)

@inject
async def on_click_confirm_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, service: ReservationService = Provide[Container.reservation_service]):
    start_date = get_start_date(dialog_manager)
    start_time = get_start_time(dialog_manager)
    end_time = get_end_time(dialog_manager)
    guests_count = get_guests_count(dialog_manager)
    table_id = get_table_id(dialog_manager)

    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(start_date, end_time)

    try:
        await service.create(Reservation(
                user_tg_id=callback.from_user.id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                count_guests=guests_count,
                table_id=table_id
            )
        )
        await callback.message.answer("Бронирование успешно создано!")
        return await dialog_manager.start(ReservationsListSG.main)
    except:
        await callback.message.answer("Произошла ошибка при создании бронирования\nПопробуйте выбрать другой столик или попробовать позже")

async def time_input_error(message: Message, *args, **kwargs):
    await message.answer("Время введенно не корректно, попробуйте снова")