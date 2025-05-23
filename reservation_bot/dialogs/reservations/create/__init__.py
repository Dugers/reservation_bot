from datetime import date
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format, Multi, Case
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Counter, Calendar, CalendarConfig, ScrollingGroup, Select

from .buttons import *
from .getters import *
from .actions_handlers import *
from reservation_bot.states import ReservationCreateSG

MAX_GUESTS = 8
MAX_TABLES = 5

dialog = Dialog(
    Window(
        Const(text="Выберите количество гостей"),
        Counter(
            id="guests_count",
            plus=Const("➕"),
            minus=Const("➖"),
            default=1,
            min_value=1,
            max_value=MAX_GUESTS
        ),
        navigation_buttons(),
        state=ReservationCreateSG.guests_count,
        getter=getter_guests_count
    ),
    Window(
        Multi(
            Const(text="Выберите дату"),
            Format(
                text="Выбранная дата: {start_date}",
                when="{start_date}"
            )
        ),
        Calendar(
            id="start_date",
            on_click=on_start_date_selected,
            config=CalendarConfig(
                min_date=date.today()
            )
        ),
        navigation_buttons(),
        state=ReservationCreateSG.start_date,
        getter=getter_start_date
    ),
    Window(
        Multi(
            Const(text="Введите время в формате час:минута (пример 12:30)"),
            Format(
                text="Введенное время: {start_time_str}", 
                when="start_time"
            )
        ),
        TextInput(
            id="start_time",
            type_factory=factory_time,
            on_error=time_input_error
        ),
        navigation_buttons(),
        state=ReservationCreateSG.start_time,
        getter=getter_start_time
    ),
    Window(
        Multi(
            Const(text="Введите время, до которого вы займете столик в формате час:минута (пример 12:30)"),
            Format(
                text="Введенное время: {end_time_str}", 
                when="end_time"
            ),
            Format(
                text="Введенное время должно быть больше времени, когда начинается бронь\nВремя начала брони {start_time_str}",
                when="end_time_less_start_time"
            ),
            sep="\n\n"
        ),
        TextInput(
            id="end_time",
            type_factory=factory_time,
            on_error=time_input_error
        ),
        navigation_buttons(),
        state=ReservationCreateSG.end_time,
        getter=getter_end_time
    ),
    Window(
        Multi(
            Case(
                {
                    True: Const("Выберите столик"),
                    False: Const("К сожалению, по вашим параметрам нету свободных столиков")
                },
                selector="has_tables"
            ),
            Const("===========================", when="table"),
            Format("Столик: {table.name}", when=lambda data, *args: data["table"] and data["table"].name),
            Format("Описание: {table.description}", when=lambda data, *args: data["table"] and data["table"].description),
            Format("Короткое описание: {table.short_description}", when=lambda data, *args: data["table"] and not data["table"].description and data["table"].short_description),
            Const("==========================="),
            Format("Дата бронирования: {start_date_str} {start_time_str} - {end_time_str}"),
            Format("Количество гостей: {guests_count}")
        ),
        ScrollingGroup(
            Select(
                text=Format(text="{item.name} | {item.short_description}"),
                on_click=on_table_id_selected,
                id="table_select",
                item_id_getter=lambda table: table.id,
                items="tables"
            ),
            id="table_scroll",
            width=1,
            height=MAX_TABLES,
            when="has_tables"
        ),
        confirm_button,
        navigation_buttons(),
        state=ReservationCreateSG.table_id,
        getter=getter_table_id
    )
)