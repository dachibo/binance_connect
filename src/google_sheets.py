import gspread
import os


def google_sheets_update(row: list):
    creds_json = os.path.dirname(__file__).replace('/src', "") + "/credentials.json"
    if os.path.exists(creds_json):
        gc = gspread.service_account(filename=creds_json)
        sheet = gc.open(title="BinanceBot")
        sheet.sheet1.append_row(row)
