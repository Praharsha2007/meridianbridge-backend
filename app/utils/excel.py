import gspread
from google.oauth2.service_account import Credentials
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]




def _get_sheet(sheet_name: str, headers: list):
    SHEET_ID = os.environ.get("GOOGLE_SHEET_ID")
    # Production (Railway): read from GOOGLE_CREDS_JSON env variable
    # Local development: read from service_account.json file
    creds_json = os.environ.get("GOOGLE_CREDS_JSON")

    if creds_json:
        creds_info = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    else:
        creds_path = os.environ.get("GOOGLE_CREDS_PATH", "service_account.json")
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(SHEET_ID)

    try:
        ws = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers))
        ws.append_row(headers, value_input_option="USER_ENTERED")

    return ws


def save_to_excel(sheet_name: str, headers: list, row_data: list):
    try:
        ws = _get_sheet(sheet_name, headers)
        safe_row = [str(v) if v is not None else "" for v in row_data]
        ws.append_row(safe_row, value_input_option="USER_ENTERED")
    except Exception as e:
        import traceback
        print("Google Sheets Error:", str(e))
        print("Full traceback:", traceback.format_exc())
        raise