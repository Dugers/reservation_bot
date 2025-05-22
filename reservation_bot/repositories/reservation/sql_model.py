from typing import List, Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import ReservationRepositoryBase
from reservation_bot.db.models import Reservation, ReservationUpdate
from reservation_bot.services.logger import combined_logger

class ReservationRepositorySQLModel(ReservationRepositoryBase):
    def __init__(self, session: AsyncSession):
        self._session = session

    @combined_logger()
    async def get_by_id(self, id: int) -> Optional[Reservation]:
        query = select(Reservation).where(Reservation.id==id)
        execute_result = await self._session.execute(query)
        return execute_result.scalar_one_or_none()

    @combined_logger()
    async def get_by_user(self, user_id: int, offset: int = 0, limit: int = 10) -> List[Reservation]:
        query = select(Reservation).where(Reservation.user_tg_id==user_id).offset(offset).limit(limit)
        execute_result = await self._session.execute(query)
        return execute_result.scalars().all()
    
    @combined_logger()
    async def create(self, reservation: Reservation) -> Reservation:
        self._session.add(reservation)
        await self._session.commit()
        await self._session.refresh(reservation)
        return reservation

    @combined_logger()
    async def update(self, reservation_update: ReservationUpdate) -> Reservation:
        reservation = await self.get_by_id(reservation_update.id)
        if (reservation is None):
            raise ValueError(f"Reservation with this id {reservation_update.id} doesn't exist")
        
        update_data = reservation_update.model_dump(exclude_none=True, exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(reservation, key, value)

        await self._session.commit()
        await self._session.refresh(reservation)
        return reservation

    @combined_logger()
    async def delete(self, id: int):
        query = delete(Reservation).where(Reservation.id==id)
        await self._session.execute(query)
        await self._session.commit()