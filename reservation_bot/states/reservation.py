from aiogram.fsm.state import StatesGroup, State

class ReservationInfoSG(StatesGroup):
    main = State()

class ReservationCreateSG(StatesGroup):
    guests_count = State()
    start_date = State()
    start_time = State()
    end_time = State()
    table_id = State()

class ReservationEditSG(StatesGroup):
    guests_count = State()
    start_date = State()
    start_time = State()
    end_time = State()
    table_id = State()

class ReservationsListSG(StatesGroup):
    main = State()