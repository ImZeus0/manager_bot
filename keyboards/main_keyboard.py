from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from callback import *
import json


def main_keyboard(role):
    k = InlineKeyboardMarkup()
    if role == 'admin':
        k.add(InlineKeyboardButton('Пользователи', callback_data=choose_main_menu.new('all_users')))
    k.add(InlineKeyboardButton('Создать заявку', callback_data=choose_main_menu.new('create_order')))
    k.add(InlineKeyboardButton('Мои заявки', callback_data=choose_main_menu.new('my_orders')))
    return k


