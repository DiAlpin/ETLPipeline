
import pyarrow as pa
from etl.transformers.base.i_transformer import ITransformer
from etl.datasets.dataset import Dataset
from etl.trackers.perf_logging import performace_logging


class PandasTransformer(ITransformer):

    @performace_logging
    def _pandas_transformation(self, df):
        return self.main_transformation(df)

    def __call__(self, dataset: Dataset):
        df = dataset.table.to_pandas()
        df = self._pandas_transformation(df)
        table = pa.Table.from_pandas(df)

        dataset.set_table(table)
        dataset.append_new_metadata(
            new_metadata=self.tracker_build_metadata(), 
            )
        return dataset