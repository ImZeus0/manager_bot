from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    nickname = State()

class AddAgency(StatesGroup):
    name = State()

class AddBc(StatesGroup):
    name = State()

class AddEmail(StatesGroup):
    email = State()
