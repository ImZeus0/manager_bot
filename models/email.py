from pydantic import BaseModel
from typing import Optional
import datetime

class Email(BaseModel):
    id_agency : int
    id_bc:int
    id_user:int
    created_at: Optional[datetime.date]
    name : str
