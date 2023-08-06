from abc import ABC, abstractmethod

import pandas

from etlframe.Connections.connections import DatabaseConnection, ElasticsearchConnection
from etlframe.Error.error import SqlStatementError
from etlframe.Mapping.dataset import Dataset


class Reader(ABC):
    default_batch_size = 10000
    _columns = None
    _limit_num = None

    def read(self, columns):
        """返回结果列名必须rename"""
        dataset = self.get_dataset(columns)
        # print(dataset.get(1))
        if isinstance(self._limit_num, int):
            dataset = dataset.limit(self._limit_num)
        return dataset

    @abstractmethod
    def get_dataset(self, columns):
        """
        获取数据集
        :param columns:
        :return:
        """
        pass

    @property
    @abstractmethod
    def columns(self):
        """
        获取列名
        :return:
        """
        return self._columns


class DatabaseReader(DatabaseConnection, Reader):

    def __init__(self, db: str,
                 table_name: str,
                 condition: str = None,
                 is_all_columns: bool = True,
                 batch_size: int = None,
                 limit: int = None):
        """

        condition:写法
        condition = lambda x: x['id'] == 10
        condition = 'id = 10'

        :param db: 数据库URI 链接字符串
        :param table_name: 表
        :param all_results: 是否查询出全部字段
        :param condition:查询条件  where后面
        :param batch_size: 每批多少条
        :param limit: 限制多少
        """
        super().__init__(db)
        self.is_all_columns = is_all_columns
        self.table_name = table_name
        self.condition = condition if condition else "1=1"
        self.batch_size = batch_size or self.default_batch_size
        self._limit_num = limit
        self.columns_all = None

    def _get_dataset(self, text):
        return Dataset(
            (r for r in self.db.read(text, batch_size=self.batch_size, columns=self.columns_all)))  # , columns=columns

    def _query_text(self, export_columns: set = None):
        """
        构造SQL查询语句
        如果self.is_all_columns=True  返回全部字段
        需要重新命名的字段 {{数据库字段名:重命名字段名}，{数据库字段名:重命名字段名}}
        需要重新命名的字段 {{数据库字段名:重命名字段名}，{数据库字段名:重命名字段名}}
        :param export_columns: 需要提取的字段
        :return:
        """
        if not self.is_all_columns:
            if not export_columns:  # 不需要全部记录， 也不传需要的列名，直接报错
                raise SqlStatementError()
            else:  # 不需要全部记录，只需要个别记录
                self.columns_all = export_columns
                fields = [col for col in export_columns]
                return " ".join(["select", ",".join(fields), "from", self.table_name])
        else:  # 需要全部记录，但是需要改名
            table_columns: list = self.db.get_table(self.table_name).get_columns()
            self.columns_all = table_columns
            fields = [col for col in table_columns]
            return " ".join(["select", ",".join(fields), "from", self.table_name])

    def get_dataset(self, export_columns: set = None) -> Dataset:
        """
        获取数据集的生成器
        :rtype:
        :param columns:
        :return:
        """
        text = self._query_text(export_columns)  #
        # print(text)
        if isinstance(self.condition, str):
            text = f"{text} where {self.condition}"
            dataset = self._get_dataset(text)
        elif callable(self.condition):
            dataset = self._get_dataset(text).filter(self.condition)
        else:
            raise ValueError("condition 参数类型错误")
        return dataset  # .rename(columns)  # 字段重命名，修改dict的key

    @property
    def columns(self) -> list:
        """
        返回列名的列表
        :return:
        """
        if self.is_all_columns:
            if self._columns is None:
                self._columns = self.db.get_table(self.table_name).get_columns()
        else:
            self._columns = self.columns_all
        return self._columns


class FileReader(Reader):

    def __init__(self, file_path, pd_params=None, limit=None):
        self.file_path = file_path
        self._limit_num = limit
        if pd_params is None:
            pd_params = {}
        pd_params.setdefault("chunksize", self.default_batch_size)
        self.file = pandas.read_csv(self.file_path, **pd_params)

    def _get_records(self, columns):
        for df in self.file:
            df = df.where(df.notnull(), None).reindex(columns=columns).rename(columns=columns)
            for record in df.to_dict("records"):
                yield record

    def get_dataset(self, columns):
        return Dataset(self._get_records(columns))

    @property
    def columns(self):
        if self._columns is None:
            self._columns = [col for col in self.file.read(0).columns]
        return self._columns


class ExcelReader(Reader):

    def __init__(self, file, sheet_name=0, pd_params=None, limit=None, detect_table_border=True):
        if pd_params is None:
            pd_params = {}
        pd_params.setdefault("dtype", 'object')
        self.sheet_name = sheet_name
        self._limit_num = limit
        if isinstance(file, str):
            file = pandas.ExcelFile(file)
            self.df = file.parse(self.sheet_name, **pd_params)
        elif isinstance(file, pandas.ExcelFile):
            self.df = file.parse(self.sheet_name, **pd_params)
        elif isinstance(file, pandas.DataFrame):
            self.df = file
        else:
            raise ValueError(f"file 参数类型错误")
        if detect_table_border:
            self.detect_table_border()

    def get_dataset(self, columns):
        df = self.df.where(self.df.notnull(), None).reindex(columns=columns).rename(columns=columns)
        return Dataset(df.to_dict("records"))

    @property
    def columns(self):
        if self._columns is None:
            self._columns = [col for col in self.df.columns]
        return self._columns

    def detect_table_border(self):
        y, x = self.df.shape
        axis_x = self.df.count()
        for i in range(axis_x.size):
            name = axis_x.index[i]
            count = axis_x.iloc[i]
            if isinstance(name, str) and name.startswith("Unnamed:") and count == 0:
                x = i
                break
        axis_y = self.df.count(axis=1)
        for i in range(axis_y.size):
            count = axis_y.iloc[i]
            if count == 0:
                y = i
                break
        self.df = self.df.iloc[:y, :x]


class ElasticsearchReader(ElasticsearchConnection, Reader):

    def __init__(self, index_name, doc_type=None, es_params=None, batch_size=None, limit=None):
        super().__init__(es_params)
        self.index_name = index_name
        self.doc_type = doc_type
        self.batch_size = batch_size or self.default_batch_size
        self._limit_num = limit
        self.index = self.client.get_index(self.index_name, self.doc_type)

    def get_dataset(self, columns):
        return Dataset(doc["_source"] for doc in self.index.scan()).rename_and_extract(columns)

    @property
    def columns(self):
        if self._columns is None:
            self._columns = self.index.get_columns()
        return self._columns

# class JsonReader(Reader):
#     def __init__(self, file_path, batch_size=None):
#         self.file_path = file_path
#         self.batch_size = batch_size
#         self.file_name = Path(file_path).name
#
#
#
#     def _get_records(self) -> str:
#         """
#         数据生成器
#         :return: 返回数据
#         """
#         with open(self.file_path, 'r') as f:
#             line = f.readline()
#             while line:
#                 yield json_to_dict(line)
#                 line = f.readline()
#
#
#     def get_dataset(self, index_name=None):
#         """
#         获取数据集迭代对象
#         :return: 每一个对象：<class 'src.etl_scp.models.out_models.DataOut'>
#         """
#         get_records = self._get_records()
#         # print('get_records', get_records)
#         return DataSet(self.logger, get_records, self.file_name)
