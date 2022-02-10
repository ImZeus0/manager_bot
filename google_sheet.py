# Подключаем библиотеки
import apiclient as apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'botsheet-340615-e9082625ce2e.json'  # Имя файла с закрытым ключом, вы должны подставить свое
spreadsheetId = '1ls6iMIyCCcSDSalGemI9tmCZ8L9Y700BWZC47BZGpOc'


def write_row_donate(rows):
    start_row = 3
    end_row = start_row+len(rows)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"Лист1!A{start_row}:F{end_row}",
             "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
             "values": rows}
        ]
    }).execute()

def write_row_spend(rows):
    start_row = 3
    end_row = start_row+len(rows)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"Лист1!H{start_row}:L{end_row}",
             "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
             "values": rows}
        ]
    }).execute()