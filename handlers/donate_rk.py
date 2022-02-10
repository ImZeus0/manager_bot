from db.base import database
from models.agency import Agency
from models.bc import Bc
from models.email import Email
from google_sheet import write_row_donate
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

@dp.callback_query_handler(text_contains='replenish_rk')
async def setacyncudonate(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys, 'donate_rk'))


@dp.callback_query_handler(agencys_for_donate_rk.filter())
async def setemaildoname(call:CallbackQuery,state:FSMContext,callback_data:dict,emails = EmailRepository(database)):
    id_agency = callback_data.get('id')
    await state.update_data(id_agency=id_agency)
    list_email = await emails.get_by_user(call.message.chat.id)
    emails_r = []
    for email in list_email:
        emails_r.append(Email.parse_obj(email))
    await call.message.edit_text('Выберете почту')
    await call.message.edit_reply_markup(show_emails(emails_r,'donate_rk'))

@dp.callback_query_handler(choose_email_for_donate_rk.filter())
async def setamountdonate(call:CallbackQuery,state:FSMContext,callback_data,agencys = AgencyRepository(database)):
    email = callback_data.get('email')
    await state.update_data(email = email)
    data = await state.get_data()
    agency = await agencys.get_by_id(int(data['id_agency']))
    await call.message.edit_text(f'Введите сумму пополнения в {agency.currency}')
    await DonateRk.amount.set()

@dp.message_handler(state=DonateRk.amount)
async def confirmammountdonate(m:Message,state:FSMContext):
    amount = m.text
    try:
        amount = float(amount)
    except Exception:
        await m.answer('Введите число')
        return
    await state.update_data(amount=amount)
    await m.answer('Введите номера РК (каждый с новой строки)')
    await DonateRk.input_rk.set()

@dp.message_handler(state=DonateRk.input_rk)
async def setdirk(m:Message,state:FSMContext,tables =  TableRepository(database),
                  agencys = AgencyRepository(database),
                  users = UserRepository(database)):
    line_rk = m.text
    data = await state.get_data()
    await state.finish()
    user = await users.get_by_id(m.chat.id)
    agency = await agencys.get_by_id(int(data['id_agency']))
    response = await tables.add_donate_rk(m.chat.id,data['amount'],m.text.replace('\n','/'),data['email'],data['id_agency'])
    msg = f"#{user.nickname} №{response}\n{data['email']}\nПополнить РК на {data['amount']} {agency.currency}\n{line_rk}"
    await bot.send_message(CHAT_ID,msg,reply_markup=send_request(response,m.chat.id,'donate_rk',data['email']))
    await m.answer(f'Заявка <b>№{response}</b> отправлена',reply_markup=main_keyboard(user.role))

@dp.callback_query_handler(send_request_donate_rk_callback.filter())
async def updatestatusdonate(call:CallbackQuery,callback_data:dict,users= UserRepository(database),
                             tables = TableRepository(database),agencys = AgencyRepository(database)):
    id_request = callback_data.get('id')
    status = callback_data.get('status')
    admin = call.from_user.id
    admin_user = await users.get_by_id(admin)
    email = callback_data.get('email')
    sender = callback_data.get('sender')
    await tables.update_status_donate_rk(int(id_request),status,admin)
    if status == 'confirm':
        records = await tables.get_all_donate_rk()
        data_to_table = []
        for record in records:
            user = await users.get_by_id(record.id_user)
            agency = await agencys.get_by_id(record.id_agency)
            data_to_table.append([user.nickname, agency.name, record.email, record.cabinets,record.ammount, str(record.updated_at)])
        write_row_donate(data_to_table)
        msg = f'Ваша заявка №{id_request} пополнить РК {email} <b>ОДОБРЕНА</b> #{admin_user.nickname}'
    else:
        msg = f'Ваша заявка №{id_request} пополнить РК {email} <b>ОТКЛОНЕНА</b> #{admin_user.nickname}'
    await bot.send_message(int(sender), msg)
    await call.message.edit_reply_markup(seached(status))

