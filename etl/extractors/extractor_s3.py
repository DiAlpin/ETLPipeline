import io
import boto3
import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, PositiveInt
from etl.trackers.perf_logging import performace_logging
from etl.trackers.tracker_extractor import ExtractorTraker
from etl.datasets.dataset import Dataset



class SingleS3ExtractorModel(BaseModel):
    bucket: str
    file_key: str
    aws_credentials: dict | None = None
    delimiter: str | None = None
    skiprows: PositiveInt | None = None
    data_source_label: str


class SingleS3Extractor(ExtractorTraker):
    def __init__(self, config):
        self._aws_credentials = config.get('aws_credentials', {})
        self._s3_resource = boto3.resource('s3', **self._aws_credentials)
        self._s3_client = boto3.client('s3', **self._aws_credentials)
        self._bucket = config['bucket']
        self._file_key = config['file_key']
        self._extension = self._file_key.rsplit('.', 1)[1]
        self._delimiter = config.get('delimiter', None)
        self._skiprows = config.get('skiprows', None)
        self.data_source_label = config['data_source_label']

    def _get_s3_object(self):
        try:
            s3_obj = self._s3_resource.Object(self._bucket, self._file_key )
            raw_data = s3_obj.get()['Body'].read()
            return io.BytesIO(raw_data)
        except Exception as e:
            raise ValueError(f'Reading s3 object failed! {e}') from e

    def _read_csv(self):
        bytes_data = self._get_s3_object()
        return pd.read_csv(bytes_data, delimiter=self._delimiter, skiprows=self._skiprows)

    def _read_parquet(self):
        bytes_data = self._get_s3_object()
        return pd.read_parquet(bytes_data, engine='fastparquet')

    @performace_logging
    def _extract_df(self):
        methods = {
            'csv': self._read_csv,
            'parquet': self._read_parquet,
        }
        read_method = methods[self._extension]
        return read_method()

    def __call__(self):
        df = self._extract_df()
        tabel = pa.Table.from_pandas(df)
        return Dataset(tabel, self.tracker_build_metadata(tabel))



