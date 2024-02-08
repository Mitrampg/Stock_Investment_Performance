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


range_to_get = "history_performance!A:A"

# Menggunakan API untuk mengambil nilai dari sel
result = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_to_get).execute()
values = result.get('values', [])

total_baris = len(values)
if total_baris > 23:
    total_baris_copy = total_baris - 22
    total_baris_paste = 23
else:
    total_baris_copy = 1
    total_baris_paste = total_baris
    

batch_update_body = {
    "requests": [
        {"copyPaste": {
            "source": {"sheetId": 1159629461, "startRowIndex": total_baris_copy, "endRowIndex": total_baris, "startColumnIndex": 0, "endColumnIndex": 1},  # A3:A23
            "destination": {"sheetId": 606892635, "startRowIndex": 1, "endRowIndex": total_baris_paste, "startColumnIndex": 0, "endColumnIndex": 1},  # A2:A22
            "pasteType": "PASTE_VALUES"
        }},
        {"copyPaste": {
            "source": {"sheetId": 1159629461, "startRowIndex": total_baris_copy, "endRowIndex": total_baris, "startColumnIndex": 1, "endColumnIndex": 2},  # A3:A23
            "destination": {"sheetId": 606892635, "startRowIndex": 1, "endRowIndex": total_baris_paste, "startColumnIndex": 1, "endColumnIndex": 2},  # A2:A22
            "pasteType": "PASTE_VALUES"
        }},
        {"copyPaste": {
            "source": {"sheetId": 1159629461, "startRowIndex": total_baris_copy, "endRowIndex": total_baris, "startColumnIndex": 3, "endColumnIndex": 4},  # A3:A23
            "destination": {"sheetId": 606892635, "startRowIndex": 1, "endRowIndex": total_baris_paste, "startColumnIndex": 3, "endColumnIndex": 4},  # A2:A22
            "pasteType": "PASTE_VALUES"
        }},
    ]
}

service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=batch_update_body).execute()

