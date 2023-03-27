from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from callback import *
import json

from core.enums import Currency, Status


def show_type_operation():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Пополнение Бюджета', callback_data=choose_type_operation.new('up_budget')))
    k.add(InlineKeyboardButton('Прочие расходы', callback_data=choose_type_operation.new('other_expenses')))
    k.add(InlineKeyboardButton('Назад', callback_data=choose_main_menu.new('back_mainmenu')))
    return k


def show_service():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Flex Card', callback_data=choose_service.new('flex_card')))
    k.add(InlineKeyboardButton('4x4', callback_data=choose_service.new('4x4')))
    k.add(InlineKeyboardButton('Combo Cards', callback_data=choose_service.new('combo_cards')))
    k.add(InlineKeyboardButton('China Agency Accounts', callback_data=choose_service.new('china_agency_accounts')))
    k.add(InlineKeyboardButton('Africa Agency Accounts', callback_data=choose_service.new('africa_agency_accounts')))
    k.add(InlineKeyboardButton('Serbia Agency Accounts', callback_data=choose_service.new('serbia_agency_accounts')))
    k.add(InlineKeyboardButton('Назад', callback_data=choose_main_menu.new('back_mainmenu')))
    return k

def show_currency():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('USDT (TRC20)',callback_data=choose_currency.new(Currency.USDT_TRC_20)))
    k.add(InlineKeyboardButton('USDT (ERC20)',callback_data=choose_currency.new(Currency.USDT_ERC_20)))
    k.add(InlineKeyboardButton('Назад', callback_data=choose_main_menu.new('back_mainmenu')))
    return k
def back():
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Назад', callback_data=choose_main_menu.new('back_mainmenu')))
    return k

def show_request(id_requets,id_user):
    k = InlineKeyboardMarkup()
    k.add(InlineKeyboardButton('Принять',callback_data=accept_request.new(Status.APPROVED,id_requets,id_user)))
    k.add(InlineKeyboardButton('Отклонить',callback_data=accept_request.new(Status.REJECTED,id_requets,id_user)))
    return k