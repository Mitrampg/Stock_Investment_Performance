import yfinance as yf
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# Jalur absolut ke file JSON
dir_path = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(dir_path, "stock_journal.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1MkxeEFOgfe7vZLXQ10wB02COlQ_aw3URamOSACP_IHg"

cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=cred)
sheet = service.spreadsheets()
range_to_get = "journal!B10:B100"

result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_to_get).execute()
values = result.get('values', [])

for row in values:
    emiten_code = row[0]
    emiten_list = {}
    for i, j in enumerate(values, start=10):
        emiten_list[f"F{i}"] = j[0]

for i, j in emiten_list.items():
    stock = yf.Ticker(f"{j}.JK")
    history = stock.history(period="1d")
    values = [[history['Close'].iloc[-1]] if not history.empty else [None]]
    rangeName = f"journal!{i}"
    body = {
        'values': values,
    }
    result = sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeName,
        valueInputOption='USER_ENTERED', body=body).execute()


    



