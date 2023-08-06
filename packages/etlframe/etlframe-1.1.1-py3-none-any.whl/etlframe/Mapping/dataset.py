import itertools

import pandas

from etlframe.Mapping.heapler import limit_iterator


class Dataset(object):

    def __init__(self, rows):
        self._rows = rows
        self.total = 0

    def __iter__(self):
        return self

    def next(self):
        self.total += 1
        return next(self._rows)

    __next__ = next

    def map(self, function):
        """
        映射方法
        :param function:
        :return:
        """
        self._rows = (function(r) for r in self._rows)
        return self

    def filter(self, function):
        """
        过滤迭代对象
        :param function:
        :return:
        """
        self._rows = (r for r in self._rows if function(r))
        return self

    def rename(self, columns):
        """
        字段重命名
        """

        def function(record):
            # print(record)
            if isinstance(record, dict):
                return {columns.get(k, k): v for k, v in record.items()}
            else:
                raise ValueError("only rename dict record")

        return self.map(function)

    def rename_and_extract(self, columns):
        """
        字段投影，字段不存在的默认等于None
        """

        def function(record):
            if isinstance(record, dict):
                return {v: record.get(k) for k, v in columns.items()}
            else:
                raise ValueError("only rename dict record")

        return self.map(function)

    def limit(self, num):
        """
        获取迭代对象限制数
        :param num:
        :return:
        """
        self._rows = limit_iterator(self._rows, num)
        return self

    def get_one(self):
        """
        获取迭代对象的第一个值
        :return:
        """
        r = self.get(1)
        return r[0] if len(r) > 0 else None

    def get(self, num):
        """
        根据索引获取迭代对象
        :param num:
        :return:
        """
        return [i for i in itertools.islice(self._rows, num)]

    def get_all(self):
        """
        获取所有迭代对象，对象转列表
        :return:
        """
        return [r for r in self._rows]

    def to_batch(self, size=10000):
        """
        获取迭代对象的长度
        :param size:
        :return:
        """
        while 1:
            batch = self.get(size)
            if batch:
                yield batch
            else:
                return None

    def show(self, num=10):
        """
        显示10条
        :param num:
        :return:
        """
        for data in self.limit(num):
            print(data)

    def write(self, writer):
        """
        写入writer对象
        :param writer:
        :return:
        """
        writer.write(self)

    def to_df(self, batch_size=None):
        """
        转换带pandas
        :param batch_size:
        :return:
        """
        if batch_size is None:
            return pandas.DataFrame.from_records(self)
        else:
            return self._df_generator(batch_size)

    def _df_generator(self, batch_size):
        while 1:
            records = self.get(batch_size)
            if records:
                yield pandas.DataFrame.from_records(records)
            else:
                return None

    def to_csv(self, file_path, batch_size=100000, **kwargs):
        """
        用于大数据量分批写入文件
        :param file_path: 文件路径
        :param sep: 分割符号，hive默认\001
        :param header: 是否写入表头
        :param columns: 按给定字段排序
        :param batch_size: 每批次写入文件行数
        """
        kwargs.update(index=False)
        for df in self.to_df(batch_size=batch_size):
            df.to_csv(file_path, **kwargs)
            kwargs.update(mode="a", header=False)

    def to_json(self, file_path, batch_size=100000, **kwargs):
        for line in self.to_batch(self):
            print(line)






        # for df in self.to_df(batch_size=batch_size):
        #     df.to_json(file_path, orient='records', force_ascii=False, **kwargs)
        #     kwargs.update(mode="a")
