from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from callback import *
import json


def main_keyboard(role):
    k = InlineKeyboardMarkup()
    if role == 'admin':
        k.add(InlineKeyboardButton('Админ панель', callback_data='admin_panel'))
    k.add(InlineKeyboardButton('Заказать новую почту', callback_data='order_new_mail'))
    k.add(InlineKeyboardButton('Сделать новые РК', callback_data='make_new_rk'))
    k.add(InlineKeyboardButton('Пополнить РК', callback_data='replenish_rk'))
    k.add(InlineKeyboardButton('Перевести баланс', callback_data='transfer_balance'))
    k.add(InlineKeyboardButton('Вывести баланс', callback_data='take_out_the_balance'))
    k.add(InlineKeyboardButton('Удалить почту', callback_data='delete_mail'))
    k.add(InlineKeyboardButton('Расход за вчера', callback_data='spending_for_yesterday'))
    return k


def admin_panel():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Добавить агенство', callback_data='add_agency'))
    k.add(InlineKeyboardButton('Добавить БЦ', callback_data='add_bc'))
    k.add(InlineKeyboardButton('Удалить агенство', callback_data='delete_agency'))
    k.add(InlineKeyboardButton('Удалить БЦ', callback_data='delete_bc'))
    k.add(InlineKeyboardButton('Сделать админом', callback_data='set_admin'))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def choose_admin(users):
    k = InlineKeyboardMarkup()
    for user in users:
        k.add(InlineKeyboardButton(user.nickname, callback_data=choose_admin_callback.new(user.id_user)))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def show_agencys_for_add_bc(agencys):
    k = InlineKeyboardMarkup()
    for agency in agencys:
        k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_add_bc.new(agency.id)))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def show_agencys_for_add_email(agencys):
    k = InlineKeyboardMarkup()
    for agency in agencys:
        k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_add_email.new(agency.id)))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def show_agencys(agencys, endpoint):
    k = InlineKeyboardMarkup()
    if endpoint == 'email':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_add_email.new(agency.id)))
    if endpoint == 'rk':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_add_rk.new(agency.id)))
    if endpoint == 'donate_rk':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_donate_rk.new(agency.id)))
    if endpoint == 'transfer':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_transfer_rk.new(agency.id)))
    if endpoint == 'withdraw':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_withdraw_rk.new(agency.id)))
    if endpoint == 'deleteemail':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_delete_email.new(agency.id)))
    if endpoint == 'spending':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_spending.new(agency.id)))
    if endpoint == 'delete':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name, callback_data=agencys_for_delete.new(agency.id)))
    if endpoint == 'delbc':
        for agency in agencys:
            k.add(InlineKeyboardButton(agency.name,callback_data=agencys_for_del_bc.new(agency.id)))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def show_bcs(bcs, endpoint):
    k = InlineKeyboardMarkup()
    if endpoint == 'email':
        for bc in bcs:
            k.add(InlineKeyboardButton(bc.name, callback_data=bc_for_add_email.new(bc.id)))
        k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    elif endpoint == 'rk':
        for bc in bcs:
            k.add(InlineKeyboardButton(bc.name, callback_data=bc_for_add_rk.new(bc.id)))
        k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    elif endpoint == 'delete':
        for bc in bcs:
            k.add(InlineKeyboardButton(bc.name, callback_data=bc_for_delete.new(bc.id)))
        k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def send_request(id, sender, endpoint,email=None):
    k = InlineKeyboardMarkup()
    if endpoint == 'mail':
        k.add(InlineKeyboardButton('🟢Подтвердить',
                                   callback_data=send_request_new_mail_callback.new(id, 'confirm', sender)))
        k.add(
            InlineKeyboardButton('🔴Отклонить', callback_data=send_request_new_mail_callback.new(id, 'reject', sender)))
    elif endpoint == 'rk':
        print(id, 'confirm', sender,email)
        k.add(InlineKeyboardButton('🟢Подтвердить',
                                   callback_data=send_request_new_rk_callback.new(id, 'confirm', sender,email)))
        k.add(
            InlineKeyboardButton('🔴Отклонить', callback_data=send_request_new_rk_callback.new(id, 'reject', sender,email)))
    elif endpoint == 'donate_rk':
        k.add(InlineKeyboardButton('🟢Подтвердить',
                                   callback_data=send_request_donate_rk_callback.new(id, 'confirm', sender)))
        k.add(
            InlineKeyboardButton('🔴Отклонить',
                                 callback_data=send_request_donate_rk_callback.new(id, 'reject', sender)))
    elif endpoint == 'transfer':
        k.add(InlineKeyboardButton('🟢Подтвердить',
                                   callback_data=send_request_transfer_rk_callback.new(id, 'confirm', sender)))
        k.add(
            InlineKeyboardButton('🔴Отклонить',
                                 callback_data=send_request_transfer_rk_callback.new(id, 'reject', sender)))
    elif endpoint == 'withdraw':
        k.add(InlineKeyboardButton('🟢Подтвердить',
                                   callback_data=send_request_donate_rk_callback.new(id, 'confirm', sender)))
        k.add(
            InlineKeyboardButton('🔴Отклонить',
                                 callback_data=send_request_donate_rk_callback.new(id, 'reject', sender)))
    return k


def seached(status):
    k = InlineKeyboardMarkup()
    if status == 'confirm':
        k.add(InlineKeyboardButton('ℹОДОБРЕНО', callback_data='x'))
    else:
        k.add(InlineKeyboardButton('ℹОТКЛОНЕНО', callback_data='x'))
    return k


def show_emails(emails, endpoint):
    k = InlineKeyboardMarkup()
    if endpoint == 'rk':
        for email in emails:
            k.add(InlineKeyboardButton(email.email, callback_data=choose_email_for_add_rk.new(email.email)))
    if endpoint == 'donate_rk':
        for email in emails:
            k.add(InlineKeyboardButton(email.email, callback_data=choose_email_for_donate_rk.new(email.email)))
    if endpoint == 'delete_email':
        for email in emails:
            k.add(InlineKeyboardButton(email.email, callback_data=choose_email_for_delete_rk.new(email.email)))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def show_count_rk():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('5', callback_data=choose_count_rk.new('5')))
    k.add(InlineKeyboardButton('10', callback_data=choose_count_rk.new('10')))
    return k

def all_amount_transfer():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Весь баланс',callback_data='allamoounttransfer'))
    return k

def all_amount_withdraw():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Весь баланс',callback_data='allamoountwithdraw'))
    return k

def confirm_delete_email():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Да',callback_data=confirm_delete_callback.new('yes')),
          InlineKeyboardButton('Нет',callback_data=confirm_delete_callback.new('no')))
    return k