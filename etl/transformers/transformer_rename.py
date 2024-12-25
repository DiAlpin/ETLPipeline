import pandas as pd 
import networkx as nx
from pydantic import BaseModel
from etl.transformers.base.pandas_transformer import PandasTransformer
from etl.trackers.i_tracker import ITracker
from etl.datasets.metadata import Metadata



class Tracker(ITracker):
    def gen_history(self):
        his = nx.DiGraph()
        for old, new in self._columns.items():
            his.add_node(new, label=f'{old} rename to {new}')
            his.add_edge(old, new)
        return his


class RenameTransformerModel(BaseModel):
    columns: dict

class RenameTransformer(PandasTransformer, Tracker):
    def __init__(self, config):
        self._columns = config['columns']

    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns=self._columns, inplace=True)
        return df
