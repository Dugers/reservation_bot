from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .reservations import Reservation

class Table(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=16)
    short_description: str = Field(max_length=16)
    description: Optional[str] = Field(default=None, max_length=128)

    revervations: List['Reservation'] = Relationship(back_populates="table")