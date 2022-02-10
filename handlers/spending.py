from db.base import database
from models.agency import Agency
from models.bc import Bc
from models.email import Email
from repositories.agencys import AgencyRepository
from repositories.bcs import BcRepository
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from google_sheet import write_row_spend
from datetime import datetime
from keyboard import *
from repositories.emails import EmailRepository
from repositories.tables import TableRepository
from state import *
from core.config import *
from aiogram.types.callback_query import CallbackQuery
from repositories.users import UserRepository

@dp.callback_query_handler(text_contains='spending_for_yesterday')
async def startspending(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()
    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))
    await call.message.edit_reply_markup(show_agencys(all_agencys, 'spending'))

@dp.callback_query_handler(agencys_for_spending.filter())
async def setspenging(call:CallbackQuery,state:FSMContext,callback_data:dict):
    id_agency = callback_data.get('id')
    await state.update_data(id_agency=id_agency)
    await call.message.edit_text('Укажите расход за вчера по данному агенству.')
    await AddSpend.set_spending.set()

@dp.message_handler(state=AddSpend.set_spending)
async def setcountban(m:Message,state:FSMContext):
    spend = float(m.text)
    await state.update_data(spend=spend)
    await m.answer('Укажите количество банов за вчера по данному агенству.')
    await AddSpend.set_count_ban.set()

@dp.message_handler(state=AddSpend.set_count_ban)
async def confirmspend(m:Message,state:FSMContext,table = TableRepository(database),
                       users = UserRepository(database),agencys = AgencyRepository(database)):
    count_ban = int(m.text)
    data = await state.get_data()
    await state.finish()
    await table.add_spend(m.chat.id,data['spend'],count_ban,data['id_agency'])
    user = await users.get_by_id(m.chat.id)
    all_spend = await table.get_all_spend()
    data_table = []
    for spend in all_spend:
        user = await users.get_by_id(spend.id_user)
        agency = await agencys.get_by_id(spend.id_agency)
        data_table.append([user.nickname,agency.name,spend.spend,spend.count_ban,str(spend.updated_at)])
    write_row_spend(data_table)
    await m.answer('Расход сохранен',reply_markup=main_keyboard(user.role))












