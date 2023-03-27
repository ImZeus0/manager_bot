from db.base import database
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
async def mainstart(m: Message, state: FSMContext,users = UserRepository(database)):
    print(m.chat.id)
    await state.finish()
    id = m.chat.id
    user = await users.get_by_id(id)
    await m.delete()
    if user is None:
        await m.answer('Введите свое ФИО')
        await Reg.nickname.set()
    else:
        await m.answer(f'Привет {user.nickname}',reply_markup=main_keyboard(user.role))


@dp.message_handler(state=Reg.nickname)
async def set_name(m:Message,state:FSMContext,users = UserRepository(database),):
    await bot.delete_message(m.chat.id, m.message_id-1)
    await bot.delete_message(m.chat.id, m.message_id)
    await users.create(m.chat.id,m.text)
    user = await users.get_by_id(m.chat.id)
    await m.answer(f'Привет {m.text}', reply_markup=main_keyboard(user.role))
    await state.finish()


@dp.callback_query_handler(choose_main_menu.filter(),state='*')
async def enter_menu(call:CallbackQuery,state:FSMContext,callback_data:dict,users = UserRepository(database),expenses=ExpensesRepository(database)):
    menu = callback_data.get('menu')
    if menu == 'create_order':
        await call.message.edit_text('Выберете тип операции')
        await call.message.edit_reply_markup(show_type_operation())
    elif menu == 'back_mainmenu':
        await state.finish()
        user = await users.get_by_id(call.message.chat.id)
        await call.message.edit_text(f'Привет {user.nickname}')
        await call.message.edit_reply_markup(main_keyboard(user.role))
    elif menu == 'my_orders':
        data = await expenses.get_by_id_user(call.message.chat.id)
        msg = 'Заявки\n'
        for d in data:
            msg += f'<b>ID</b>:{d.id} {d.status} {d.purpose} {d.amount} {d.service}\n'
        await call.message.edit_text(msg,reply_markup=back())



