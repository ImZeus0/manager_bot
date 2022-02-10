from pydantic import BaseModel
from typing import Optional
import datetime

class Agency(BaseModel):
    id:int
    name : str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    currency : str

class AgencyIn(BaseModel):
    name : str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    currency : str

