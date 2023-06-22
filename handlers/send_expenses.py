from datetime import datetime

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
from state import AddExpenses, AddAgencyAccountState, SalaryRequest
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
    elif type_operation == Operation.Salary:
        await state.update_data(type_operation='salary')
        await call.message.edit_text('Введите номер карты/USDT кошелек')
        await SalaryRequest.address.set()

@dp.message_handler(state=SalaryRequest.address)
async def enter_address_salary(m:Message,state:FSMContext):
    await state.update_data(address=m.text)
    await m.answer('Введите сумму в USD')
    await SalaryRequest.amount.set()

@dp.message_handler(state=SalaryRequest.amount,)
async def enter_address_salary(m:Message,state:FSMContext,expenses=ExpensesRepository(database),
                                     users=UserRepository(database)):
    await state.update_data(amount=m.text)
    data = await state.get_data()
    data['service'] = '-'
    expense_obj = Expense(type_operation=data['type_operation'],
                          id_user=m.chat.id,
                          service=data['service'],
                          amount=data['amount'],
                          currency='USD',
                          purpose='Salary',
                          payment_key=data['address'],
                          account_number=None,
                          status=Status.PENDING)
    id_record = await expenses.create(expense_obj)
    user = await users.get_by_id(m.chat.id)
    msg = f'<b>Зарплата</b>\nСумма {data["amount"]}\nРеквизиты {data["address"]}'
    to_admin = f'Пришла заявка на зарплату №{id_record} от {user.nickname}\n'
    to_user = f'Заявка отправлена №{id_record}\n' + msg
    await m.answer(to_user, reply_markup=back())
    admin_users = await users.get_admin_users()
    for admin in admin_users:
        await bot.send_message(admin.id_user, to_admin)

@dp.callback_query_handler(choose_service.filter())
async def enter_service(call: CallbackQuery, state: FSMContext, callback_data: dict):
    service = callback_data.get('service')
    await state.update_data(service=service)
    if service.find('agency_accounts') != -1:
        await call.message.edit_text(service)
        await call.message.edit_reply_markup(show_operation_agency_accounts())
    else:
        await call.message.edit_text('Выберете валюту')
        await call.message.edit_reply_markup(show_currency())





@dp.callback_query_handler(choose_operation_agency_account.filter())
async def enter_operation_account(call:CallbackQuery,callback_data:dict,state:FSMContext):
    operation = callback_data.get('type')
    await state.update_data(operation=operation)
    if operation == OperationAgencyAccount.UP_BALANCE_ACCOUNT:
        await call.message.edit_text('Выберете валюту')
        await call.message.edit_reply_markup(show_currency())
    elif operation == OperationAgencyAccount.CREATE_ACCOUNT:
        await call.message.edit_text('Введите email\nПример test@test.com',reply_markup=back())
        await AddAgencyAccountState.email.set()
@dp.message_handler(state=AddAgencyAccountState.email)
async def enter_email_agency_account(m:Message,state:FSMContext):
    await state.update_data(email=m.text)
    await m.answer('Введите домен с whitepage',reply_markup=back())
    await AddAgencyAccountState.domain.set()

@dp.message_handler(state=AddAgencyAccountState.domain)
async def enter_domain_account(m:Message,state:FSMContext):
    await state.update_data(domain=m.text)
    data = await state.get_data()
    min_amount = 0
    if data['service'] == 'china_agency_accounts':
        min_amount = 0
    elif data['service'] == 'serbia_agency_accounts':
        min_amount = 300
    await m.answer(f'Введите cтартовую сумма на аккаунте\nМинимум {min_amount}$',reply_markup=back())
    await AddAgencyAccountState.start_amount.set()

@dp.message_handler(state=AddAgencyAccountState.start_amount)
async def enter_start_amount_agency_account(m:Message,state:FSMContext,
                                     expenses=ExpensesRepository(database),
                                     users=UserRepository(database)):
    try:
        start_amount = float(m.text)
        await state.update_data(start_amount=m.text)
        data = await state.get_data()
        expense_obj = Expense(type_operation=Operation.UpBudget,
                              id_user=m.chat.id,
                              service=data['service'],
                              amount=start_amount,
                              currency=Currency.USDT_TRC_20,
                              purpose=data['domain'],
                              payment_key=data['email'],
                              account_number='create',
                              status=Status.PENDING)
        id_record = await expenses.create(expense_obj)
        user = await users.get_by_id(m.chat.id)
        msg = f'<b>Создание аккаунта</b>\n\nПочта {data["email"]}\nДомен {data["domain"]}\nТип акаута {data["service"]}\nСтартовая сумма {data["start_amount"]}'
        to_admin = f'Пришла заявка на создание аккаунта №{id_record} от {user.nickname}\n'
        to_user = f'Заявка отправлена №{id_record}\n' + msg
        await m.answer(to_user, reply_markup=back())
        admin_users = await users.get_admin_users()
        for admin in admin_users:
            await bot.send_message(admin.id_user, to_admin)
    except:
        await m.answer(f'Введите число', reply_markup=back())


