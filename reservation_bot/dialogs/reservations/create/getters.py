from datetime import date, datetime
from datetime import time
from typing import Optional
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import ManagedCounter
from dependency_injector.wiring import Provide, inject

from reservation_bot.di import Container
from reservation_bot.services import TableService

def get_guests_count(dialog_manager: DialogManager) -> int:
    widget: ManagedCounter = dialog_manager.find("guests_count")
    return int(widget.get_value())

def get_start_date(dialog_manager: DialogManager) -> Optional[date]:
    return dialog_manager.dialog_data.get("start_date")

def get_start_time(dialog_manager: DialogManager) -> Optional[time]:
    widget: ManagedTextInput = dialog_manager.find("start_time")
    return widget.get_value()

def get_end_time(dialog_manager: DialogManager) -> Optional[time]:
    widget: ManagedTextInput = dialog_manager.find("end_time")
    return widget.get_value()

def get_table_id(dialog_manager: DialogManager) -> Optional[int]:
    return dialog_manager.dialog_data.get("table_id")

async def getter_guests_count(dialog_manager: DialogManager, **kwargs):
    guests_count = get_guests_count(dialog_manager)
    return {
        "guests_count": guests_count,
        "has_next": True
    }

async def getter_start_date(dialog_manager: DialogManager, **kwargs):
    start_date = get_start_date(dialog_manager)
    return {
        "start_date": start_date,
        "has_back": True,
        "has_next": start_date
    }

async def getter_start_time(dialog_manager: DialogManager, **kwargs):
    start_time = get_start_time(dialog_manager)
    return {
        "has_back": True,
        "start_time": start_time,
        "start_time_str": start_time.strftime("%H:%M") if start_time else "",
        "has_next": start_time
    }

async def getter_end_time(dialog_manager: DialogManager, **kwargs):
    start_time = get_start_time(dialog_manager)
    end_time = get_end_time(dialog_manager)
    end_time_less_start_time = end_time <= start_time if end_time else False
    return {
        "has_back": True,
        "start_time": start_time,
        "start_time_str": start_time.strftime("%H:%M") if start_time else "",
        "end_time": end_time,
        "end_time_str": end_time.strftime("%H:%M") if end_time else "",
        "end_time_less_start_time": end_time_less_start_time,
        "has_next": end_time and not end_time_less_start_time
    }

@inject
async def getter_table_id(dialog_manager: DialogManager, service: TableService = Provide[Container.table_service], **kwargs):
    start_date = get_start_date(dialog_manager)
    start_time = get_start_time(dialog_manager)
    end_time = get_end_time(dialog_manager)
    guests_count = get_guests_count(dialog_manager)
    table_id = get_table_id(dialog_manager)

    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(start_date, end_time)
    tables = await service.get_free_from_interval(start_datetime, end_datetime)

    table = None
    if (table_id):
        table = list(filter(lambda table : table.id == table_id, tables))[0]

    return {
        "has_back": True,
        "guests_count": guests_count,
        "start_date_str": start_date.strftime("%d.%m.%Y"),
        "start_time_str": start_time.strftime("%H:%M"),
        "end_time_str": end_time.strftime("%H:%M"),
        "tables": tables,
        "table_id": table_id,
        "table": table,
        "has_tables": bool(len(tables)),
        "has_confirm": table_id
    }

def factory_time(value) -> time:
    return datetime.strptime(value, "%H:%M").time()