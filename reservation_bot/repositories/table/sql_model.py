from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .base import TableRepositoryBase
from reservation_bot.db.models import Table, Reservation

class TableRepositorySQLModel(TableRepositoryBase):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: int) -> Optional[Table]:
        query = select(Table).where(Table.id==id)
        execute_result = await self._session.execute(query)
        return execute_result.scalar_one_or_none()

    async def get_free_from_interval(self, start_datetime: datetime, end_datetime: datetime, offset: int = 0, limit: int = 10) -> List[Table]:
        subquery = (
            select(Reservation)
            .where(
                Reservation.table_id == Table.id,
                Reservation.start_datetime < end_datetime,
                Reservation.end_datetime > start_datetime
            )
            .offset(offset)
            .limit(limit)
        )
        query = (
            select(Table)
            .where(~exists(subquery))
        )
        execute_result = await self._session.execute(query)
        return execute_result.scalars().all()

    async def create(self, table: Table) -> Table:
        self._session.add(table)
        await self._session.commit()
        await self._session.refresh(table)
        return table