from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from reservation_bot.di import Container
from reservation_bot.repositories import ReservationRepositoryBase, Reservation, ReservationUpdate

@inject
class ReservationService:
    def __init__(self, repository: ReservationRepositoryBase = Provide[Container.reservation_repository]):
        self._repository = repository

    async def get_by_id(self, id: int) -> Optional[Reservation]:
        return await self._repository.get_by_id(id)

    async def get_by_user(self, user_id: int) -> List[Reservation]:
        return await self._repository.get_by_user(user_id)
    
    async def create(self, reservation: Reservation) -> Reservation:
        return await self._repository.create(reservation)
    
    async def update(self, reservation_update: ReservationUpdate) -> Reservation:
        return await self._repository.update(reservation_update)
    
    async def delete(self, id: int):
        return await self._repository.delete(id)