from etlframe.Mapping.dataset import Dataset
from etlframe.Mapping.heapler import validate_param, print_run_time
from etlframe.Mapping.mapping import Mapping
from etlframe.Reader.reader import Reader
from etlframe.Writer.writer import Writer


class Task(object):
    _dataset = None
    reader = None
    writer = None
    columns = None
    functions = None
    alias_columns = None

    def __init__(self, reader: Reader = None,
                 writer: Writer = None,
                 is_all_columns: bool = True,
                 alias_columns: dict = None,
                 export_columns: set = None,
                 functions=None):
        """

        :param reader: 读取数据的对象
        :param writer: 写入数据的对象
        :param is_all_columns: 是否需要全部的字段 bool
        :param alias_columns: 需要改名的列名
        :param export_columns: 需要导出的列名
        :param functions: 处理列的函数
        """

        self.export_columns = export_columns
        self.alias_columns = alias_columns
        self.is_all_columns = is_all_columns
        if reader is not None:
            self.reader = reader
        if writer is not None:
            self.writer = writer
        if not getattr(self, 'reader', None):
            raise ValueError("%s must have a reader" % type(self).__name__)
        if not isinstance(self.reader, Reader):
            raise ValueError("reader类型错误")
        if self.writer and not isinstance(self.writer, Writer):
            raise ValueError("writer类型错误")

        if functions is not None:
            self.functions = validate_param("functions", functions, dict)  # todo: 此处应该写成错误提供函数样式
        self.columns = self.get_columns()
        # print(self.columns)
        # self.functions = self.get_functions()
        # self.columns_mapping = ColumnsMapping(self.columns, self.is_all_columns)
        # print(self.columns_mapping.alias)
        # print(self.columns_mapping.columns)

        # #
        self.mapping = Mapping(self.columns, self.functions, self.apply_function)

    def get_columns(self):
        if self.is_all_columns:
            if self.export_columns:
                raise ValueError(f"is_all_columns 为True， export_columns 不需要赋值,  请检查{type(self).__name__}参数")
            else:
                if isinstance(self.alias_columns, dict) and self.alias_columns:
                    return {col: self.alias_columns.get(col, '') or col for col in self.reader.columns}
                elif self.alias_columns is None:
                    return {col: col for col in self.reader.columns}
                else:
                    raise ValueError("alias_columns 参数错误")
        else:
            if self.export_columns:
                if self.alias_columns and isinstance(self.alias_columns, dict):
                    return {col: self.alias_columns.get(col, '') or col for col in self.export_columns}
                else:
                    return {col: col for col in self.export_columns}
            else:
                if not self.alias_columns:
                    raise ValueError(
                        f"alias_columns 不存在 and export_columns不存在 and is_all_columns False， 请检查{type(self).__name__}参数")
                else:
                    if isinstance(self.alias_columns, dict):
                        return {col: alias or col for col, alias in self.alias_columns.items()}
                    else:
                        raise ValueError("alias_columns 参数错误")

    def get_functions(self):
        if self.functions:
            return self.functions
        else:
            return {}

    def apply_function(self, record):
        return record

    def filter_function(self, record):
        return True

    def before(self):
        pass

    def after(self):
        pass

    def show(self, num=10):
        self.dataset.show(num)

    @property
    def total(self):
        return self.mapping.total

    @property
    def dataset(self):
        if self._dataset is None:
            self._dataset: Dataset = self.reader.read(self.columns).rename(self.columns).map(self.mapping).filter(
                self.filter_function)
        return self._dataset

    @print_run_time
    def start(self):
        if not getattr(self, "writer", None):
            raise ValueError("%s must have a writer" % type(self).__name__)
        self.before()
        self.dataset.write(self.writer)
        self.after()
