from .base import BaseRepository
from db.agencys import agencys
from typing import List ,Optional
from models.agency import Agency
from datetime import datetime


class AgencyRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Agency]:
        query = agencys.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def create(self,name):
        user = Agency(
            created_at = datetime.now(),
            name = name,
            updated_at = datetime.now()
        )
        values = {**user.dict()}
        query = agencys.insert().values(**values)
        await self.database.execute(query)
        return user