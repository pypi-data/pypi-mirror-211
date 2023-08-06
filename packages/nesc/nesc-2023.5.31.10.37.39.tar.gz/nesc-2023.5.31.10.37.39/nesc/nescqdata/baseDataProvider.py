import os
import re
from enum import Enum

import dask.dataframe as dd
import pandas as pd
import pyarrow as pa

from .selfException import InvalidTypeError, ItemNotFoundError
from . import utils, columnsMap


# columns need to transform   '10|20' --> [10, 20]
QUEUE_TO_TRANSFORM = ["buypricequeue", "buyorderqtyqueue", "sellpricequeue", "sellorderqtyqueue",
                      "buyorderqueue", "sellorderqueue", "buynumordersqueue", "sellnumordersqueue"]
HDFS_BASE_PATH = "/user/smartdata_quot/hive_db/smartdata_quot.db"
TABLE_TYPE_MAP = {
    "stock": "md_stock",
    "index": "md_index",
    "bond": "md_bond",
    "fund": "md_fund",
    "option": "md_option",
    "transaction": "md_transaction",
    "order": "md_order"
}
COLUMNS_MAP = {
    "stock": columnsMap.stock_columns,
    "index": columnsMap.index_columns,
    "option": columnsMap.option_columns,
    "transaction": columnsMap.transaction_columns,
    "fund": columnsMap.fund_columns,
    "order": columnsMap.order_columns,
    "bond": columnsMap.bond_columns
}


class MarketEnum(str, Enum):
    sse = '101'  # 上交所
    sz = '102'  # 深交所


