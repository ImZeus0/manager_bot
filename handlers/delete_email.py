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

@dp.callback_query_handler(text_contains='delete_mail')
async def setacyncudonate(call:CallbackQuery,agencys = AgencyRepository(database)):
    await call.message.edit_text('Выберете агентство')
    list_agencys = await agencys.get_all()

    all_agencys = []
    for agency in list_agencys:
        all_agencys.append(Agency.parse_obj(agency))

    await call.message.edit_reply_markup(show_agencys(all_agencys, 'deleteemail'))

@dp.callback_query_handler(agencys_for_delete_email.filter())
async def setemaildelete(call:CallbackQuery,state:FSMContext,callback_data:dict,emails = EmailRepository(database)):
    id_agency = callback_data.get('id')
    await state.update_data(id_agency=id_agency)
    list_email = await emails.get_by_user(call.message.chat.id,int(id_agency))
    emails_r = []
    for email in list_email:
        emails_r.append(Email.parse_obj(email))
    await call.message.edit_text('Выберете почту которую нужно удалить')
    await call.message.edit_reply_markup(show_emails(emails_r, 'delete_email'))

@dp.callback_query_handler(choose_email_for_delete_rk.filter())
async def confirmingemail(call:CallbackQuery,state:FSMContext,callback_data:dict):
    email = callback_data.get('email')
    await state.update_data(email=email)
    await call.message.edit_text(f'Вы действительно хотите удалить почту {email} ?',reply_markup=confirm_delete_email())

@dp.callback_query_handler(confirm_delete_callback.filter())
async def finishdeletemail(call:CallbackQuery,callback_data:dict,state:FSMContext,emails = EmailRepository(database),
                           users = UserRepository(database)):
    status = callback_data.get('status')
    data = await state.get_data()
    user = await users.get_by_id(call.message.chat.id)
    await state.finish()
    if status == 'yes':
        await emails.delete(data['email'])
        await call.message.edit_text(f"Почта {data['email']} удалена",reply_markup=main_keyboard(user.role))
    else:
        await call.message.edit_text(f"Главное меню", reply_markup=main_keyboard(user.role))






