import pandas as pd
import pyarrow as pa
from pydantic import BaseModel
from typing import Literal
from etl.datasets.dataset import Dataset
from etl.trackers.perf_logging import performace_logging
from etl.trackers.tracker_blender import BlenderTraker
from etl.utils.blenders import set_suffixes
from etl.datasets.metadata import merge_metadatas

class MergeBlenderModel(BaseModel):
    blend_method: Literal[
        'LeftJoin', 'RightJoin', 
        'OuterJoin', 'InnerJoin', 
        'CrossJoin'
        ]
    on_column: str
    suffixes: tuple | None = None


class MergeBlender(BlenderTraker):
    def __init__(self, config):
        self._on_column = config['on_column']
        self._suffixes = set_suffixes(config)
        self._blend_method = config['blend_method']
        self._left_ds = None
        self._right_ds = None
        self._description = f'{self._blend_method} ' \
                          + f'on column {self._on_column}'
    def _set_datasets(self, datasets):
        assert len(datasets) == 2, \
            f'Invalid datasets, list should contain 2 datasets'     
        self._left_ds = datasets[0]
        self._right_ds = datasets[1]


    @performace_logging
    def _blend_df(self):
        how = self._blend_method.replace('Join', '').lower()
        df = pd.merge(
            self._left_ds.table.to_pandas(),
            self._right_ds.table.to_pandas(),
            how=how,
            on=self._on_column,
            suffixes=self._suffixes
        )
        return df

    def __call__(self, datasets):
        self._set_datasets(datasets)
        df = self._blend_df()
        
        tabel = pa.Table.from_pandas(df)
        metadata = merge_metadatas(
            self._left_ds.metadata,
            self._right_ds.metadata
        )
        dataset = Dataset(tabel, metadata)
        dataset.append_new_metadata(
            new_metadata=self.tracker_build_metadata()
        )
        return dataset
