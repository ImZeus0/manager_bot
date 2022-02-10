from db.base import database
from models.agency import Agency
from models.bc import Bc
from repositories.agencys import AgencyRepository
from repositories.bcs import BcRepository
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from datetime import datetime
from keyboard import *
from repositories.emails import EmailRepository
from state import *
from core.config import *
from aiogram.types.callback_query import CallbackQuery
from repositories.users import UserRepository

@dp.callback_query_handler(text_contains='order_new_mail')
async def choose_agency(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys,'email'))

@dp.callback_query_handler(agencys_for_add_email.filter())
async def choocebc(call:CallbackQuery,callback_data:dict,state:FSMContext,bcs = BcRepository(database)):
    id_agency = int(callback_data.get('id'))
    await state.update_data(id_agency=id_agency)
    list_bcs = await bcs.get_by_agency(id_agency)

    all_bcs = []
    for agency in list_bcs:
        all_bcs.append(Bc.parse_obj(agency))

    await call.message.edit_text('Выберете БЦ')
    await call.message.edit_reply_markup(show_bcs(all_bcs,'email'))

@dp.callback_query_handler(bc_for_add_email.filter())
async def entername(call:CallbackQuery,state:FSMContext,callback_data:dict):
    id_bc = int(callback_data.get('id'))
    await state.update_data(id_bc=id_bc)
    await call.message.edit_text('Введите почту')
    await AddEmail.email.set()

@dp.message_handler(state=AddEmail.email)
async def add_email(m:Message,state:FSMContext,users = UserRepository(database),
                    emails = EmailRepository(database)):
    current_user = await users.get_by_id(m.chat.id)
    email = m.text
    data = await state.get_data()
    await state.finish()
    user = await users.get_by_id(m.chat.id)
    await bot.delete_message(m.chat.id, m.message_id - 1)
    await bot.delete_message(m.chat.id, m.message_id)
    request = await emails.create(data['id_agency'],data['id_bc'],m.chat.id,email)
    msg = f'#{user.nickname} №{request}\nсделать инвайт на новую почту\n{email}'
    await bot.send_message(CHAT_ID,msg,reply_markup=send_request(request,m.chat.id,'mail'))
    await m.answer(f'Заявка <b>№{request}</b> отправлена',reply_markup=main_keyboard(current_user.role))

@dp.callback_query_handler(send_request_new_mail_callback.filter())
async def updatestatusemail(call:CallbackQuery,callback_data:dict,emails = EmailRepository(database),
                            users = UserRepository(database)):
    id_request = callback_data.get('id')
    status = callback_data.get('status')
    admin = call.from_user.id
    admin_user = await users.get_by_id(admin)
    sender = callback_data.get('sender')
    await emails.update_status(int(id_request),status,admin)
    if status == 'confirm':
        msg = f'Ваша заявка №{id_request} на новую почту <b>ОДОБРЕНА</b> #{admin_user.nickname}'
    else:
        msg = f'Ваша заявка №{id_request} на новую почту <b>ОТКЛОНЕНА</b> #{admin_user.nickname}'
    await bot.send_message(int(sender),msg)
    await call.message.edit_reply_markup(seached(status))



