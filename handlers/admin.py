from db.base import database
from loader import bot, dp
from models.agency import Agency
from models.bc import Bc
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
async def agencycurrency(m:Message,state:FSMContext,agencys=AgencyRepository(database)):
    agency = m.text
    await state.update_data(agency=agency)
    await bot.delete_message(m.chat.id, m.message_id - 1)
    await bot.delete_message(m.chat.id, m.message_id)
    await m.answer('Введите валюту')
    await AddAgency.currency.set()

@dp.message_handler(state=AddAgency.currency)
async def confirmagency(m:Message,state:FSMContext,agencys=AgencyRepository(database)):
    currency = m.text
    data = await state.get_data()
    await state.finish()
    await agencys.create(data['agency'],currency)
    await m.answer(f'Агентство {data["agency"]} добавлено ',reply_markup=admin_panel())

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

@dp.callback_query_handler(text_contains = 'delete_agency')
async def seleteagency(call:CallbackQuery,agencys=AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство которое нужно удалить')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys,'delete'))

@dp.callback_query_handler(agencys_for_delete.filter())
async def deleteagency(call:CallbackQuery,callback_data:dict,agencys=AgencyRepository(database)):
    id = int(callback_data.get('id'))
    agency = await agencys.get_by_id(id)
    await agencys.delete(id)
    await call.message.edit_text(f'Агентство {agency.name}  удаленно',reply_markup=admin_panel())

@dp.callback_query_handler(text_contains = 'delete_bc')
async def seleteagency(call:CallbackQuery,agencys=AgencyRepository(database),bcs=BcRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys, 'delbc'))

@dp.callback_query_handler(agencys_for_del_bc.filter())
async def setbcfordelete(call:CallbackQuery,state:FSMContext,callback_data:dict,
                         bcs = BcRepository(database)):
    id_agency = int(callback_data.get('id'))
    list_bc = await bcs.get_by_agency(id_agency)
    all_bc = []
    for bc in list_bc:
        all_bc.append(Bc.parse_obj(bc))
    await call.message.edit_text('Выберете БЦ который нужно удалить')
    await call.message.edit_reply_markup(show_bcs(list_bc,'delete'))

@dp.callback_query_handler(bc_for_delete.filter())
async def deletebc(call:CallbackQuery,callback_data:dict,bcs = BcRepository(database)):
    id_bc = int(callback_data.get('id'))
    bc = await bcs.get_by_id(id_bc)
    await bcs.delete(id_bc)
    await call.message.edit_text(f'БЦ {bc.name} удален', reply_markup=admin_panel())









