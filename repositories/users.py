
from .base import BaseRepository
from db.users import users
from typing import List ,Optional
from models.user import User,UserIn
from datetime import datetime


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def get_users(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().where(users.c.role == 'user')
        return await self.database.fetch_all(query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id_user==id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_by_nickname(self, nickname: str) -> Optional[User]:
        query = users.select().where(users.c.nickname==nickname)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def is_register(self,id_user):
        query = users.select().where(users.c.id_user == id_user)
        user = await self.database.fetch_one(query)
        if user is None:
            return True
        return False

    async def create(self,id_user,nickname):
        user = UserIn(
            id_user = id_user,
            nickname = nickname,
        )
        values = {**user.dict()}
        query = users.insert().values(**values)
        await self.database.execute(query)
        return user

    async def update_role(self,id:int,role)-> Optional[User]:
        values = {'role':role,'updated_at':datetime.now()}
        query = users.update().where(users.c.id_user==id).values(**values)
        print(query)
        await self.database.execute(query)
        query = users.select().where(users.c.id_user==id)
        user = await self.database.fetch_one(query)
        if user is None:
            return {'error':12,'msg':'User not found'}
        return User.parse_obj(user)
