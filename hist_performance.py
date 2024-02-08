import yfinance as yf
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from datetime import datetime


# Jalur absolut ke file JSON
dir_path = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(dir_path, "stock_journal.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1MkxeEFOgfe7vZLXQ10wB02COlQ_aw3URamOSACP_IHg"

cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=cred)
sheet = service.spreadsheets()
tanggal_hari_ini = datetime.now().strftime("%Y-%m-%d")

range_to_get = "history_performance!A:A"

# Menggunakan API untuk mengambil nilai dari sel
result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_to_get).execute()
values = result.get('values', [])

new_row_index = len(values) + 1 
new_row_range = f"history_performance!A{new_row_index}"

new_row_data = [[tanggal_hari_ini]]
body = {
        'values': new_row_data,
    }

# Menambahkan baris baru
sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=new_row_range,
        valueInputOption='USER_ENTERED', body=body).execute()

range_to_get = "history_performance!B:B"

result_get = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="journal!B8").execute()
values_get = result_get.get('values', [])

new_row_range = f"history_performance!B{new_row_index}"
Body = {
'values' : values_get,
}
result = service.spreadsheets().values().update(
spreadsheetId=SAMPLE_SPREADSHEET_ID, range=new_row_range,
valueInputOption='USER_ENTERED', body=Body).execute()

range_to_get = "history_performance!D:D"

# Menggunakan API untuk mengambil nilai dari sel
values = [[yf.Ticker("^JKSE").history(period="now").Close.values[0]]]
new_row_range = f"history_performance!D{new_row_index}"
Body = {
'values' : values,
}

result = service.spreadsheets().values().update(
spreadsheetId=SAMPLE_SPREADSHEET_ID, range=new_row_range,
valueInputOption='USER_ENTERED', body=Body).execute()

