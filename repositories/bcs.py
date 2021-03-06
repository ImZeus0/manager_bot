from .base import BaseRepository
from db.bcs import bcs
from typing import List ,Optional
from models.bc import BcIn,Bc
from datetime import datetime


class BcRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Bc]:
        query = bcs.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def get_by_agency(self, id_agency) :
        query = bcs.select().where(bcs.c.id_agency == id_agency)
        return await self.database.fetch_all(query)

    async def get_by_id(self,id):
        query = bcs.select().where(bcs.c.id == id)
        res = await self.database.fetch_one(query)
        return Bc.parse_obj(res)

    async def create(self,name,id_agency):
        user = BcIn(
            created_at = datetime.now(),
            name = name,
            id_agency =id_agency,
            updated_at = datetime.now()
        )
        values = {**user.dict()}
        query = bcs.insert().values(**values)
        await self.database.execute(query)
        return user

    async def delete(self,id):
        query = bcs.delete().where(bcs.c.id == id)
        await self.database.execute(query)
        return id