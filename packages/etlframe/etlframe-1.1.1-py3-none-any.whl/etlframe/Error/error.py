class MyError(Exception):
    pass


class SQLTableError(MyError):
    """
    数据库中没有该表
    """

    def __init__(self, table_name: str):
        self.table_name = table_name

    def __str__(self):
        return f'{self.table_name} 数据库中没有该表'


class SqlStatementError(MyError):
    """
    查询语句条件错误
    """

    def __str__(self):
        return f'组合查询语句的条件错误 is_all_columns 和 export_columns 必须传递一个参数, is_all_columns导出全部字段，export_columns导出指定字段'


