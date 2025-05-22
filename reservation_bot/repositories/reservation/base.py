from abc import ABC, abstractmethod
from typing import List, Optional

from db.models import Reservation, ReservationUpdate

class ReservationRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Reservation]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_user(self, user_id: int, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Reservation]:
        raise NotImplementedError()
    
    @abstractmethod
    async def create(self, reservation: Reservation) -> Reservation:
        raise NotImplementedError()
    
    @abstractmethod
    async def update(self, reservation_update: ReservationUpdate) -> Reservation:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete(self, id: int):
        raise NotImplementedError()