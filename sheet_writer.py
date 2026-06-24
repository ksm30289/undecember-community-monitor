import os
import json
import gspread

from google.oauth2.service_account import Credentials

SHEET_NAME = "언디셈버_KR_동향"


def get_sheet():

    credentials_info = json.loads(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    creds = Credentials.from_service_account_info(
        credentials_info,
        scopes=scopes
    )

    gc = gspread.authorize(creds)

    spreadsheet = gc.open_by_key(
        os.getenv("SPREADSHEET_ID")
    )

    return spreadsheet.worksheet(
        SHEET_NAME
    )
