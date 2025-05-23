from datetime import datetime
from typing import List, Optional

from reservation_bot.repositories import TableRepositoryBase, Table

class TableService:
    def __init__(self, repository: TableRepositoryBase):
        self._repository = repository

    async def get_by_id(self, id: int) -> Optional[Table]:
        return await self._repository.get_by_id(id)
    
    async def get_free_from_interval(self, start_datetime: datetime, end_datetime: datetime) -> List[Table]:
        return await self._repository.get_free_from_interval(start_datetime, end_datetime)
    
    async def create(self, table: Table) -> Table:
        return await self._repository.create(table)