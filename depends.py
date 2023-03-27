from repositories.users import UserRepository
from repositories.expenses_repository import  ExpensesRepository
from db.base import database

def get_user_repository() -> UserRepository:
    return UserRepository(database)

def get_expenses_repository() -> ExpensesRepository:
    return ExpensesRepository(database)