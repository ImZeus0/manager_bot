from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    nickname = State()


class AddExpenses(StatesGroup):
    amount = State()
    purpose = State()
    payment_key = State()
    account_number = State()
