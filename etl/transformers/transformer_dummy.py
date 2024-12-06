

import pandas as pd 
import networkx as nx
from pydantic import BaseModel
from etl.transformers.base.pandas_transformer import PandasTransformer
from etl.datasets.metadata import Metadata
from etl.trackers.tracker_basic import BasicTracker


class DummyTransformerModel(BaseModel):
    dummy_arg: 'str'


class DummyTransformer(PandasTransformer, BasicTracker):
    """Transformer used to test the infrastructure."""

    def __init__(self, config):
        self._dummy_arg = config['dummy_arg']

    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        df['dummy'] = self._dummy_arg
        return df