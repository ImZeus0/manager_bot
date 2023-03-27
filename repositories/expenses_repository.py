from datetime import datetime

from core.enums import Status
from .base import BaseRepository
from db.expenses import expenses
from typing import List ,Optional
from models.expenses import Expense



class ExpensesRepository(BaseRepository):

    async def get_all(self) -> List[Expense]:
        query = expenses.select()
        return await self.database.fetch_all(query)

    async def create(self,expense):
        values = {**expense.dict()}
        del values['id']
        query = expenses.insert().values(**values)
        data = await self.database.execute(query)
        return data

    async def get_by_id_user(self,id_user) -> List[Expense]:
        query = expenses.select().where(expenses.c.id_user==id_user)
        data =  await self.database.fetch_all(query)
        res = []
        for d in data:
            res.append(Expense.parse_obj(d))
        return res

    async def update_status(self,status,id_request):
        values = {'status': status,'updated_at':datetime.now()}
        query = expenses.update().where(expenses.c.id == id_request).values(**values)
        await self.database.execute(query)
        query = expenses.select().where(expenses.c.id  == id_request)
        expense = await self.database.fetch_one(query)
        return expense
