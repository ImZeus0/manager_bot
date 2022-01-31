from db.base import database
from loader import bot, dp
from models.agency import Agency
from models.user import User,UserIn
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from core import config
from datetime import datetime
from keyboard import *
from state import *
from aiogram.types.callback_query import CallbackQuery
from repositories.users import UserRepository
from repositories.agencys import AgencyRepository
from repositories.bcs import BcRepository

@dp.callback_query_handler(text_contains='admin_panel')
async def menu_admin(call:CallbackQuery):
    await call.message.edit_text('Админ панель')
    await call.message.edit_reply_markup(admin_panel())

@dp.callback_query_handler(text_contains='set_admin')
async def choose_user(call:CallbackQuery,users = UserRepository(database)):
    await call.message.edit_text('Выберете пользователя')
    list_users = await users.get_users()

    all_users = []
    for user in list_users:
        print(User.parse_obj(user))
        all_users.append(User.parse_obj(user))

    await call.message.edit_reply_markup(choose_admin(all_users))

@dp.callback_query_handler(choose_admin_callback.filter())
async def confirm_admin(call:CallbackQuery,callback_data:dict,users = UserRepository(database)):
    id = callback_data.get('id')
    user = await users.get_by_id(int(id))
    await users.update_role(int(id),'admin')

    await call.message.edit_text(f'{user.nickname} теперь админ')
    await call.message.edit_reply_markup(admin_panel())

@dp.callback_query_handler(text_contains='add_agency')
async def addagency(call:CallbackQuery):
    await call.message.edit_text('Введите названия агентства')
    await AddAgency.name.set()

@dp.message_handler(state=AddAgency.name)
async def confirmagency(m:Message,state:FSMContext,agencys=AgencyRepository(database)):
    agency = m.text
    await state.finish()
    await bot.delete_message(m.chat.id, m.message_id - 1)
    await bot.delete_message(m.chat.id, m.message_id)
    await agencys.create(agency)
    await m.answer(f'Агентство {agency} добавлено ',reply_markup=admin_panel())

@dp.callback_query_handler(text_contains='add_bc')
async def chooseagencyforbc(call:CallbackQuery,agencys=AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys_for_add_bc(all_agencys))

@dp.callback_query_handler(agencys_for_add_bc.filter())
async def set_name_bc(call:CallbackQuery,state:FSMContext,callback_data:dict):
    id_agency = int(callback_data.get('id'))
    await state.update_data(id_agency=id_agency)
    await call.message.edit_text('Введите названия БЦ')
    await AddBc.name.set()

@dp.message_handler(state=AddBc.name)
async def createbc(m:Message,state:FSMContext,bcs=BcRepository(database)):
    name = m.text
    data = await state.get_data()
    id_agency = data['id_agency']
    await state.finish()
    await bcs.create(name,id_agency)
    await bot.delete_message(m.chat.id, m.message_id - 1)
    await bot.delete_message(m.chat.id, m.message_id)
    await m.answer(f'БЦ {name} добавлено ', reply_markup=admin_panel())





