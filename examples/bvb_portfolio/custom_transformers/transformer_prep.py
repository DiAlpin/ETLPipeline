import numpy as np
import pandas as pd
from etl import PandasTransformer
from etl import CustomPDTransformerTraker


class PortfolioTransformer(PandasTransformer, CustomPDTransformerTraker):
    def __init__(self, config):
        self._config = config
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        ### start
        df['value'] = df['price'] * df['shares']
        df['portfolio_weight'] = df['value'] / df['value'].sum()
        df['bet_weight'] = df['bet_weight'] / 10000
        df['name'] = np.where(df['portfolio_name'].isnull(), df['bet_name'], df['portfolio_name'])
        ### end
        return df