class BaseDataProvider(object):
    # Stock-股票，Index-指数，Transaction-逐笔成交，Order-逐笔委托，Kline1M4ZT-分钟K线，
    #             Kline5M4ZT-5分钟K线，Kline10M4ZT-10分钟K线，Kline60M4ZT-60分钟K线，EnhancedKline1M-增强K线，
    #             EnhancedKline5M-增强5分钟K线，EnhancedKline10M-增强10分钟K线，EnhancedKline60M-增强60分钟K线
    TABLE_TYPE_PLUS = {"stock", "index", "transaction", "order", "kline1m4zt", "kline5m4zt",
                       "kline10m4zt", "kline60m4zt", "enhancedkline1m", "enhancedkline5m", "enhancedkline10m",
                       "enhancedkline60m"}
    TABLE_TYPE = {"stock", "index", "transaction", "order", "kline1m4zt", "enhancedkline1m"}
    TABLE_TYPE_NEED_2_TRANS = {"stock"}

    def __init__(self, dfs=None):
        self.dfs = pa.hdfs.connect() if dfs is None else dfs

    def __trans_format_4_df(self, df, table_type):
        """将以‘|’分割的队列转成list类型返回"""
        if table_type in self.TABLE_TYPE_NEED_2_TRANS and set(QUEUE_TO_TRANSFORM).issubset(df.columns):
            # df[QUEUE_TO_TRANSFORM] = df[QUEUE_TO_TRANSFORM].applymap(self.__trans_str_queue_2_list)
            df[QUEUE_TO_TRANSFORM] = df[QUEUE_TO_TRANSFORM].apply(lambda x: x.str.split('|'))
        return df

    @staticmethod
    def __trans_str_queue_2_list(value):
        """按‘|’分割，并转int返回list"""
        if isinstance(value, str):
            return [int(i) for i in value.split("|") if i != ""]
        else:
            return value

    def __end_process(self, df, table_type, sort_by_receive_time, trading_phase_code):
        """收尾处理，包括数据类型转换，排序，及筛选"""
        if {'id', 'date'}.issubset(df.columns):
            df.drop(labels=['id', 'date'], axis=1, inplace=True)
        df = self.__filter_by_trading_phase_code(df, trading_phase_code)
        if 'receivedatetime' in df.columns and sort_by_receive_time:
            df.sort_values(by=["receivedatetime"], inplace=True)
        elif {"nescsecurityid", "mddate", "mdtime"}.issubset(df.columns) and not sort_by_receive_time:
            df.sort_values(by=["nescsecurityid", "mddate", "mdtime"], ascending=[True, True, True], inplace=True)
        df.rename(columns=COLUMNS_MAP[table_type], inplace=True)
        return df.reset_index(drop=True)

    @staticmethod
    def __filter_by_trading_phase_code(df, trading_phase_code=None):
        """根据trading_phase_code筛选"""
        if trading_phase_code is None:
            trading_phase_code = []
        if 'tradingphasecode' in df.columns:
            return df[df.tradingphasecode.isin(trading_phase_code)] if trading_phase_code else df
        else:
            return df

    def __get_loop_df_from_list(self, security_path, loop_list, df_r, columns):
        files = []
        for day in loop_list:
            file_path = os.path.join(security_path, f"date={day}")
            if self.dfs.exists(file_path):
                files.extend(utils.get_hdfs_file_path(self.dfs, file_path))
        df = dd.read_parquet(files, engine="pyarrow", columns=columns).compute(num_worker=4)
        df_r = df_r.append(df, ignore_index=True)
        return df_r

    def _get_one_month_security_ids(self, year_month: str, market: MarketEnum):
        return []

    def get_data_by_year_month(self, table_type, security_id,
                               year_month, trading_phase_code=None, sort_by_receive_time=False,
                               need_trans_str_2_list=True, columns=None):
        """
        按月取数据
        :param table_type:           证券类型 如Stock、Index、Transaction、Order、Kline1M4ZT、EnhancedKline1M
        :param security_id:          证券id "000001.SH",若为‘*.SH’或‘*.SZ’表示上交所全市场或深交所全市场
        :param year_month:           年月如"201803",格式为六位字符串
        :param trading_phase_code:   过滤出需要的交易阶段代码，默认为空不过滤
        :param sort_by_receive_time: 是否按照ReceiveTime字段排序，默认为否不排序
        :param need_trans_str_2_list: 是否需要将委托队列等转换成列表，默认True，如果不需要可关闭，将极大提高数据获取效率
        :param columns: str|list     DataFrame指定列名读取，默认全部
        :return:                     Pandas DataFrame
        """
        table_type_low = table_type.lower()
        if table_type_low not in self.TABLE_TYPE:
            raise InvalidTypeError(f"Table_type {table_type} not exists")
        utils.check_year_month(year_month)
        utils.valid_month(year_month)
        if trading_phase_code is None:
            trading_phase_code = []
        columns = self.trans_columns_2_low(columns)
        df_r = pd.DataFrame()
        if security_id == '*.SH' and table_type_low == 'stock':
            df_r = self._get_parquet_data_by_file_list(df_r, table_type, table_type_low, year_month,
                                                       columns, need_trans_str_2_list, MarketEnum.sse)
        elif security_id == '*.SZ' and table_type == 'stock':
            df_r = self._get_parquet_data_by_file_list(df_r, table_type, table_type_low, year_month,
                                                       columns, need_trans_str_2_list, MarketEnum.sz)
        else:
            df_r = self._get_data_by_year_month(security_id, table_type_low, year_month, columns)
            if need_trans_str_2_list:
                df_r = self.__trans_format_4_df(df_r, table_type_low)
        return self.__end_process(df_r, table_type_low, sort_by_receive_time, trading_phase_code)

    @staticmethod
    def trans_columns_2_low(columns):
        if columns is not None:
            if isinstance(columns, str):
                columns = columns.lower()
            elif isinstance(columns, list):
                columns = [i.lower() for i in columns]
            else:
                raise InvalidTypeError("columns with wrong type !")
        return columns

    def _get_parquet_data_by_file_list(self, df_r, table_type, table_type_low, year_month,
                                       columns, need_trans_str_2_list, market):
        security_ids = self._get_one_month_security_ids(year_month, market)
        file_path_list = [os.path.join(HDFS_BASE_PATH, TABLE_TYPE_MAP[table_type_low],
                                       f"id={security_id}", f"date={year_month}")
                          for security_id in security_ids]
        parquet_file_list = []
        for file_path in file_path_list:
            parquet_file_list.extend(utils.get_hdfs_file_path(self.dfs, file_path))
        if parquet_file_list:
            df_r = dd.read_parquet(parquet_file_list, engine="pyarrow", columns=columns)
            if need_trans_str_2_list and table_type in self.TABLE_TYPE_NEED_2_TRANS:
                df_r[QUEUE_TO_TRANSFORM] = df_r[QUEUE_TO_TRANSFORM].apply(lambda x: x.str.split('|'), axis=1)
            df_r = df_r.compute(scheduler="processes", num_workers=20)
        return df_r

    def _get_data_by_year_month(self, security_id, table_type_low, year_month, columns):
        security_path = os.path.join(HDFS_BASE_PATH, TABLE_TYPE_MAP[table_type_low], f"id={security_id}")
        file_path = os.path.join(security_path, f"date={year_month}")
        # 存在月份的文件
        df_r = pd.DataFrame()
        if self.dfs.exists(file_path):
            df = dd.read_parquet(utils.get_hdfs_file_path(self.dfs, file_path),
                                 engine="pyarrow", columns=columns).compute()
            df_r = df_r.append(df, ignore_index=True)
        else:
            if not self.dfs.exists(security_path):
                raise OSError(f"Security {security_id} not exists")
            date_dir_paths = utils.get_hdfs_file_path(self.dfs, security_path)
            pattern = re.compile(f"date={year_month}" + "\d{2}$")
            src_list = [path for path in date_dir_paths if pattern.search(path)]
            for src_file in src_list:
                df = dd.read_parquet(utils.get_hdfs_file_path(self.dfs, src_file),
                                     engine="pyarrow", columns=columns).compute()
                df_r = df_r.append(df, ignore_index=True)
        return df_r

    def get_data_by_date(self, table_type, security_id, date, trading_phase_code=None,
                         sort_by_receive_time=False, need_trans_str_2_list=True, columns=None):
        """
        按天取数据
        :param table_type: 数据表名称(Stock-股票，Index-指数，Transaction-逐笔成交，Order-逐笔委托，
            Kline1M4ZT-分钟K线，EnhancedKline1M-增强K线)
        :param security_id: 证券ID
        :param date: 年月日，格式为YYYYmmdd
        :param trading_phase_code: 取哪些市场阶段状态，默认取所有。所需的交易阶段代码(‘0’表示开盘前，启动。‘1’表示开盘集合竞价。
            ‘2’表示开盘集合竞价阶段结束到连续竞价阶段开始之前。‘3’表示连续竞价。‘4’表示中午休市。‘5’表示收盘集合竞价。‘6’表示已闭市。
            ‘7’表示盘后交易（实际未使用）。)。<br/>**注意：TRANSACTION和ORDER和KLINE1M4ZT无此参数**
        :param sort_by_receive_time: 默认为False，按数据到达时间排序，True-按ReceiveDateTime排序，False-按MDTime排序
        :param need_trans_str_2_list: 是否需要将委托队列等转换成列表，默认True，如果不需要可关闭，将极大提高数据获取效率
        :param columns: DataFrame指定列名读取，默认全部
        :return: DataFrame
        """
        table_type_low = table_type.lower()
        if table_type_low not in self.TABLE_TYPE:
            raise InvalidTypeError(f"Table_type {table_type} not exists")
        utils.check_date(date)
        utils.valid_date(date)
        if trading_phase_code is None:
            trading_phase_code = []
        columns = self.trans_columns_2_low(columns)
        security_path = os.path.join(HDFS_BASE_PATH, TABLE_TYPE_MAP[table_type_low], f"id={security_id}")
        file_path = os.path.join(security_path, f"date={date}")
        if self.dfs.exists(file_path):  # 存在日期date的路徑，到天
            df = dd.read_parquet(utils.get_hdfs_file_path(self.dfs, file_path),
                                 engine="pyarrow", columns=columns).compute()
        elif self.dfs.exists(os.path.join(security_path, f"date={date[:6]}")):  # 存在当月的路径
            files = utils.get_hdfs_file_path(self.dfs, os.path.join(security_path, f"date={date[:6]}"))
            if not files:
                return pd.DataFrame()
            df = dd.read_parquet(files, engine="pyarrow", columns=columns).compute()
            df = df[df.mddate == int(date)]
        else:
            raise ValueError(f"No {date} data for {security_id} was found")
        if need_trans_str_2_list:
            df = self.__trans_format_4_df(df, table_type_low)
        return self.__end_process(df, table_type_low, sort_by_receive_time, trading_phase_code)

    def get_data_by_time_frame(self, table_type, security_id, start_time,
                               end_time, trading_phase_code=None, sort_by_receive_time=False,
                               need_trans_str_2_list=True, columns: list=None):
        """
        按时间窗口取数据
        :param table_type: 数据表名称(Stock-股票，Index-指数，Transaction-逐笔成交，Order-逐笔委托，Kline1M4ZT-分钟K线，
            Kline5M4ZT-5分钟K线，Kline10M4ZT-10分钟K线，Kline60M4ZT-60分钟K线，EnhancedKline1M-增强K线，
            EnhancedKline5M-增强5分钟K线，EnhancedKline10M-增强10分钟K线，EnhancedKline60M-增强60分钟K线)
        :param security_id: 证券ID
        :param start_time: 开始时间，格式为’YYYYmmdd HHMMSS’
        :param end_time: 结束时间，格式为’YYYYmmdd HHMMSS’
        :param trading_phase_code: 取哪些市场阶段状态，默认取所有。所需的交易阶段代码(‘0’表示开盘前，启动。‘1’表示开盘集合竞价。
            ‘2’表示开盘集合竞价阶段结束到连续竞价阶段开始之前。‘3’表示连续竞价。‘4’表示中午休市。‘5’表示收盘集合竞价。‘6’表示已闭市。
            ‘7’表示盘后交易（实际未使用）。)。<br/>**注意：TRANSACTION和ORDER和KLINE1M4ZT无此参数**
        :param sort_by_receive_time: 默认为False，按数据到达时间排序，True-按ReceiveDateTime排序，False-按MDTime排序。
        :param need_trans_str_2_list: 是否需要将委托队列等转换成列表，默认True，如果不需要可关闭，将极大提高数据获取效率
        :param columns: DataFrame指定列名读取，默认全部
        :return: DataFrame
        """
        if columns and not {'mddate', 'mdtime'}.issubset(columns):
            columns.extend(['mddate', 'mdtime'])
        table_type_low = table_type.lower()
        if table_type_low not in self.TABLE_TYPE_PLUS:
            raise InvalidTypeError(f"Table_type {table_type} not exists")
        utils.check_time(start_time)
        utils.check_time(end_time)
        utils.valid_time(start_time=start_time, end_time=end_time)
        if trading_phase_code is None:
            trading_phase_code = []
        columns = self.trans_columns_2_low(columns)
        s_year_month, s_day, s_time = utils.get_year_month_and_day(start_time)
        e_year_month, e_day, e_time = utils.get_year_month_and_day(end_time)
        security_path = os.path.join(HDFS_BASE_PATH, TABLE_TYPE_MAP[table_type_low], f"id={security_id}")
        months = utils.get_month_iter(start_month=s_year_month, end_month=e_year_month)
        df_r = pd.DataFrame()
        if not self.dfs.exists(security_path):
            raise ItemNotFoundError(security_id)
        df_r = self.__get_loop_df_from_list(security_path, months, df_r, columns)
        if df_r.empty and len(self.dfs.ls(security_path)) > 0:  # 没查到数据，但是存在文件，尝试用date作为路径查找
            days = utils.get_date_iter(start_date=s_day, end_date=e_day)
            df_r = self.__get_loop_df_from_list(security_path, days, df_r, columns)
        if df_r.empty:
            return df_r
        # 筛选符合的时间段
        d_filter = ((df_r["mddate"] > int(s_day)) |
                    ((df_r["mddate"] == int(s_day)) & (df_r["mdtime"] >= 1000 * int(s_time)))) & \
                   ((df_r["mddate"] < int(e_day)) |
                    ((df_r["mddate"] == int(e_day)) & (df_r["mdtime"] <= 1000 * int(e_time))))
        df_r = df_r[d_filter]
        if need_trans_str_2_list:
            df_r = self.__trans_format_4_df(df_r, table_type_low)
        return self.__end_process(df_r, table_type_low, sort_by_receive_time, trading_phase_code)


class TypeOfProvider(BaseDataProvider):

    def __init__(self, data_type, dfs=None):
        super(TypeOfProvider, self).__init__(dfs)
        self.TABLE_TYPE = {data_type}
        self.TABLE_TYPE_NEED_2_TRANS = {data_type}
        self.TABLE_TYPE_PLUS = {data_type}
