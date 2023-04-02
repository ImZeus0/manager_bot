from db.base import database
from google_sheet import create_list, write_row_spend
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from keyboards.main_keyboard import *
from keyboards.admin_keyboards import *
from keyboards.send_requests_keyboards import *
from repositories.expenses_repository import ExpensesRepository
from state import *
from aiogram.types.callback_query import CallbackQuery
from repositories.users import UserRepository



@dp.callback_query_handler(update_table.filter())
async def enter_menu(call:CallbackQuery,callback_data:dict,users=UserRepository(database),expenses=ExpensesRepository(database)):
    id_user = int(callback_data.get('id'))
    user = await users.get_by_id(id_user)
    result = await expenses.get_by_id_user(id_user)
    rows = []
    rows.append(['ID','STATUS','TYPE','SERVICE','AMOUNT','CURRENCY','DATE_ACCEPT'])
    for r in result:
        rows.append([r.id,r.status.value,r.type_operation.value,r.service,r.amount,r.currency,str(r.updated_at)])
    write_row_spend(user.nickname,rows)
    await call.answer('Updated')





