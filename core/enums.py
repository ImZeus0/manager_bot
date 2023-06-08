from enum import Enum

class Operation(str,Enum):
    UpBudget = 'up_budget'
    OtherExpenses = 'other_expenses'
    Salary = 'salary'

class OperationAgencyAccount(str,Enum):
    CREATE_ACCOUNT = 'create_account'
    UP_BALANCE_ACCOUNT = 'up_balance_account'
    
class Status(str,Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class Currency(str,Enum):
    USDT_TRC_20 = 'usdt_trc_20'
    USDT_ERC_20 = 'usdt_erc_20'

