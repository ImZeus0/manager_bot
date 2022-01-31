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

    await call.message.edit_reply_markup(show_agencys_for_add_email(all_agencys))

@dp.callback_query_handler(agencys_for_add_email.filter())
async def choocebc(call:CallbackQuery,callback_data:dict,state:FSMContext,bcs = BcRepository(database)):
    id_agency = int(callback_data.get('id'))
    await state.update_data(id_agency=id_agency)
    list_bcs = await bcs.get_by_agency(id_agency)

    all_bcs = []
    for agency in list_bcs:
        all_bcs.append(Bc.parse_obj(agency))

    await call.message.edit_text('Выберете БЦ')
    await call.message.edit_reply_markup(show_bcs_for_add_email(all_bcs))

@dp.callback_query_handler(bc_for_add_email.filter())
async def entername(call:CallbackQuery,state:FSMContext,callback_data:dict):
    id_bc = int(callback_data.get('id'))
    await state.update_data(id_bc=id_bc)
    await call.message.edit_text('Введите почту')
    await AddEmail.email.set()

@dp.message_handler(state=AddEmail.email)
async def add_email(m:Message,state:FSMContext,users = UserRepository(database)):
    email = m.text
    user = await users.get_by_id(m.chat.id)
    msg = f'#{user.nickname}\nсдлеать инвайт на новую почту\n{email}'
    await bot.delete_message(m.chat.id, m.message_id - 1)
    await bot.delete_message(m.chat.id, m.message_id)
    await bot.send_message(CHAT_ID,msg)


