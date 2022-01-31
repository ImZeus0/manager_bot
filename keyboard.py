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
    k.add(InlineKeyboardButton('Сделать админом', callback_data='set_admin'))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k


def choose_admin(users):
    k = InlineKeyboardMarkup()
    for user in users:
        k.add(InlineKeyboardButton(user.nickname,callback_data=choose_admin_callback.new(user.id_user)))
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

def show_bcs_for_add_email(bcs):
    k = InlineKeyboardMarkup()
    for bc in bcs:
        k.add(InlineKeyboardButton(bcs.name, callback_data=bc_for_add_email.new(bc.id)))
    k.add(InlineKeyboardButton('Назад', callback_data='back_mainmenu'))
    return k

