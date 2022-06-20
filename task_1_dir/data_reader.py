import os
from datetime import datetime
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import creds
import numpy as np
import pandas as pd


def get_service_simple():
    return build('sheets', 'v4', developerKey=creds.api_key)


def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/creds/sacc1.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


def get_data():
    service = get_service_sacc()
    sheet = service.spreadsheets()

    sheet_id = "1QKMBoeI1FQjWIPEaveyJ6X-L4jXKqOZmTy3laP7ifjY"

    resp = sheet.values().get(spreadsheetId=sheet_id, range="Лист4").execute()
    all_data = resp["values"]
    date = list()
    values = list()

    for i in range(1, len(resp["values"])):
        temp = all_data[i]
        values.append(float(temp[1].replace(',', '.')))
        date.append(temp[0][:10])
        #date.append(i)
    df = pd.DataFrame(values, index=date, columns=['Value'])
    df = df.rename_axis("Date")
    #df.to_csv('out.csv')
    return df

get_data()