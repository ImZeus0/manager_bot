from aiogram.utils.callback_data import CallbackData

choose_main_menu = CallbackData('choosemainmenu','menu')
choose_type_operation = CallbackData('choosetypeoperation','type')
choose_service = CallbackData('chooseservice','service')
choose_service_other = CallbackData('chooseserviceother','service')
choose_currency = CallbackData('choosecurrency','currency')
accept_request = CallbackData('acceptrequest','operation','id','user')
update_table = CallbackData('updategoogletable','id')
choose_operation_agency_account = CallbackData('operationagencyacc','type')