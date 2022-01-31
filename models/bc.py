from pydantic import BaseModel
from typing import Optional
import datetime

class Bc(BaseModel):
    id:int
    id_agency : int
    created_at: Optional[datetime.datetime]
    updated_at : Optional[datetime.datetime]
    name : str


class BcIn(BaseModel):
    id_agency : int
    created_at: Optional[datetime.datetime]
    updated_at : Optional[datetime.datetime]
    name : str