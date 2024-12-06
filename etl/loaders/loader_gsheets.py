import pandas as pd
import gspread
import pyarrow as pa
from pydantic import BaseModel
from etl.trackers.perf_logging import performace_logging
from etl.trackers.tracker_basic import BasicTracker
from etl.datasets.dataset import Dataset
from etl.utils.google_sheets import GoogleSheet

class GoogleSheetsLoaderModel(BaseModel):
    workbook_id: str
    sheet_name: str
    replace: bool


class GoogleSheetsLoader(BasicTracker):
    def __init__(self, config):
        self._workbook_id = config['workbook_id']
        self._sheet_name = config['sheet_name']
        self._replace = config['replace']

    @performace_logging
    def _load_df(self, df):
        with GoogleSheet(self._workbook_id, self._sheet_name) as gs:
            gs.insert_df(df, replace=self._replace)

    def __call__(self, dataset):
        df = dataset.table.to_pandas()
        
        self._load_df(df)

        dataset.append_new_metadata(
            new_metadata=self.tracker_build_metadata())
        return dataset
