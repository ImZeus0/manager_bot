from pydantic import BaseModel
from typing import Optional
import datetime
from core.enums import Operation, Status


class Expense(BaseModel):
    id: Optional[str] = None
    id_user: int
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    type_operation: Operation
    service: str
    amount: float
    currency: str
    purpose: str
    account_number:Optional[str] = None
    payment_key: str
    status: Status
