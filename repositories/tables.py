from .base import BaseRepository
from db.add_rk import add_rk
from db.donate_rk import donate_rk
from db.transfer import transfer
from db.spending import spending
from db.withdraw_balance import withdraw_balance
from typing import List ,Optional
from models.tables import Add_rk,DonateRk,TransferRk,WithdrawRk,Spending
from datetime import datetime


class TableRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Add_rk]:
        query = add_rk.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def add_rk(self,id_user,count,email):
        user = Add_rk(
            created_at = datetime.now(),
            updated_at = datetime.now(),
            count = count,
            id_user = id_user,
            admin = 0,
            email = email,
            status = 'wait'
        )
        values = {**user.dict()}
        query = add_rk.insert().values(**values)
        res = await self.database.execute(query)
        return res

    async def update_status_add_rk(self,id,status,admin):
        values = {'status': status,'admin':admin,'updated_at':datetime.now()}
        query = add_rk.update().where(add_rk.c.id == id).values(**values)
        await self.database.execute(query)
        query = add_rk.select().where(add_rk.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return {'error': 12, 'msg': 'User not found'}
        return Add_rk.parse_obj(user)

    async def add_donate_rk(self,id_user,ammount,cabinets,email,id_agency):
        donate = DonateRk(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            ammount=ammount,
            id_user=id_user,
            email=email,
            id_agency = id_agency,
            admin=0,
            cabinets=cabinets,
            status='wait'
        )
        values = {**donate.dict()}
        query = donate_rk.insert().values(**values)
        res = await self.database.execute(query)
        return res

    async def get_all_donate_rk(self):
        query = donate_rk.select().where(donate_rk.c.status == 'confirm')
        res = await self.database.fetch_all(query)
        objs = []
        for r in res:
            objs.append(DonateRk.parse_obj(r))
        return objs


    async def update_status_donate_rk(self,id,status,admin):
        values = {'status': status,'admin':admin,'updated_at':datetime.now()}
        query = donate_rk.update().where(donate_rk.c.id == id).values(**values)
        await self.database.execute(query)
        query = donate_rk.select().where(donate_rk.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return {'error': 12, 'msg': 'User not found'}
        return DonateRk.parse_obj(user)

    async def add_transfer_rk(self,id_user,amount,rk_in,rk_out):
        if amount == 'all':
            amount = 0.0
        t = TransferRk(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            ammount=float(amount),
            id_user=id_user,
            admin=0,
            rk_in=rk_in,
            rk_out =rk_out,
            status='wait'
        )
        values = {**t.dict()}
        query = transfer.insert().values(**values)
        res = await self.database.execute(query)
        return res

    async def update_status_transfer_rk(self,id,status,admin):
        values = {'status': status,'admin':admin,'updated_at':datetime.now()}
        query = transfer.update().where(transfer.c.id == id).values(**values)
        await self.database.execute(query)
        query = transfer.select().where(transfer.c.id == id)
        obj = await self.database.fetch_one(query)
        if obj is None:
            return {'error': 12, 'msg': 'User not found'}
        return TransferRk.parse_obj(obj)

    async def add_withdraw_rk(self,id_user,amount,rk):
        t = WithdrawRk(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            ammount=float(amount),
            id_user=id_user,
            admin=0,
            cabinets=rk,
            status='wait'
        )
        values = {**t.dict()}
        query = withdraw_balance.insert().values(**values)
        res = await self.database.execute(query)
        return res

    async def update_status_withdraw_rk(self,id,status,admin):
        values = {'status': status,'admin':admin,'updated_at':datetime.now()}
        query = withdraw_balance.update().where(withdraw_balance.c.id == id).values(**values)
        await self.database.execute(query)
        query = withdraw_balance.select().where(withdraw_balance.c.id == id)
        obj = await self.database.fetch_one(query)
        if obj is None:
            return {'error': 12, 'msg': 'User not found'}
        return WithdrawRk.parse_obj(obj)


    async def add_spend(self,id_user,spend,count_ban,id_agency):
        t = Spending(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            spend=spend,
            id_agency=id_agency,
            id_user=id_user,
            count_ban=count_ban
        )
        values = {**t.dict()}
        query = spending.insert().values(**values)
        res = await self.database.execute(query)
        return res

    async def get_all_spend(self):
        query = spending.select()
        res = await self.database.fetch_all(query)
        objs = []
        for r in res:
            objs.append(Spending.parse_obj(r))
        return objs
