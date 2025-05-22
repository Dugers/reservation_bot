from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .base import TableRepositoryBase
from reservation_bot.db.models import Table, Reservation
from reservation_bot.services.logger import combined_logger

class TableRepositorySQLModel(TableRepositoryBase):
    def __init__(self, session: AsyncSession):
        self._session = session

    @combined_logger()
    async def get_by_id(self, id: int) -> Optional[Table]:
        query = select(Table).where(Table.id==id)
        execute_result = await self._session.execute(query)
        return execute_result.scalar_one_or_none()

    @combined_logger()
    async def get_free_from_interval(self, start_datetime: datetime, end_datetime: datetime, offset: int = 0, limit: int = 10) -> List[Table]:
        subquery = (
            select(Reservation)
            .where(
                Reservation.table_id == Table.id,
                Reservation.start_datetime < end_datetime,
                Reservation.end_datetime > start_datetime
            )
        )
        query = (
            select(Table)
            .where(~exists(subquery))
            .offset(offset)
            .limit(limit)
        )
        execute_result = await self._session.execute(query)
        return execute_result.scalars().all()

    @combined_logger()
    async def create(self, table: Table) -> Table:
        self._session.add(table)
        await self._session.commit()
        await self._session.refresh(table)
        return table