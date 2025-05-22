from aiogram.fsm.state import StatesGroup, State

class ReservationInfoSG(StatesGroup):
    main = State()

class ReservationConfigSG(StatesGroup):
    main = State()

class ReservationsListSG(StatesGroup):
    main = State()