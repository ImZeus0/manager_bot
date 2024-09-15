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
    rows.append(['ID','STATUS','TYPE','SERVICE','AMOUNT','CURRENCY','DATE_ACCEPT','PURPOSE'])
    for r in result:
        rows.append([r.id,r.status.value,r.type_operation.value,r.service,r.amount,r.currency,str(r.updated_at),r.purpose])
    write_row_spend(user.nickname,rows)
    await call.answer('Updated')

@dp.callback_query_handler(reg_new_user.filter())
async def user_request(call:CallbackQuery,callback_data:dict,users=UserRepository(database)):
    id_user = int(callback_data.get('id'))
    status = callback_data.get('status')
    user = await users.get_by_id(id_user)
    print(user)
    if user.role != 'wait':
        if status == 'yes':
            answer_text = 'одобрен'
        else:
            answer_text = 'отклонен'
        text = f'🔹{user.nickname} ({user.id_user}) Запрос уже <b>{answer_text}</b>'
        await call.message.answer(text)
        await bot.delete_message(call.message.chat.id,call.message.message_id)
    else:
        if status == 'yes':
            await users.update_role(user.id_user,'user')
            text = '🟢 Заявка одобрена'
        else:
            await users.update_role(user.id_user, 'block')
            text = '🔴 Заявка отклонена'
        await bot.send_message(user.id_user,text)
        await bot.delete_message(call.message.chat.id,call.message.message_id)










