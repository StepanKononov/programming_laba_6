import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import creds

"""
Эта ветка для Видео о записи в электронные таблицы Google Sheets
с помощью API Google Sheets 
https://youtu.be/RV-aN_WEFPE
"""


def get_service_simple():
    return build('sheets', 'v4', developerKey=creds.api_key)


def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/creds/sacc1.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


sheet = get_service_sacc().spreadsheets()

sheet_id = "1QKMBoeI1FQjWIPEaveyJ6X-L4jXKqOZmTy3laP7ifjY"


def update_sheet_value(data):
    resp = sheet.values().update(
        spreadsheetId=sheet_id,
        range="Лист2!A1",
        valueInputOption="RAW",
        body={'values': data}).execute()
