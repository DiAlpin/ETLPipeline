import pandas as pd 
import networkx as nx
from pydantic import BaseModel
from typing import Literal
from etl.transformers.base.pandas_transformer import PandasTransformer
from etl.trackers.i_tracker import ITracker
from etl.datasets.metadata import Metadata



class Tracker(ITracker):
    def gen_history(self):
        his = nx.DiGraph()
        his.add_node(
            self._column, 
            label=self._description
        )
        return his


class StringFilterTransformerModel(BaseModel):
    column: str
    operation: Literal['isin', 'notin']
    args: list


class StringFilterTransformer(PandasTransformer, Tracker):
    def __init__(self, config):
        self._column = config['column']
        self._operation = config['operation']
        self._args = config['args']
        self._description = f'{self._args} {self._operation} {self._column}'.replace("'", '')
        
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._operation == 'isin':
            df = df[df[self._column].isin(self._args)].copy()

        elif self._operation == 'notin':
            df = df[~df[self._column].isin(self._args)].copy()
        
        return df