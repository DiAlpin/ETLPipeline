import pandas as pd 
import networkx as nx
from pydantic import BaseModel
from etl.transformers.base.pandas_transformer import PandasTransformer
from etl.trackers.i_tracker import ITracker
from etl.datasets.metadata import Metadata



class Tracker(ITracker):
    def gen_history(self):
        his = nx.DiGraph()
        for node, val in self._columns.items():
            his.add_node(
                node, 
                label=self._description.format(val=val)
            )
        return his


class FillnaTransformerModel(BaseModel):
    columns: dict


class FillnaTransformer(PandasTransformer, Tracker):
    def __init__(self, config):
        self._columns = config['columns']
        self._description = 'fill nan values with {val}'
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        current_cols = set(df.columns.tolist())

        for c in self._columns.keys():
            assert c in current_cols, f'Column {c} not found in DataFrame'
        
        df.fillna(self._columns, inplace=True)
        
        return df