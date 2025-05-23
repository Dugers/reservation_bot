from aiogram.fsm.state import StatesGroup, State

class ReservationInfoSG(StatesGroup):
    main = State()

class ReservationConfigBaseSG(StatesGroup):
    guests_count = State()
    start_datetime = State()
    end_datetime = State()

class ReservationCreateSG(ReservationConfigBaseSG):
    table_id = State()

class ReservationEditSG(ReservationConfigBaseSG):
    pass

class ReservationsListSG(StatesGroup):
    main = State()