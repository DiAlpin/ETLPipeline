"""Google Sheet module."""

# Author: Daniel Broboana <>
import os.path

import gspread
import pandas as pd

from etl.utils.misc import get_env_variable
from google.oauth2.credentials import Credentials



def df_to_gs_range(df, header=True):
    if header:
        rg = [list(df.columns)]
    else:
        rg = []
    for i in df.iterrows():
        rg.append(i[1].tolist())
    return rg


class GoogleSheet:
    def __init__(self, workbook_id, sheet_name):
        self._workbook_id = workbook_id
        self._sheet_name = sheet_name
        self._token_path = rf'{get_env_variable('PIPELINEPATH')}/.token.json'
        self._scope = ["https://www.googleapis.com/auth/spreadsheets"]
        self._sheet = None

    def _load_credeantials(self):
        if os.path.exists(self._token_path):
            return Credentials.from_authorized_user_file(
                        self._token_path, self._scope)
        raise ValueError(f'Token dosen t exist on path {self._token_path}!')

    def __enter__(self):
        creds = self._load_credeantials()
        client = gspread.authorize(creds)
        workbook = client.open_by_key(self._workbook_id)
        self._sheet = workbook.worksheet(self._sheet_name)

        return self


    def insert_df(self, df, replace):
        if replace:
            self._sheet.clear()
            start_cell = 'A1'
        else:
            col_values = self._sheet.col_values(1)
            start_cell = f'A{len(col_values) + 1}'
        
        gs_range = df_to_gs_range(df, header=replace)
        self._sheet.update(gs_range, start_cell)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
        