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

# Permintaan untuk mengosongkan kolom B dan C mulai dari baris kedua
clear_sheet_request = {
    "updateCells": {
        "range": {
            "sheetId": 1186258338,  # ID dari sheet yang akan dikosongkan
            "startRowIndex": 1,  # Mulai dari baris kedua
            "endRowIndex": 1000,  # Sampai baris ke-1000, sesuaikan sesuai kebutuhan
            "startColumnIndex": 1,  # Mulai dari kolom B
            "endColumnIndex": 3  # Sampai setelah kolom C
        },
        "fields": "userEnteredValue"  # Mengosongkan sel
    }
}

# Menambahkan permintaan pengosongan ke batch update body
batch_update_body = {"requests": [clear_sheet_request]}

# Melakukan batch update untuk mengosongkan kolom B dan C
service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_update_body).execute()

batch_update_body = {
    "requests": [
        # Permintaan pertama: Mengosongkan sel dengan copyPaste
        {"copyPaste": {
            "source": {"sheetId": 0, "startRowIndex": 9, "endRowIndex": 100, "startColumnIndex": 1, "endColumnIndex": 2},  # A3:A23
            "destination": {"sheetId": 1186258338, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": 0, "endColumnIndex": 1},  # A2:A22
            "pasteType": "PASTE_VALUES"
        }},
        {"copyPaste": {
            "source": {"sheetId": 0, "startRowIndex": 9, "endRowIndex": 100, "startColumnIndex": 4, "endColumnIndex": 5},  # A3:A23
            "destination": {"sheetId": 1186258338, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": 3, "endColumnIndex": 4},  # A2:A22
            "pasteType": "PASTE_VALUES"
        }}   ]}

service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_update_body).execute()

range_to_get = "journal!B10:B100"
result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_to_get).execute()
values = result.get('values', [])

for row in values:
    # Asumsikan sel B11 hanya memiliki satu nilai
    emiten_code = row[0]
    emiten_list_sector = {}
    emiten_list_marketcap = {}
    for i, j in enumerate(values, start=2):
        emiten_list_sector[f"B{i}"] = j[0]
        emiten_list_marketcap[f"C{i}"] = j[0]

for i, j in emiten_list_sector.items():
    sectors = [[yf.Ticker(f"{j}.JK").info['sector']]]
    rangeName = f"sector!{i}"
    body = {
        'values': sectors,
    }
    result = sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeName,
        valueInputOption='USER_ENTERED', body=body).execute()
    
for i, j in emiten_list_marketcap.items():
    marketcap = [[yf.Ticker(f"{j}.JK").info['marketCap']]]
    rangeName = f"sector!{i}"
    body = {
        'values': marketcap,
    }
    result = sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeName,
        valueInputOption='USER_ENTERED', body=body).execute()