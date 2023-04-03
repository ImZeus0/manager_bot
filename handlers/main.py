from db.base import database
from google_sheet import create_list
from keyboards.admin_keyboards import users_keyboard
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from keyboards.main_keyboard import *
from keyboards.send_requests_keyboards import *
from repositories.expenses_repository import ExpensesRepository
from state import *
from aiogram.types.callback_query import CallbackQuery
from repositories.users import UserRepository


@dp.message_handler(commands=['start'], state='*')
async def mainstart(m: Message, state: FSMContext,users = UserRepository(database),expenses=ExpensesRepository(database)):
    await state.finish()
    id = m.chat.id
    user = await users.get_by_id(id)
    await m.delete()
    if user is None:
        await m.answer('Введите свое ФИО')
        await Reg.nickname.set()
    else:
        active_expenses = await expenses.get_active()
        await m.answer(f'Привет {user.nickname}',reply_markup=main_keyboard(user.role,len(active_expenses)))


@dp.message_handler(state=Reg.nickname)
async def set_name(m:Message,state:FSMContext,users = UserRepository(database),expenses=ExpensesRepository(database)):
    await bot.delete_message(m.chat.id, m.message_id-1)
    await bot.delete_message(m.chat.id, m.message_id)
    await users.create(m.chat.id,m.text)
    user = await users.get_by_id(m.chat.id)
    active_expenses = await expenses.get_active()
    await m.answer(f'Привет {m.text}', reply_markup=main_keyboard(user.role,len(active_expenses)))
    await state.finish()
    create_list(m.text)


@dp.callback_query_handler(choose_main_menu.filter(),state='*')
async def enter_menu(call:CallbackQuery,state:FSMContext,callback_data:dict,users = UserRepository(database),expenses=ExpensesRepository(database)):
    menu = callback_data.get('menu')
    if menu == 'create_order':
        await call.message.edit_text('Выберете тип операции')
        await call.message.edit_reply_markup(show_type_operation())
    elif menu == 'back_mainmenu':
        active_expenses = await expenses.get_active()
        await state.finish()
        user = await users.get_by_id(call.message.chat.id)
        await call.message.edit_text(f'Привет {user.nickname}')
        await call.message.edit_reply_markup(main_keyboard(user.role,len(active_expenses)))
    elif menu == 'my_orders':
        data = await expenses.get_by_id_user(call.message.chat.id)
        msg = 'Заявки\n'
        for d in data:
            msg += f'<b>ID</b>:{d.id} {d.status} {d.purpose} {d.amount} {d.service}\n'
        await call.message.edit_text(msg,reply_markup=back())
    elif menu == 'all_users':
        list_users = await users.get_users()
        await call.message.edit_text('Выберете пользователя',reply_markup=users_keyboard(list_users))
    elif menu == 'active_orders':
        active_expenses = await expenses.get_active()
        for e in active_expenses:
            user = await users.get_by_id(e.id_user)
            if e.account_number == 'create':
                msq = f'Заявка №{e.id} от {user.nickname}\n' \
                      f'Тип операции: <b>создать аккаунт</b>\n' \
                      f'Сервис: {e.service}\n' \
                      f'White page domain {e.purpose}\n' \
                      f'Сумма {e.amount}\n ' \
                      f'Email <code>{e.payment_key}\n</code>' \
                      f'Дата {e.created_at}'
            else:
                msq = f'Заявка №{e.id} от {user.nickname}\n' \
                      f'Тип операции: <b>{e.type_operation}</b>\n' \
                      f'Сервис: {e.service}\n' \
                      f'Назначение {e.purpose}\n' \
                      f'Валюта {e.currency}\n ' \
                      f'Cумма <code>{e.amount}\n</code>' \
                      f'Номер аккаунта <code>{e.account_number}</code>\n' \
                      f'Nдентификатор аккаунта <code>{e.payment_key}\n</code>' \
                      f'Дата {e.created_at}'
            await call.message.answer(msq,reply_markup=show_request(e.id, str(e.id_user)))



