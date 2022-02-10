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

@dp.callback_query_handler(text_contains='transfer_balance')
async def starttransfer(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()
    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys, 'transfer'))

@dp.callback_query_handler(agencys_for_transfer_rk.filter())
async def setemailfortransfer(call: CallbackQuery, state:FSMContext,callback_data: dict):
    id_agency = callback_data.get('id')
    await state.update_data(id_agency=id_agency)
    await call.message.edit_text('Введите РК  с которого нужно снять деньги. Можно указывать как один так и множесвто сразу')
    await Transfer.rk_out.set()

@dp.message_handler(state=Transfer.rk_out)
async def setrkout(m:Message,state:FSMContext):
    rks = m.text
    await state.update_data(rk_out=rks)
    await m.answer('Введите РК на который нужно перевести деньги. Можно указывать только один.')
    await Transfer.rk_in.set()

@dp.message_handler(state=Transfer.rk_in)
async def setrkin(m:Message,state:FSMContext):
    rks = m.text
    await state.update_data(rk_in=rks)
    await m.answer('Введите РК на который нужно перевести деньги. Можно указывать только один.',reply_markup=all_amount_transfer())
    await Transfer.set_amount.set()

@dp.message_handler(state=Transfer.set_amount)
async def setamounttransfer(m:Message,state:FSMContext,agencys = AgencyRepository(database),users = UserRepository(database),table = TableRepository(database)):
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
    id_request = await table.add_transfer_rk(m.chat.id,amount, data['rk_in'].replace('\n', '/'),
                                             data['rk_out'].replace('\n', '/'))
    msg = f"#{user.nickname} №{id_request} агентство {agency.name}\nВывести на сумму {str(amount)}\n<b>{data['rk_out']}</b> на\n<b>{data['rk_in']}</b>"
    await bot.send_message(CHAT_ID, msg, reply_markup=send_request(id_request, m.chat.id, 'transfer'))
    await m.answer(f'Ваша заявка <b>№{id_request}</b> отправлена', reply_markup=main_keyboard(user.role))


@dp.callback_query_handler(text_contains='allamoounttransfer',state=Transfer.set_amount)
async def confirmamount(call:CallbackQuery,state:FSMContext,agencys = AgencyRepository(database),users = UserRepository(database),table = TableRepository(database)):
    data = await state.get_data()
    await state.finish()
    user = await users.get_by_id(call.message.chat.id)
    agency = await agencys.get_by_id(int(data['id_agency']))
    id_request = await table.add_transfer_rk(call.message.chat.id,'all',data['rk_in'].replace('\n','/'),data['rk_out'].replace('\n','/'))
    msg = f"#{user.nickname} №{id_request} агентство {agency.name}\nВывести всё средства c\n<b>{data['rk_out']}</b> на\n<b>{data['rk_in']}</b>"
    await bot.send_message(CHAT_ID,msg,reply_markup=send_request(id_request,call.message.chat.id,'transfer'))
    await call.message.edit_text(f'Ваша заявка <b>№{id_request}</b> отправлена',reply_markup=main_keyboard(user.role))

@dp.callback_query_handler(send_request_transfer_rk_callback.filter())
async def updatestatustransfer(call:CallbackQuery,callback_data:dict,users= UserRepository(database),
                             tables = TableRepository(database)):
    id_request = callback_data.get('id')
    status = callback_data.get('status')
    admin = call.from_user.id
    admin_user = await users.get_by_id(admin)
    sender = callback_data.get('sender')
    await tables.update_status_transfer_rk(int(id_request),status,admin)
    if status == 'confirm':
        msg = f'Ваша заявка №{id_request} перевести баланс <b>ОДОБРЕНА</b> #{admin_user.nickname}'
    else:
        msg = f'Ваша заявка №{id_request} перевести баланс <b>ОТКЛОНЕНА</b> #{admin_user.nickname}'
    await bot.send_message(int(sender), msg)
    await call.message.edit_reply_markup(seached(status))





