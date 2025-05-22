from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from db.models import Table

class TableRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[Table]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_free_from_interval(self, start_datetime: datetime, end_datetime: datetime, offset: Optional[int] = None, limit: Optional[int] = None) -> List[Table]:
        raise NotImplementedError()
    
    @abstractmethod
    async def create(self, table: Table) -> Table:
        raise NotImplementedError()