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


def append_post(post):

    sheet = get_sheet()

    sheet.append_row([
        post.get("collectedAt", ""),
        post.get("createdAt", ""),
        post.get("source", ""),
        post.get("title", ""),
        post.get("content", ""),
        post.get("url", ""),
        "",
        "",
        "",
        "",
        "",
        post.get("postId", "")
    ])

def post_exists(post_id):

    sheet = get_sheet()

    ids = sheet.col_values(12)

    return post_id in ids
