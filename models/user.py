from pydantic import BaseModel
from typing import Optional
import datetime

class User(BaseModel):
    id:int
    id_user : int
    nickname : str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    role : str

class UserIn(BaseModel):
    id_user : int
    nickname : str
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    role: str= 'user'

