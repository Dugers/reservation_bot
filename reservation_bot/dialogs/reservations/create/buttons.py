from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Next, Back, Row, Group

from .actions_handlers import on_click_go_to_main_menu, on_click_confirm_button

back_button = Button(text=Const("Назад"), id="back", on_click=Back(), when="has_back")
next_button = Button(text=Const("Продолжить"), id="continue", on_click=Next(), when="has_next")
go_to_main_menu_button = Button(text=Const("Главное меню"), id="go_to_main_menu", on_click=on_click_go_to_main_menu)
confirm_button = Button(text=Const("Забронировать"), id="confirm_button", on_click=on_click_confirm_button, when="has_confirm")

def navigation_buttons() -> Group:
    return Group(
        Row(
            back_button,
            next_button
        ),
        go_to_main_menu_button
    )