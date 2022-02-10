from .base import BaseRepository
from db.emails import emails
from typing import List ,Optional
from models.email import Email
from datetime import datetime


class EmailRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Email]:
        query = emails.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def get_by_user(self, id_user,agency=None) -> List[Email]:
        if agency is None:
            query = emails.select().where(emails.c.id_user == id_user)
        else:
            query = emails.select().where(emails.c.id_user == id_user).where(emails.c.id_agency == agency)
        return await self.database.fetch_all(query)



    async def create(self,id_agency,id_bc,id_user,email):
        user = Email(
            id_agency = id_agency,
            id_bc = id_bc,
            id_user =id_user,
            created_at = datetime.now(),
            updated_at = datetime.now(),
            status='wait',
            admin=0,
            email=email
        )
        values = {**user.dict()}
        query = emails.insert().values(**values)
        res = await self.database.execute(query)
        return res

    async def get_by_agency_and_bc(self,agency,bc,id_user):
        query = emails.select().where(emails.c.id_agency == agency).\
            where(emails.c.id_bc == bc).\
            where(emails.c.status == 'confirm').\
            where(emails.c.id_user == id_user)
        return await self.database.fetch_all(query)

    async def delete(self,email):
        query = emails.delete().where(emails.c.email == email)
        await self.database.execute(query)

    async def update_status(self,id,status,admin):
        values = {'status': status,'admin':admin,'updated_at':datetime.now()}
        query = emails.update().where(emails.c.id == id).values(**values)
        await self.database.execute(query)
        query = emails.select().where(emails.c.id == id)
        user = await self.database.fetch_one(query)
        if user is None:
            return {'error': 12, 'msg': 'User not found'}
        return Email.parse_obj(user)