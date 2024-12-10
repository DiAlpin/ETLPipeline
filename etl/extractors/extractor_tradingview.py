
import functools
import pandas as pd
import pyarrow as pa
import networkx as nx
from typing import List
from pydantic import BaseModel
from etl.utils.tradingview import TVHistoricalPrices
from etl.utils.retry_decorator import retry
from etl.trackers.perf_logging import performace_logging
from etl.trackers.tracker_extractor import ExtractorTraker
from etl.datasets.dataset import Dataset


class LastPriceTradingviewExtractorModel(BaseModel):
    exchange: str
    symbols: List[str]
    interval: str
    data_source_label: str


class LastPriceTradingviewExtractor(ExtractorTraker):
    def __init__(self, config):
        self._exchange = config['exchange']
        self._symbols = config['symbols']
        self._interval = config['interval']
        self._n_bar = 1
        self.data_source_label = config['data_source_label']

    @retry(max_attempts=5, delay=1, backoff_factor=2)
    def _get_data_for_symbol(self, symbol):
        tv = TVHistoricalPrices(exchange=self._exchange)
        try:
            df = tv.get_hist(
                symbol=symbol,
                interval=self._interval, 
                n_bars=self._n_bar
            )
            if df is None or df.empty:
                raise ValueError(f"No data retrieved for symbol: {symbol}")
            return df
        
        except Exception as e:
            print(f'Error extracting data for {symbol}: {e}')
            raise
        finally:
            del tv 
    

    @performace_logging
    def _extract_df(self):
        dfs = [self._get_data_for_symbol(s) for s in self._symbols]
        return pd.concat(dfs)

    def __call__(self):
        df = self._extract_df()
        table = pa.Table.from_pandas(df)
        return Dataset(table, self.tracker_build_metadata(table))






class PickDayPriceTradingviewExtractorModel(BaseModel):
    exchange: str
    symbols: List[str]
    piking_date: str
    data_source_label: str


class PickDayPriceTradingviewExtractor(ExtractorTraker):
    def __init__(self, config):
        self._exchange = config['exchange']
        self._symbols = config['symbols']
        self._interval = '1D'
        self._piking_date = config['piking_date'] #TODO: add a standat dateformat
        self._n_bar = 13
        self.data_source_label = config['data_source_label'] 

    @performace_logging
    def _extract_df(self, get_price_method):
        dfs = []
        for s in self._symbols:
            _df = get_price_method(s)
            dfs.append(
                _df[_df['datetime'] == self._piking_date].copy()
            )
        return pd.concat(dfs)

    def __call__(self):
        tvph = TVHistoricalPrices(exchange=self._exchange)
        get_price_method = functools.partial(
                                tvph.get_hist, 
                                interval=self._interval, 
                                n_bars=self._n_bar)
        
        df = self._extract_df(get_price_method)
        table = pa.Table.from_pandas(df)
        return Data(table, self.tracker_build_metadata(table))
    



class OhlcTradingviewExtractorModel(BaseModel):
    exchange: str
    symbol: str
    interval: str
    candles: int
    data_source_label: str


class OhlcTradingviewExtractor(ExtractorTraker):
    def __init__(self, config):
        self._exchange = config['exchange']
        self._symbol = config['symbol']
        self._interval = config['interval']
        self._n_bar = config['candles']
        self.data_source_label = config['data_source_label']

    @performace_logging
    def _extract_df(self, get_price_method):
        df = get_price_method(self._symbol)
        return df

    def __call__(self):
        tvph = TVHistoricalPrices(exchange=self._exchange)
        get_price_method = functools.partial(
                            tvph.get_hist, 
                            interval=self._interval, 
                            n_bars=self._n_bar)

        df = _extract_df(get_price_method)
        table = pa.Table.from_pandas(df)
        return Dataset(table, self.tracker_build_metadata(table))
