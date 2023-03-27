from core.config import get_settings
from db.base import database
from keyboards.send_requests_keyboards import *
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from keyboards.main_keyboard import *
from core.enums import Operation, Status
from aiogram.types.callback_query import CallbackQuery
from models.expenses import Expense
from repositories.expenses_repository import ExpensesRepository
from repositories.users import UserRepository
from state import AddExpenses
from depends import get_expenses_repository


@dp.callback_query_handler(choose_type_operation.filter())
async def enter_type_operation(call: CallbackQuery, state: FSMContext, callback_data: dict):
    type_operation = callback_data.get('type')
    await state.update_data(type_operation=type_operation)
    if type_operation == Operation.UpBudget:
        await call.message.edit_text('Выберете сервис')
        await call.message.edit_reply_markup(show_service())
    elif type_operation == Operation.OtherExpenses:
        await state.update_data(service='other')
        await call.message.edit_text('Выберете валюту')
        await call.message.edit_reply_markup(show_currency())



@dp.callback_query_handler(choose_service.filter())
async def enter_service(call: CallbackQuery, state: FSMContext, callback_data: dict):
    service = callback_data.get('service')
    await state.update_data(service=service)
    await call.message.edit_text('Выберете валюту')
    await call.message.edit_reply_markup(show_currency())


@dp.callback_query_handler(choose_currency.filter())
async def enter_currency(call: CallbackQuery, state: FSMContext, callback_data: dict):
    currency = callback_data.get('currency')
    await state.update_data(currency=currency)
    await call.message.edit_text('Введите сумму', reply_markup=back())
    await AddExpenses.amount.set()


@dp.message_handler(state=AddExpenses.amount)
async def enter_amount(m: Message, state: FSMContext):
    try:
        amount = float(m.text)
        await state.update_data(amount=amount)
        await m.answer('Введите назначение платежа', reply_markup=back())
        await AddExpenses.purpose.set()
    except ValueError as e:
        await m.answer('Введите число', reply_markup=back())


@dp.message_handler(state=AddExpenses.purpose)
async def enter_purpose(m: Message, state: FSMContext):
    purpose = m.text
    await state.update_data(purpose=purpose)
    await m.answer('Введите идентификатор аккаунта (email, address wallet, account number)', reply_markup=back())
    await AddExpenses.payment_key.set()


@dp.message_handler(state=AddExpenses.payment_key)
async def enter_payment_key(m: Message,
                            state: FSMContext, expenses=ExpensesRepository(database),
                            users=UserRepository(database)):
    payment_key = m.text
    await state.update_data(payment_key=payment_key)
    data = await state.get_data()
    expense_obj = Expense(id_user=m.chat.id,
                          type_operation=data['type_operation'],
                          service=data['service'],
                          amount=data['amount'],
                          currency=data['currency'],
                          purpose=data['purpose'],
                          payment_key=data['payment_key'],
                          status=Status.PENDING)
    id_record = await expenses.create(expense_obj)
    user = await users.get_by_id(m.chat.id)
    msq = f'Тип операции: {expense_obj.type_operation}\n' \
          f'Сервис: {expense_obj.service}\n' \
          f'Назначение {expense_obj.purpose}\n' \
          f'Валюта {expense_obj.currency}\n ' \
          f'Cумма {expense_obj.amount}\n' \
          f'Статус {expense_obj.status}'
    to_admin = f'Заявка №{id_record} от {user.nickname}\n' + msq
    to_user = f'Заявка отправлена №{id_record}\n' + msq
    await m.answer(to_user, reply_markup=back())
    await bot.send_message(get_settings().admin,to_admin,reply_markup=show_request(id_record,str(m.chat.id)))

@dp.callback_query_handler(accept_request.filter())
async def enter_request(call: CallbackQuery, state: FSMContext, callback_data: dict,
                        expenses=ExpensesRepository(database)):
    status = callback_data.get('operation')
    id_requets = int(callback_data.get('id'))
    id_user = int(callback_data.get('user'))
    await expenses.update_status(status,id_requets)
    await call.message.edit_text(f'Запрос №{id_requets} -> {status}')
    await bot.send_message(id_user,f'Запрос №{id_requets} -> {status}')
