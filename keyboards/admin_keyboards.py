from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from callback import *

def users_keyboard(users):
    k = InlineKeyboardMarkup()
    for user in users:
        k.add(InlineKeyboardButton(user.nickname, callback_data=update_table.new(user.id_user)))
    k.add(InlineKeyboardButton('Назад', callback_data=choose_main_menu.new('back_mainmenu')))
    return k

def consider_request(id_user:str):
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('🟢', callback_data=reg_new_user.new(id_user,'yes')),InlineKeyboardButton('🔴', callback_data=reg_new_user.new(id_user,'no')))
    return k


