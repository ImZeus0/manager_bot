from .base import BaseRepository
from db.agencys import agencys
from typing import List ,Optional
from models.agency import Agency, AgencyIn
from datetime import datetime


class AgencyRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Agency]:
        query = agencys.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def get_by_id(self,id):
        query = agencys.select().where(agencys.c.id == id)
        res = await self.database.fetch_one(query)
        return Agency.parse_obj(res)

    async def create(self,name,currency):
        user = AgencyIn(
            created_at = datetime.now(),
            name = name,
            currency = currency,
            updated_at = datetime.now()
        )
        values = {**user.dict()}
        query = agencys.insert().values(**values)
        await self.database.execute(query)
        return user

    async def delete(self,id):
        query = agencys.delete().where(agencys.c.id == id)
        await self.database.execute(query)
        return id
