import pyarrow as pa
import networkx as nx
from etl.datasets.metadata import Metadata


class Dataset:
    def __init__(
        self, 
        pa_table: pa.Table, 
        metadata: Metadata
    ):
        self._table = pa_table
        self._metadata = metadata
    
    @property
    def table(self) -> pa.Table:
        return self._table
    
    @property
    def metadata(self):
        return self._metadata

    def set_table(self, table):
        self._table = table

    def set_metadata(self, metadata):
        self._metadata = metadata

    def append_new_metadata(self, new_metadata):
        """"""
        self._metadata += new_metadata
