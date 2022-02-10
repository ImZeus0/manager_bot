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

@dp.callback_query_handler(text_contains='make_new_rk')
async def chooseagensyrk(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys,'rk'))

@dp.callback_query_handler(agencys_for_add_rk.filter())
async def choocebcrk(call:CallbackQuery,callback_data:dict,state:FSMContext,bcs = BcRepository(database)):
    id_agency = int(callback_data.get('id'))
    await state.update_data(id_agency=id_agency)
    list_bcs = await bcs.get_by_agency(id_agency)

    all_bcs = []
    for agency in list_bcs:
        all_bcs.append(Bc.parse_obj(agency))

    await call.message.edit_text('Выберете БЦ')
    await call.message.edit_reply_markup(show_bcs(all_bcs,'rk'))

@dp.callback_query_handler(bc_for_add_rk.filter())
async def chooseemail(call:CallbackQuery,state:FSMContext,callback_data:dict,emails = EmailRepository(database),
                      users = UserRepository(database)):
    id_bc = callback_data.get('id')
    await state.update_data(id_bc=id_bc)
    data = await state.get_data()
    list_emails = []
    user = await users.get_by_id(call.message.chat.id)
    emails = await emails.get_by_agency_and_bc(data['id_agency'],int(id_bc),call.message.chat.id)
    for email in emails:
        list_emails.append(Email.parse_obj(email))

    if len(list_emails) == 0:
        await call.message.edit_text("У вас нет подвязаных почт")
        await call.message.edit_reply_markup(main_keyboard(user.role))

    await call.message.edit_text('Выберете почту')
    await call.message.edit_reply_markup(show_emails(list_emails,'rk'))

@dp.callback_query_handler(choose_email_for_add_rk.filter())
async def choosecountrk(call:CallbackQuery,state:FSMContext,callback_data:dict):
    email = callback_data.get('email')
    await state.update_data(email=email)
    await call.message.edit_text('Выберете количество')
    await call.message.edit_reply_markup(show_count_rk())

@dp.callback_query_handler(choose_count_rk.filter())
async def confirmaddrk(call:CallbackQuery,state:FSMContext,callback_data:dict,
                       users = UserRepository(database),
                       tables =  TableRepository(database)):
    current_user = await users.get_by_id(call.message.chat.id)
    count = callback_data.get('count')
    data = await state.get_data()

    request = await tables.add_rk(call.message.chat.id,int(count),data['email'])
    print(request)
    msg = f'#{current_user.nickname} №{request}\nсделать новые РК на почту\n{data["email"]}\n{count} штук'
    await bot.send_message(CHAT_ID,msg,reply_markup=send_request(request,call.message.chat.id,'rk',data['email']))
    await call.message.edit_text(f'Заявка <b>№{request}</b> отправлена')
    await call.message.edit_reply_markup(main_keyboard(current_user.role))

@dp.callback_query_handler(send_request_new_rk_callback.filter())
async def updatestatusemail(call:CallbackQuery,callback_data:dict,
                            users = UserRepository(database),tables =  TableRepository(database)):
    id_request = callback_data.get('id')
    status = callback_data.get('status')
    admin = call.from_user.id
    admin_user = await users.get_by_id(admin)
    email = callback_data.get('email')
    sender = callback_data.get('sender')
    await tables.update_status_add_rk(int(id_request),status,admin)
    if status == 'confirm':
        msg = f'Ваша заявка №{id_request} сделать новые РК на почту {email} <b>ОДОБРЕНА</b> #{admin_user.nickname}'
    else:
        msg = f'Ваша заявка №{id_request} сделать новые РК на почту {email} <b>ОТКЛОНЕНА</b> #{admin_user.nickname}'
    await bot.send_message(int(sender),msg)
    await call.message.edit_reply_markup(seached(status))









