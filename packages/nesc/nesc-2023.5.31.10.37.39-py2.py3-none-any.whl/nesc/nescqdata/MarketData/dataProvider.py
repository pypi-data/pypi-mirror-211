import os
import dask.dataframe as dd
import pandas as pd

from .. import utils
from ..baseDataProvider import BaseDataProvider, HDFS_BASE_PATH, MarketEnum


STOCK_ID_TABLE = 'md_stockid'


class DataProvider(BaseDataProvider):

    def __init__(self, dfs=None):
        super(DataProvider, self).__init__(dfs)

    def _get_one_month_security_ids(self, year_month: str, market: MarketEnum):
        """
        获取一个月的股票id
        :param year_month: 需要获取数据的月份 年月如"201803",格式为六位字符串
        :param market: MarketEnum 枚举值MarketEnum.sz表示深交所，MarketEnum.sse表示上交所
        :return: 证券id列表
        """
        market_list = [os.path.join(HDFS_BASE_PATH, STOCK_ID_TABLE, f'date={year_month}', f'source={market_name}')
                       for market_name in market.value.split(',')]
        df_r = pd.DataFrame()
        for file_path in market_list:
            if self.dfs.exists(file_path):
                df = dd.read_parquet(utils.get_hdfs_file_path(self.dfs, file_path), engine="pyarrow").compute()
                df_r = df_r.append(df, ignore_index=True)
            else:
                raise ValueError(f"No {year_month} data found, please check.")
        return df_r.drop_duplicates(['nescsecurityid'])['nescsecurityid'].to_list()
