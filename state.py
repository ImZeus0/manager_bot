from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    nickname = State()

class AddAgency(StatesGroup):
    name = State()
    currency = State()

class AddBc(StatesGroup):
    name = State()

class AddEmail(StatesGroup):
    email = State()

class DonateRk(StatesGroup):
    amount = State()
    input_rk = State()

class Transfer(StatesGroup):
    rk_out = State()
    rk_in = State()
    set_amount = State()

class Withdraw(StatesGroup):
    set_rk = State()
    set_amount = State()

class AddSpend(StatesGroup):
    set_spending = State()
    set_count_ban = State()


