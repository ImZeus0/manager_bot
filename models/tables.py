from pydantic import BaseModel
from typing import Optional
import datetime


class Add_rk(BaseModel):
    created_at : Optional[datetime.datetime]
    updated_at :Optional[datetime.datetime]
    count :int
    id_user :int
    admin :int
    email :str
    status : str

class DonateRk(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    id_user: int
    admin: int
    email:str
    id_agency:int
    status: str
    ammount: float
    cabinets:str

class TransferRk(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    id_user: int
    admin: int
    status: str
    ammount: float
    rk_in: str
    rk_out: str

class WithdrawRk(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    id_user: int
    admin: int
    status: str
    ammount: float
    cabinets:str

class Spending(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    id_user: int
    id_agency:int
    spend : float
    count_ban : int



