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


@dp.message_handler(commands=['start'], state='*')
async def mainstart(m: Message, state: FSMContext,users = UserRepository(database)):
    await state.finish()
    id = m.chat.id
    user = await users.get_by_id(id)
    await m.delete()
    if user is None:
        await m.answer('Введите свое ФИО')
        await Reg.nickname.set()
    else:
        await m.answer(f'Привет {user.nickname}',reply_markup=main_keyboard(user.role))


@dp.message_handler(state=Reg.nickname)
async def set_name(m:Message,state:FSMContext,users = UserRepository(database),):
    await bot.delete_message(m.chat.id, m.message_id-1)
    await bot.delete_message(m.chat.id, m.message_id)
    await users.create(m.chat.id,m.text)
    user = await users.get_by_id(m.chat.id)
    await m.answer(f'Привет {m.text}', reply_markup=main_keyboard(user.role))
    await state.finish()
    create_list(m.text)


@dp.callback_query_handler(update_table.filter())
async def enter_menu(call:CallbackQuery,callback_data:dict,expenses=ExpensesRepository(database)):
    nickname = callback_data.get('name')
    id_user = int(callback_data.get('id'))
    result = await expenses.get_by_id_user(id_user)
    rows = []
    rows.append(['ID','STATUS','TYPE','SERVICE','AMOUNT','CURRENCY','DATE_ACCEPT'])
    for r in result:
        rows.append([r.id,r.status.value,r.type_operation.value,r.service,r.amount,r.currency,str(r.updated_at)])
    write_row_spend(nickname,rows)
    await call.answer('Updated')




