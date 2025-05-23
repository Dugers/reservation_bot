from dependency_injector import containers, providers

from reservation_bot.db.connection import get_session
from reservation_bot.repositories.table.sql_model import TableRepositorySQLModel
from reservation_bot.repositories.reservation.sql_model import ReservationRepositorySQLModel

class Container(containers.DeclarativeContainer):
    session_provider = providers.Resource(get_session)

    table_repository = providers.Factory(
        TableRepositorySQLModel,
        session=session_provider
    )

    reservation_repository = providers.Factory(
        ReservationRepositorySQLModel,
        session=session_provider
    )

container = Container()