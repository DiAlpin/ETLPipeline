import pandas as pd 
import networkx as nx
from pydantic import BaseModel
from etl.transformers.base.pandas_transformer import PandasTransformer
from etl.datasets.metadata import Metadata
from etl.trackers.tracker_basic import BasicTracker


class KeepTransformerModel(BaseModel):
    columns_to_keep: list
    ascending_by: str | None = None
    descending_by: str | None = None



class KeepTransformer(PandasTransformer, BasicTracker):
    def __init__(self, config):
        self._columns = config['columns_to_keep']
        self._ascending_by = config.get('ascending_by')
        self._descending_by = config.get('descending_by')
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[self._columns].copy()

        if self._ascending_by:
            df = df.sort_values(self._ascending_by, ascending=True)
        if self._descending_by:
            df = df.sort_values(self._descending_by, ascending=False)

        return df