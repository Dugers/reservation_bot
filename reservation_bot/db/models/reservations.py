from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .tables import Table

class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_tg_id: int
    start_datetime: datetime
    end_datetime: datetime

    table_id: int = Field(foreign_key="table.id")
    table: 'Table' = Relationship(back_populates="reservations")