@dp.callback_query_handler(choose_currency.filter())
async def enter_currency(call: CallbackQuery, state: FSMContext, callback_data: dict):
    currency = callback_data.get('currency')
    await state.update_data(currency=currency)
    await call.message.edit_text('Amount (сумма в USDT без знаков)', reply_markup=back())
    await AddExpenses.amount.set()


@dp.message_handler(state=AddExpenses.amount)
async def enter_amount(m: Message, state: FSMContext):
    try:
        amount = float(m.text)
        await state.update_data(amount=amount)
        msg = 'Примеры:\n' \
                        'Пополнение карты onlybank для DE - 20BET/IViBet - бренд ключи "22bet".\n' \
                        'Назначение Продление 5 укр моб прокси PPC proxylite.com\n' \
                        'Оплата сайтов в боте телеграмм @whiteduck_bot'
        await m.answer(msg, reply_markup=back())
        await AddExpenses.purpose.set()
    except ValueError as e:
        await m.answer('Введите число', reply_markup=back())


@dp.message_handler(state=AddExpenses.purpose)
async def enter_purpose(m: Message, state: FSMContext):
    purpose = m.text
    await state.update_data(purpose=purpose)
    data = await state.get_data()
    if data['service'] == 'flex_card':
        await m.answer('Email ( Почта вашего агентского аккаунта):', reply_markup=back())
    elif data['service'] == '4x4':
        await m.answer('Введите адрес кошелька\nПример: TAx6owFW8Rt552z12Xaz1EqkjY95vfnwqi', reply_markup=back())
    elif data['service'] == 'combo_cards':
        await m.answer('Email ( Почта вашего агентского аккаунта) test@test.com:', reply_markup=back())
    elif data['service'].find('agency_accounts') != -1:
        await m.answer('Account Number ( Десятизначній  код рекламного кабинета):', reply_markup=back())
        await AddExpenses.account_number.set()
        return
    elif data['service'] == 'other':
        await m.answer('Введите способ оплаты', reply_markup=back())
    await AddExpenses.payment_key.set()


@dp.message_handler(state=AddExpenses.account_number)
async def enter_payment_key(m: Message,
                            state: FSMContext):
    account_number = m.text
    await state.update_data(account_number=account_number)
    await m.answer('Введите Email\nПример: user@gmail.com', reply_markup=back())
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
                          created_at=datetime.now(),
                          account_number=data.get('account_number'),
                          status=Status.PENDING)
    id_record = await expenses.create(expense_obj)
    user = await users.get_by_id(m.chat.id)
    msq = f'Тип операции: {expense_obj.type_operation}\n' \
          f'Сервис: {expense_obj.service}\n' \
          f'Назначение {expense_obj.purpose}\n' \
          f'Валюта {expense_obj.currency}\n ' \
          f'Cумма <code>{expense_obj.amount}\n</code>' \
          f'Статус {expense_obj.status}\n' \
          f'Nдентификатор аккаунта <code>{expense_obj.payment_key}\n</code>'
    if expense_obj.account_number is not None:
        msq += f'Account number: {expense_obj.account_number}\n'
    to_admin = f'Пришла заявка №{id_record} от {user.nickname}\n'
    to_user = f'Заявка отправлена №{id_record}\n' + msq
    await state.finish()
    await m.answer(to_user, reply_markup=back())
    admin_users = await users.get_admin_users()
    for admin in admin_users:
        await bot.send_message(admin.id_user, to_admin)


@dp.callback_query_handler(accept_request.filter(),state='*')
async def enter_request(call: CallbackQuery, state: FSMContext, callback_data: dict,
                        expenses=ExpensesRepository(database),users=UserRepository(database)):
    status = callback_data.get('operation')
    id_requets = int(callback_data.get('id'))
    id_user = int(callback_data.get('user'))
    await expenses.update_status(status, id_requets)
    await bot.send_message(id_user, f'Запрос №{id_requets} -> {status}')
    await call.message.answer(f'Запрос №{id_requets} -> {status}',reply_markup=back())

