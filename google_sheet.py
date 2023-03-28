# Подключаем библиотеки
import apiclient as apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'manager-bot-381913-4ae1ff921100.json'  # Имя файла с закрытым ключом, вы должны подставить свое
spreadsheetId = '10qfpdbG7sBTfAHCL0h5DSZ1vDbZ42nZsdo7g6yqOC-4'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API




def write_row_spend(list,rows):
    start_row = 2
    end_row = start_row+len(rows)
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"{list}!B{start_row}:L{end_row}",
             "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
             "values": rows}
        ]
    }).execute()

def get_lists():
    spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
    sheetList = spreadsheet.get('sheets')
    for sheet in sheetList:
        print(sheet['properties']['sheetId'], sheet['properties']['title'])
def create_list(name):
    results = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body=
        {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": name,
                            "gridProperties": {
                                "rowCount": 20,
                                "columnCount": 12
                            }
                        }
                    }
                }
            ]
        }).execute()
