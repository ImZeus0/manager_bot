from enums import Enum 

class Operation(str,Enum):
    UpBudget = 'up_budget'
    OtherExpenses = 'other_expenses'
    
class Status(str,Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
