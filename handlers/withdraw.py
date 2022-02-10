from db.base import database
from models.agency import Agency
from models.bc import Bc
from models.email import Email
from repositories.agencys import AgencyRepository
from repositories.bcs import BcRepository
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from datetime import datetime
from keyboard import *
from repositories.emails import EmailRepository
from repositories.tables import TableRepository
from state import *
from core.config import *
from aiogram.types.callback_query import CallbackQuery
from repositories.users import UserRepository

@dp.callback_query_handler(text_contains='take_out_the_balance')
async def starttransfer(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()
    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys,'withdraw'))

@dp.callback_query_handler(agencys_for_withdraw_rk.filter())
async def setagencyforwithdraw(call: CallbackQuery, state:FSMContext,callback_data: dict):
    id_agency = callback_data.get('id')
    await state.update_data(id_agency=id_agency)
    await call.message.edit_text('Введите РК  с которого нужно снять деньги. Можно указывать как один так и множесвто сразу.')
    await Withdraw.set_rk.set()

@dp.message_handler(state=Withdraw.set_rk)
async def setamountwithdraw(m:Message,state:FSMContext):
    rk = m.text
    await state.update_data(rk=rk)
    await m.answer('Укажите сумму снятия для одного РК или весь баланс для множества.',reply_markup=all_amount_withdraw())
    await Withdraw.set_amount.set()

@dp.callback_query_handler(text_contains ='allamoountwithdraw',state=Withdraw.set_amount)
async def setallbalancewithdraw(call:CallbackQuery,state:FSMContext,agencys = AgencyRepository(database),users = UserRepository(database),table = TableRepository(database)):
    data = await state.get_data()
    await state.finish()
    user = await users.get_by_id(call.message.chat.id)
    agency = await agencys.get_by_id(int(data['id_agency']))
    id_request = await table.add_withdraw_rk(call.message.chat.id,0,data['rk'].replace('\n','/'))
    msg = f"#{user.nickname} №{id_request} агентство {agency.name}\nСнять деньги на общий баланс с\n<b>{data['rk']}</b> Весь баланс"
    await bot.send_message(CHAT_ID, msg, reply_markup=send_request(id_request, call.message.chat.id, 'transfer'))
    await call.message.edit_text(f'Ваша заявка <b>№{id_request}</b> отправлена', reply_markup=main_keyboard(user.role))

@dp.message_handler(state=Withdraw.set_amount)
async def setamountwithdraw(m:Message,state:FSMContext,agencys = AgencyRepository(database),users = UserRepository(database),table = TableRepository(database)):
    amount = ''
    try:
        amount = float(m.text)
    except Exception:
        await m.answer('Неверно указано число, попробуйте ещё раз')
        return
    data = await state.get_data()
    await state.finish()
    user = await users.get_by_id(m.chat.id)
    agency = await agencys.get_by_id(int(data['id_agency']))
    id_request = await table.add_withdraw_rk(m.chat.id,amount, data['rk'].replace('\n', '/'))
    msg = f"#{user.nickname} №{id_request} агентство {agency.name}\nСнять деньги на общий баланс с <b>{data['rk']}</b> на {str(amount)}"
    await bot.send_message(CHAT_ID, msg, reply_markup=send_request(id_request, m.chat.id, 'withdraw'))
    await m.answer(f'Ваша заявка <b>№{id_request}</b> отправлена', reply_markup=main_keyboard(user.role))

@dp.callback_query_handler(send_request_withdraw_rk_callback.filter())
async def setwitrdrawcounfirm(call:CallbackQuery,callback_data:dict,users= UserRepository(database),
                             tables = TableRepository(database)):
    id_request = callback_data.get('id')
    status = callback_data.get('status')
    admin = call.from_user.id
    admin_user = await users.get_by_id(admin)
    sender = callback_data.get('sender')
    await tables.update_status_withdraw_rk(int(id_request), status, admin)
    if status == 'confirm':
        msg = f'Ваша заявка №{id_request} Снять деньги на общий баланс <b>ОДОБРЕНА</b> #{admin_user.nickname}'
    else:
        msg = f'Ваша заявка №{id_request} Снять деньги на общий баланс <b>ОТКЛОНЕНА</b> #{admin_user.nickname}'
    await bot.send_message(int(sender), msg)
    await call.message.edit_reply_markup(seached(status))


