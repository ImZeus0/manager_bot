from aiogram.utils.callback_data import CallbackData

choose_admin_callback = CallbackData('chooseadmin', 'id')

agencys_for_add_bc = CallbackData('agencysforaddbc', 'id')
agencys_for_add_email = CallbackData('agencysforaddemail', 'id')
agencys_for_add_rk = CallbackData('agencysforaddrk', 'id')
agencys_for_donate_rk = CallbackData('agencysfordonaterk', 'id')
agencys_for_transfer_rk = CallbackData('agencysfortransferrk', 'id')
agencys_for_withdraw_rk = CallbackData('agencysforwithdrawrk', 'id')
agencys_for_delete_email = CallbackData('agencysfordeleteemail', 'id')
agencys_for_spending = CallbackData('agencysforspending', 'id')
agencys_for_delete = CallbackData('agencysfordetele', 'id')
agencys_for_del_bc = CallbackData('agencysfordelbc', 'id')

bc_for_add_email = CallbackData('bcsforaddemail', 'id')
bc_for_add_rk = CallbackData('bcsforaddrk', 'id')
bc_for_delete = CallbackData('bcsfordelete', 'id')

send_request_new_mail_callback = CallbackData('sendrequstnewmail', 'id', 'status', 'sender')
send_request_new_rk_callback = CallbackData('sendrequstnewrk', 'id', 'status', 'sender', 'email')
send_request_donate_rk_callback = CallbackData('sendrequstdonaterk', 'id', 'status', 'sender', )
send_request_transfer_rk_callback = CallbackData('sendrequsttransferrk', 'id', 'status', 'sender', )
send_request_withdraw_rk_callback = CallbackData('sendrequstwithdrawrk', 'id', 'status', 'sender', )

choose_email_for_add_rk = CallbackData('chooseemailforrk', 'email')
choose_email_for_donate_rk = CallbackData('chooseemailfordonaterk', 'email')
choose_email_for_delete_rk = CallbackData('chooseemailfordelete', 'email')

choose_count_rk = CallbackData('choosecountrk', 'count')
confirm_delete_callback = CallbackData('confirmdeleteemail','status')