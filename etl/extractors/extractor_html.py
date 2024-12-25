import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, PositiveInt
from etl.trackers.perf_logging import performace_logging
from etl.trackers.tracker_extractor import ExtractorTraker
from etl.datasets.dataset import Dataset


class HtmlExtractorModel(BaseModel):
    url: str
    table_id: PositiveInt
    data_source_label: str


class HtmlExtractor(ExtractorTraker):
    def __init__(self, config):
        self._url = config['url']
        self._table_id = config['table_id']
        self.data_source_label = config['data_source_label']
    
    @performace_logging
    def _extract_df(self):
        dfs = pd.read_html(self._url)
        df = dfs[self._table_id]
        return df

    def __call__(self):
        df = self._extract_df()
        tabel = pa.Table.from_pandas(df)
        return Dataset(tabel, self.tracker_build_metadata(tabel))
    
