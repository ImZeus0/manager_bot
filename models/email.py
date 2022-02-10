from pydantic import BaseModel
from typing import Optional
import datetime

class Email(BaseModel):
    id_agency : int
    id_bc:int
    id_user:int
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    status : str
    admin : int
    email : str
