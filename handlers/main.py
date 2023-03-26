from db.base import database
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from core import config
from datetime import datetime
from keyboard import *
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
        await m.answer('Введите свой ник')
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

@dp.callback_query_handler(text_contains='back_mainmenu')
async def back_menu(call:CallbackQuery,state:FSMContext,users = UserRepository(database)):
    await state.finish()
    user = await users.get_by_id(call.message.chat.id)
    await call.message.edit_text(f'Привет {user.nickname}')
    await call.message.edit_reply_markup(main_keyboard(user.role))



